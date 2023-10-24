# DML-Experiments

## Installation

1. Download a pre-configured Mininet-WiFi virtual machine image from the [Mininet-WiFi GitHub repository](https://github.com/intrig-unicamp/mininet-wifi#pre-configured-virtual-machine)

   -Use P4 version.
2. Import the downloaded image into VMWare Player and start a new VM
3. Install OpenVM tools (ctrl-v, full-screen, etc.)
   ```
   sudo apt-get update
   sudo apt-get install open-vm-tools-desktop
   sudo apt-get install open-vm-tools
   ```
4. Within the VM, update Mininet-WiFi to the latest version:
   ```
   cd mininet-wifi
   git pull
   sudo make install
   ```
5. Install `bridge-utils`:
   ```
   sudo apt install bridge-utils
   ```

6. Install Java:
   ```
   sudo apt install default-jdk
   ```

7. [Download and install InfluxDB](https://docs.influxdata.com/influxdb/v2.5/install/?t=Linux#manually-download-and-install-the-influxd-binary):
   ```
   cd ~/Downloads/
   wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.5.1-linux-amd64.tar.gz
   tar xvzf influxdb2-2.5.1-linux-amd64.tar.gz
   sudo cp influxdb2_linux_amd64/influxd /usr/local/bin/
   rm -r influxdb2-2.5.1-linux-amd64.tar.gz influxdb2_linux_amd64
   ```
   
8. [Download and install the influx CLI](https://docs.influxdata.com/influxdb/v2.5/tools/influx-cli/?t=Linux#install-the-influx-cli):
   ```
   cd ~/Downloads/
   wget https://dl.influxdata.com/influxdb/releases/influxdb2-client-2.5.0-linux-amd64.tar.gz
   tar xvzf influxdb2-client-2.5.0-linux-amd64.tar.gz
   sudo cp influxdb2-client-2.5.0-linux-amd64/influx /usr/local/bin/
   rm -r influxdb2-client-2.5.0-linux-amd64.tar.gz influxdb2-client-2.5.0-linux-amd64
   ```

9. Configure InfluxDB
   
   1. Start InfluxDB:
      ```
      sudo influxd --reporting-disabled
      ```
   
   2. In a second terminal, run the [initial set up](https://docs.influxdata.com/influxdb/v2.5/install/?t=Set+up+with+the+CLI#set-up-influxdb-through-the-influx-cli) and then create a new bucket:
      ```
      sudo influx setup -u dml -p dmldmldml -o dml -b initial -f
      sudo influx bucket create --name test
      ```
      
   3. Stop InfluxDB with CTRL+C in the terminal where you started it.

10. Install the InfluxDB Python Client and other Python dependencies:
   ```
   sudo pip install influxdb-client[async,extra] networkx
   ```

11. Clone the [distributed-data-layer](https://github.com/Apollo-Tools/distributed-data-layer.git) repository:
   ```
   cd ~
   git clone https://github.com/Apollo-Tools/distributed-data-layer.git
   ```

12. Install the DML Python client:
   ```
   cd distributed-data-layer
   sudo pip install -e client-py/
   ```

13. Create a fat jar of the DML node and copy it to the experiments directory:
   ```
   chmod +x gradlew
   ./gradlew shadowJar
   cp node/build/libs/node-1.0-SNAPSHOT-all.jar experiments/dml-node.jar 
   ```

## Usage
### Start the testbed
1. Run the testbed python script:
   ```
   cd ~/distributed-data-layer/experiments/
   sudo python testbed.py
   ```

2. Connect to the Wi-Fi stations:
   ```
   xterm sta1 sta2
   ```

3. In the newly opened xterm windows, start a workload generator:
   ```
   python simple_workload.py name_of_key
   ```

4. In the Mininet-WiFi CLI, start mobility of the stations:
   ```
   start
   ```   

### Stop the testbed
Enter `exit` in the Mininet-WiFi CLI.

### Cleanup
```
sudo mn -c
```
