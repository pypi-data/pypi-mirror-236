import argparse
import asyncio
import time

import numpy as np
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

from dml.asyncio.client import DmlClient
from topology import GraphTopology
from statistics import StatisticsReaderInfluxDB, StatisticsReaderDml


# Source: https://stackoverflow.com/a/70262376
def string_hash(text: str):
    x = 0
    for ch in text:
        x = (x * 281 ^ ord(ch) * 997) & 0xFFFFFFFF
    return x


class Optimizer:
    """
    Optimizer
    """

    def __init__(self, statistics_repository, topology, time_range):
        self.statistics = statistics_repository
        self.topo = topology
        self.time_range = time_range

    def compose_cost_matrix(self, input_size):
        """
        Compose cost matrix (matrix operations)
        """
        # TODO: remove provisional 0 to take into account also second term (not only latency)
        cost = self.topo.storage_ap_latencies + 0 * input_size / self.topo.storage_ap_bandwidths
        return cost

    async def optimize_key(self, key, allowed_replicas, strict_replicas):
        """
        Optimize placement of certain key
        :param key: key specified
        :param allowed_replicas: number of maximum number of replicas to be used
        :param strict_replicas: if False, replicas are optimized, otherwise the exact given number of replicas is used
        :return: proposed reconfigurations e.g., {'<key>': ['Storage A', 'Storage B', 'Storage C']}
        """
        # READ INFLUX DB
        df = await self.statistics.get_traces_key(key, self.time_range)
        if df.empty:
            return {}
        df = df.sort_values(by=["get_accesses", "set_accesses"])
        input_size = df["avg_size"].mean()
        # print(df)

        # ORDER APS ACCORDING TO WEIGHTED GET/SET REQUESTS
        total_accesses = {}
        total_set = {}
        for ap in self.topo.aps:
            if ap in df["ap"].unique():
                total = df.loc[df["ap"] == ap].sum()
                total_set[ap] = total["set_accesses"]
                total_accesses[ap] = total["get_accesses"] * 1 + total["set_accesses"] * 1
            else:
                total_accesses[ap] = 0
                total_set[ap] = 0
        # print("Totals")
        # print(total_accesses)
        # print("Sets")
        # print(total_set)

        cost_matrix = self.compose_cost_matrix(input_size)
        # print(cost_matrix)
        result = {}

        # Algorithm Phase 1: Proposal of reconfiguration
        count = 0
        accesses = total_accesses.copy()
        # Look for the best storage (min. cost) for the AP with more accesses and requests
        for _ in self.topo.storages:
            if count < allowed_replicas:
                best_ap = max(accesses, key=accesses.get)
                idx_best_ap = self.topo.aps.index(best_ap)
                # Find the best storages (list of minimum costs)
                best_storages = [i for i, x in enumerate(cost_matrix[idx_best_ap]) if
                                 x == cost_matrix[idx_best_ap].min()]
                # If different storage nodes available with the same minimum latency, select with Hash(x) mod len(bS)
                if len(best_storages) > 1:
                    best_storage = string_hash(key) % len(best_storages)
                    result[best_ap] = self.topo.storages[best_storages[best_storage]]
                else:
                    result[best_ap] = self.topo.storages[best_storages[0]]
                accesses.pop(best_ap)
                count += 1
        # Return a dictionary including the allowed number of replicas specified by the user:
        # {'Access point name': 'Proposed optimal storage'}
        # Then, evaluate whether introduce these replicas is worthwhile in the second phase.
        if strict_replicas:
            return {key: list(result.values())}
        # Algorithm Phase 2: Evaluation of replicas
        main_ap = list(result.keys())[0]
        proposed_replicas = result.copy()
        proposed_replicas.pop(main_ap)
        idx_main_ap = self.topo.aps.index(main_ap)
        idx_main_storage = self.topo.storages.index(result[main_ap])
        for ap in proposed_replicas.keys():
            idx_proposed_ap = self.topo.aps.index(ap)
            idx_proposed_ap_storage = self.topo.storages.index(result[ap])

            # Cost between main AP and main replica
            cost_main = cost_matrix[idx_main_ap][idx_main_storage] * total_accesses[main_ap]
            # TODO: This cost_main is in both sides of the inequality, so it can be removed for opt. purposes
            # RTT between potential AP and main storage
            rtt = 2 * cost_matrix[idx_proposed_ap][idx_main_storage]
            cost_ap = (rtt / 2) * total_accesses[ap]
            # Sum of all cost NOT including the proposed replica
            cost_nr = 0 * cost_main + cost_ap

            # Cost of maintaining replicas consistent
            cost_consistency = rtt * total_set[main_ap]
            # Cost between proposed AP and proposed storage (not main)
            cost_ap = cost_matrix[idx_proposed_ap][idx_proposed_ap_storage] * total_accesses[ap]
            # Sum of all cost including the proposed replica
            cost_r = 0 * cost_main + cost_ap + cost_consistency

            # If the cost of including the replica is lower than the cost of not doing it...
            if cost_nr < cost_r:
                result.pop(ap)
        # self.plot_graph(self.network_graph)
        return {key: list(result.values())}

    async def optimize_all(self, allowed_replicas, strict_replicas, time_limit):
        """
        Optimize placement of all stored key within a given period of time
        :param strict_replicas: if False, replicas are optimized, otherwise the exact given number of replicas is used
        :param allowed_replicas: number of maximum number of replicas to be used
        :param time_limit: maximum allowed time to optimize keys
        :return: proposed reconfigurations e.g., {'<key A>': ['Storage A'], '<key B>': ['Storage C']}
        """
        # READ INFLUX DB
        start = time.time()
        df = await self.statistics.get_all(self.time_range)
        if df.empty:
            return {}
        grouped_keys = df.groupby(['key']).sum(numeric_only=True)
        grouped_keys['rank'] = grouped_keys['get_accesses'] + grouped_keys['set_accesses'] + grouped_keys['total'] / \
                               grouped_keys['count']
        grouped_keys = grouped_keys.sort_values(by=["rank"], ascending=False)
        ordered_keys = list(grouped_keys['table'].to_dict().keys())
        result = {}
        for k in ordered_keys:
            if (time.time() - start) < time_limit:
                result[k] = (await self.optimize_key(k, allowed_replicas, strict_replicas))[k]
            else:
                break
        return result

    async def optimize_all_matrix(self, df_stats, allowed_replicas, current_configurations, reconfig_threshold):
        """
        Optimize placement of all stored keys
        :param df_stats: dataframe containing access statistics
        :param allowed_replicas: strict number of replicas that must be used
        :param current_configurations: current placements of keys
        :return: proposed reconfigurations e.g., {'<key A>': ['Storage A'], '<key B>': ['Storage C']}
        """
        # COMPUTE USED MEMORY
        # df_sizes = await self.statistics.get_sizes(self.time_range)
        # key_configurations = await self.dml.get_all_configurations()
        # print(df_sizes)
        # if key_configurations is None:
        #    return "Empty metadata"

        # storage_used_memory = {}
        # for storage in self.topology.storages:
        #    storage_used_memory[storage] = 0
        #    for key, configuration in key_configurations.items():
        #        key_size = df_sizes[df_sizes["key"] == key]['avg_size'].values[0]
        #        replicas = [str(replica.id) for replica in configuration.replicas]
        #        if storage in replicas:
        #            storage_used_memory[storage] += key_size

        # print(storage_used_memory)

        # CALCULATE RANK FROM INFLUX DB ACCESSES AND SIZE
        df_stats['rank'] = df_stats['get_accesses'] + df_stats['set_accesses']
        cost_matrix = self.compose_cost_matrix(0.008)  # Network cost matrix
        keys = df_stats['key'].unique()  # Get keys list from influx df
        # Keys may not have accesses from all aps
        # So fill with zeros to multiply with cost_matrix
        # COMPUTE RANK MATRIX AND MULTIPLY BY COST
        rank = np.zeros((len(self.topo.aps), len(keys)))
        for key_idx, key in enumerate(keys):
            df_k = df_stats[df_stats["key"] == key]
            aps = df_k['ap'].unique()
            for ap in aps:
                ap_idx = self.topo.aps.index(ap)
                rank[ap_idx][key_idx] = df_k[df_k["ap"] == ap]["rank"].sum()
        rank = np.dot(cost_matrix, rank)

        # SELECT MINIMUM COST FOR 'R' REPLICAS
        result = {}
        for key_idx, key in enumerate(keys):
            # Iterate over each column of the rank matrix (keys)
            rank_k = list(rank[:, key_idx])
            # Get the indices that would sort the ranks
            sorted_rank_k_indices = np.argsort(rank_k)
            assigned = 0
            proposed_storages = []
            proposed_hosts = []
            proposed_region = None
            # Iterate over the sorted array of ranks (storages)
            for rank_idx in sorted_rank_k_indices:
                if assigned >= allowed_replicas:
                    break
                # Get associated storage
                storage_idx = rank_idx
                storage = self.topo.storages[storage_idx]
                # Replicas should not be stored on the same host but within the same region
                host = self.topo.get_node_attribute(storage, 'host')
                region = self.topo.get_node_attribute(storage, 'region')
                if proposed_region is None:
                    proposed_region = region
                if host not in proposed_hosts and region == proposed_region:
                    proposed_storages.append(storage)
                    proposed_hosts.append(host)
                    assigned += 1
            # Sort storages by the expected write accesses (write accesses always go to the first storage)
            proposed_storages = self.sort_storages_by_writes(df_stats, key, proposed_storages)
            # Check whether a reconfiguration is worthwhile
            current_storages = [str(storage.id) for storage in current_configurations[key].replicas]
            score_diff = self.compute_placement_score_diff(df_stats, key, current_storages, proposed_storages)
            result[key] = proposed_storages if abs(score_diff) > reconfig_threshold else current_storages

        return result

    def compute_placement_score_diff(self, df_stats, key, current_storage_ids, new_storage_ids):
        if new_storage_ids == current_storage_ids:
            return 0.0
        # Note that a lower score (RTT) is better
        old_score = self.average_rtt(df_stats, key, current_storage_ids)
        new_score = self.average_rtt(df_stats, key, new_storage_ids)
        rel_score_diff = (old_score - new_score) / old_score if old_score != 0.0 else 0.0
        return rel_score_diff

    def sort_storages_by_writes(self, df_stats, key, storages):
        """Sorts the given storages by the expected write accesses to the given key in descending order."""
        set_accesses = []
        for storage in storages:
            # Get the closest AP to the storage
            closest_ap_idx = np.argmin(self.topo.storage_ap_latencies[self.topo.storages.index(storage)])
            closest_ap = self.topo.aps[closest_ap_idx]
            # Get the number of write accesses to the key from the closest AP
            num_set_accesses = \
                df_stats[(df_stats['ap'] == closest_ap) & (df_stats['key'] == key)]['set_accesses'].sum()
            set_accesses.append(num_set_accesses)
        return [storage for _, storage in sorted(zip(set_accesses, storages), reverse=True)]

    def rtt_for_read_req(self, ap, replicas):
        return min([2 * self.topo.get_ap_to_storage_latency(ap, replica) for replica in replicas])

    def rtt_for_write_req(self, ap, replicas):
        replication_rtt = 0 if len(replicas) <= 1 \
            else max([2 * self.topo.get_storage_latency(replicas[0], replica) for replica in replicas[1:]])
        return 2 * self.topo.get_ap_to_storage_latency(ap, replicas[0]) + replication_rtt

    def average_rtt(self, df_stats, key, replicas):
        df_key = df_stats[df_stats['key'] == key]
        sum_requests = 0
        sum_rtts = 0
        for ap in df_key['ap']:
            read_requests = df_key[(df_key['ap'] == ap)]['get_accesses'].sum()
            write_requests = df_key[(df_key['ap'] == ap)]['set_accesses'].sum()
            sum_requests += read_requests + write_requests
            sum_rtts += read_requests * self.rtt_for_read_req(ap, replicas) \
                        + write_requests * self.rtt_for_write_req(ap, replicas)
        return sum_rtts / sum_requests


