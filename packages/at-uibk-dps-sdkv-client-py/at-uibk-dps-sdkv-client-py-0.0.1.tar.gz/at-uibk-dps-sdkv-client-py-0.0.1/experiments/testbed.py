#!/usr/bin/python
import math
import os
import random

from mininet.node import Host
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.nodelib import LinuxBridge as LinuxBridgeSwitch
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.nodelib import LinuxBridge as LinuxBridgeAP
from mn_wifi.wmediumdConnector import interference


def start_testbed():
    net = Mininet_wifi(switch=LinuxBridgeSwitch,
                       accessPoint=LinuxBridgeAP,
                       link=wmediumd,
                       wmediumd_mode=interference,
                       ipBase='10.0.0.0/8')

    # we do not need a controller yet
    #info('*** Adding controller\n')
    #c0 = net.addController(name='c0',
    #                       controller=Controller,
    #                       protocol='tcp',
    #                       port=6653)

    info('*** Add switches/APs\n')
    # add main switch
    s0 = net.addSwitch('s0', cls=LinuxBridgeSwitch)
    # add APs arranged in a grid
    columns = 2
    rows = 2
    ap_range = 313
    ap_distance = 2 * ap_range * math.sin(math.radians(45))
    ap_x_offset = ap_range * math.sin(math.radians(45))
    ap_y_offset = ap_range * math.sin(math.radians(45))
    aps = []
    for x in range(columns):
        for y in range(rows):
            ap_id = len(aps) + 1
            ap_pos_x = ap_x_offset + x * ap_distance
            ap_pos_y = ap_y_offset + y * ap_distance
            ap_pos_z = 0
            ap_channel = random.randint(1, 11)
            aps.append(net.addAccessPoint('ap{}'.format(ap_id), cls=LinuxBridgeAP, ssid='ap{}'.format(ap_id),
                                          channel='{}'.format(ap_channel), mode='g',
                                          position='{},{},{}'.format(ap_pos_x, ap_pos_y, ap_pos_z)))
    # add switches between APs and hosts
    ap_host_switches = []
    for i in range(len(aps)):
        ap_host_switches.append(net.addSwitch('s{}'.format(i + 1), cls=LinuxBridgeSwitch))

    info('*** Add hosts/stations\n')
    ip_offset = 1
    # storage nodes
    hosts = []
    for i in range(len(aps)):
        hosts.append(net.addHost('h{}'.format(i + 1), cls=Host, ip='10.0.0.{}'.format(ip_offset)))
        ip_offset += 1

    # stations (clients)
    ip_offset = max(ip_offset, 128)
    stations = []
    stations.append(net.addStation('sta1', ip='10.0.0.{}'.format(ip_offset),
                                   min_x=0, max_x=aps[-1].position[0] + ap_x_offset,
                                   min_y=0, max_y=aps[-1].position[1] + ap_y_offset,
                                   min_v=15, max_v=25))
    ip_offset += 1
    stations.append(net.addStation('sta2', ip='10.0.0.{}'.format(ip_offset),
                                   min_x=0, max_x=aps[-1].position[0] + ap_x_offset,
                                   min_y=0, max_y=aps[-1].position[1] + ap_y_offset,
                                   min_v=20, max_v=35))
    ip_offset += 1

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=2)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info('*** Add links\n')
    for ap, host, switch in zip(aps, hosts, ap_host_switches):
        net.addLink(ap, switch, cls=TCLink, delay='5ms')
        net.addLink(switch, host, cls=TCLink, delay='5ms')
        net.addLink(switch, s0, cls=TCLink, delay='30ms')

    net.plotGraph(max_x=3000, max_y=3000)

    info('*** Set mobility model\n')
    net.setMobilityModel(time=0, model='RandomDirection', max_x=2000, max_y=2000, seed=20)
    # by default, the simulation starts automatically
    # we stop it here and later start it manually using the 'start' command from the CLI
    net.stop_simulation()

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches/APs\n')
    s0.start([])
    for switch in ap_host_switches:
        switch.start([])
    for ap in aps:
        ap.start([])

    info('*** Post configure nodes\n')
    # create a directory for log files
    working_directory = os.path.abspath(os.path.dirname(__file__))
    log_directory = os.path.join(working_directory, 'logs')
    os.makedirs(log_directory, exist_ok=True)

    # start a DML node on each host
    for host in hosts:
        dml_jar_path = os.path.join(working_directory, 'dml-node.jar')
        config_path = os.path.join(working_directory, 'conf', 'config_mn_' + host.name + '.json')
        # start the node and redirect the output to a log file
        host.cmd('VERTX_CONFIG_PATH="' + config_path + '" java -jar ' + dml_jar_path
                 + ' &> ' + os.path.join(log_directory, host.name + '_dml.log')
                 + ' &', shell=True)

    # start InfluxDB on the first host and redirect logs to a log file
    hosts[0].cmd('influxd --reporting-disabled'
                 + ' &> ' + os.path.join(log_directory, hosts[0].name + '_influxdb.log')
                 + ' &', shell=True)

    CLI(net)
    net.stop()


if __name__ == '__main__':
    random.seed(42)
    setLogLevel('info')
    start_testbed()
