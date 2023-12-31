# Welcome to LWT

## File Structure

This project is split into 5 main folders:

1) analysis: Contains nice visualizations and other (non-machine learning) tools.

2) data: Contains all the data generated by each experiment, neatly stashed into its own folder.

3) init: Split into two sub-directories, which contain all the start-up scripts to build the necessary components.

    - loc: Contains files which install various software on the local machine.

    - xdc: Contains files which install on remote hosts using the syntax:

            ./x0-<name>, <username>@<remote host>

4) ml: Contains all the machine learning methods applied to the data.

5) nfra: Contains all the code infrastructure necessary to run the experiments. Currently split into sub-directories:

    - collection: Contains the custom dpdk & click code used to create the data-collecting router.

    - generation: Contains the different packet generation techniques this project analyzes (be it the pipe generation or interfering traffic).

## Configuration

In an attempt to make this package as simple as possible, nearly every important feature is specified in `./config-test.sh`. The configuration options should be clearly labeled in the file, but drop an issue if not!

## Functionality

> Note: All commands are meant to be run from the root of the project. Many scripts source `./config-test.sh`.

`./build-test.sh`: This file reads the configuration file and installs the click router, the pipe generator, the pipe receiver, the external host, and the external server. Each host's software is downloaded to their system, but THEY ARE NOT TURNED ON.

`./run-test.sh`: This file reads the config and runs a test. Must be run AFTER `./build-test.sh` if the testing env has not previously been set up or if any settings have changed.

- The test will generate a CSV, pcap data file, and a copy of the config. The pcap is the recorded data from the tapped server (specified in the config by `srvr_tap`). The CSV file is a record of the size and timestamp of each packet received by the click router set up before the pipe receiver (specified in the config by `click_collector`). The CSV saves data in the form `size:timestamp, size:timestamp` (size is an int, and the timestamp is a float).

`./analysis/csv-vis.py`: This file plots timestamps recorded by `click_collector` for each packet received. Helpful for intuition.

`./nfra/bind.sh`: This script binds the specified interface as a dpdk interface (used when building the click router in `build-test.sh`).

- Uses the syntax:

        ./nfra/bind.sh eth1

`./init/loc/dpdk.sh`: Installs dpdk on the current machine.

`./init/loc/fc.sh`: Installs fastclick with the custom data recorder element on the current machine. Doesn't install the router file, as that isn't necessary at compile time.

`./init/xdc/dpdk.sh`: Installs dpdk on the remote hosts specified.

- Uses the syntax:

        ./init/xdc/dpdk.sh remoteOne, remoteTwo

`./init/xdc/fc.sh`: Installs fastclick on the remote host specified with the same syntax as `./init/xdc/dpdk.sh`. This file is left on the host machine, in the home directory, during `./build-test.sh`. It can be used to recompile fastclick if one wants to make edits to the components currently installed.

- To recompile, navigate to ~ (the same location fastclick is installed) and run:

        ./fastclick.sh recomp

`./init/xdc/iperf3.sh` : Installs client and server iperf3 executable bash scripts to the specified hosts. The reciever side will automatically shut off after a single test

Flag definitions:

    -c <client@ip> 
    -s <server@ip> 
    -p <port num> 
    -i <interval of data collection in seconds> 
    -ip <server's IP address> (default localhost) 
    -u (uses UDP data. Default TCP) 
    -b <bits per second > (default 100M)
    -t <duration (in sec) of iperf run>
    -o <file where you'd like to save server's iperf3 output> (default iperf3.res)

## Limitations

For some reason, running the DPDK router prevents the DNS from resolving. If you have a fix, please let me know.

All traffic generation files executed on any host (either pipe or tap) need to have executable privileges and can be run with the syntax: `./<filename>`

If you run iperf as the traffic generation strategy for the tapped server, be careful. It generates a lot of data very quickly and can be larger than GitHub's allowed file size.

The biggest limitation about this package is its need for "hard coded" values. 

Technically, I could add some more options to the config file and have build functionality transpile new versions of files, but that felt like too much work at this point. If you feel like its necessary, do let me know. 

The hard coded values are listed here:

1) The dpdk interface (ie eth1) needs to be explicitly set in config-test

2) If you're using iperf3, the IP address of the servers need to be explicitly set in config-test

2) Values that need to be hard coded in recorder.cpp (or any other click router you deploy):

    - IP addresses for both experiment internet side interface and to pipe reciever
    - non-dpdk interface name needs to be explicily specified 
    - mac addresses need to be specified for both dpdk interface and interface connected to exteriment internet
    - DPDK interface # (if you have more than one. If only one, defaults save us)

