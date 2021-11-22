Tapiox is a Python script that gathers hostnames from Bloodhound results and performs correlation of hostnames to IP addresses. There is a ping sweep option that once the list of IP addresses has been generated, each host is pinged a single time to test if it is up or not.

This tool generates reports that are stored in the same directory as the script is located. The reports contain IP addresses, IP addresses with hostnames, and if the ping sweep option is used an additional report is generated which contains each IP and whether it was up or down.

Python modules required: socket, platform, subprocess, json, argparse, datetime

To use this tool, the computers.json file from a Bloodhound collector is required. To access this file, unzip the contents gathered from a Bloodhound collector.

For help: _python tapiox.py -h_

Example command (verbose with ping sweep): _python tapiox.py -f computers.json -v -p_