async def reconfigure_key(dml, key, storage_ids):
    lock_token = await dml.lock(key)
    await dml.reconfigure(key, storage_ids)
    await dml.unlock(key, lock_token)


async def main(argv=None):
    args = parse_args(argv)

    dml = DmlClient(args.dml_hostname, args.dml_port)

    if args.use_influxdb:
        influx_client = InfluxDBClientAsync(url=args.influxdb_url, username="dml", password="dmldmldml", org="dml")
        statistics = StatisticsReaderInfluxDB(influx_client, 'test')
    else:
        statistics = StatisticsReaderDml(dml)

    #  Create graph and optimizer
    topology = GraphTopology()
    # plot_graph(network_graph)
    optimizer = Optimizer(statistics, topology, args.time_window_length)
    await dml.connect()
    i = 0
    while True:
        i += 1
        df_stats = await statistics.get_all(args.time_window_length)
        if df_stats.empty:
            await asyncio.sleep(args.delay)
            continue
        key_configurations = await dml.get_all_configurations()
        result = await optimizer.optimize_all_matrix(df_stats, args.num_replicas,
                                                     key_configurations, args.reconfig_threshold)
        reconfig_tasks = []
        for key in result:
            new_storage_ids = result[key]
            current_configuration = key_configurations[key]
            if current_configuration is None:
                continue
            current_storage_ids = [str(storage.id) for storage in current_configuration.replicas]
            if new_storage_ids != current_storage_ids:
                print(time.monotonic(), i, key, 'reconfigure',
                      '"' + ','.join(current_storage_ids) + '"', '"' + ','.join(new_storage_ids) + '"',
                      sep=',')
                reconfig_tasks.append(reconfigure_key(dml, key, [int(storage_id) for storage_id in new_storage_ids]))
        await asyncio.gather(*reconfig_tasks)
        await asyncio.sleep(args.delay)

    #  metadata_client.disconnect()
    #  if args.use_influxdb:
    #      await influx_client.close()


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='dml_hostname', default='localhost',
                        help='hostname of a metadata server')
    parser.add_argument('--port', dest='dml_port', type=int, default=9000,
                        help='port of the metadata server')
    parser.add_argument('--use-influxdb', dest='use_influxdb', action='store_true')
    parser.add_argument('--influxdb-url', dest='influxdb_url', default='http://localhost:8086',
                        help='URL of the InfluxDB where client traces are stored')
    parser.add_argument('--replicas', dest='num_replicas', type=int, default=1,
                        help='number of replicas per key')
    parser.add_argument('--delay', dest='delay', type=int, default=10,
                        help='delay in seconds to wait between executions of the optimizer')
    parser.add_argument('--window', dest='time_window_length', type=int, default=10,
                        help='the length of the time window in seconds for which to query past client traces')
    parser.add_argument('--reconfig-threshold', dest='reconfig_threshold', type=float, default=0.05)
    return parser.parse_args(args)


if __name__ == '__main__':
    asyncio.run(main())
