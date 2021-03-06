#### TO DO
#### Fully flesh out quiet and verbose modes

#Import modules
import os
import socket
import platform
import subprocess
import json
import argparse
import datetime

#The below code blocks use argparse to define and take in arguments from the command line.
parser = argparse.ArgumentParser(description='Tapiox is a Python script that extracts hostnames from the computers.json file gathered from Bloodhound collectors and correlates IP addresses to the hostnames. For this script to work, the Bloodhound output results will need to be unzipped. This script generates reports and stores them in the directory this tool is kept in. Quiet mode is the default setting.')

parser.add_argument('-f','--filepath', metavar='', type=str, required=True, help='Path to computers.json file')
parser.add_argument('-p', '--ping', action='store_true', help="Pings each identified IP address a single time. If a "
                                                               "response occurs, it is marked UP, if not it is marked"
                                                               " DOWN")

group = parser.add_mutually_exclusive_group()
group.add_argument('-v','--verbose', action='store_true', help="Print all output and descriptions of actions "
                                                                "as they are occurring")
group.add_argument('-q','--quiet', action='store_true', help="Suppress all output until the end")
args = parser.parse_args()

#Get operating system
opsys = platform.system().lower()

#Get file location
#filepath = input("Please enter full path to Bloodhound computers.json file: ")

#Empty hostname list for future population
hostnameList = []

#Empty IP list for future population
ipList = []

#Empty list for future population of hostnames that correlate to IP addresses
hostWithIPList = []

#Empty hostname list for hostnames that do not correlate to an IP address
noIPList = []

#Empty list for IP addresses and ping status
pingList = []

#Current date and time variables to be used in report generation
currentDT = datetime.datetime.now()
dt_string = currentDT.strftime("%Y%m%d%H%M")

#This function opens the computers.json file and iterates through the keys looking for the "name" subkey under "Properties".
# The value of name is the hostname. This hostname is appended to hostnameList.
def jsonHostnameValueExtraction(filepath):
    if args.verbose:
        print('Extracting hostnames from ' + filepath)
    with open(filepath) as computersJson:
        jsonData = json.load(computersJson)
        for computer in jsonData['computers']:
            propertyDict = computer['Properties']
            valuesList = list(propertyDict.values())
            hostnameList.append(valuesList[0])

#This function iterates through hostnameList and gets the IP address of each host. If there is a correlating IP,
# the hostname and IP are appended to hostWithIPList as a tuple and the IP is appended to ipList, if there is no
# correlating IP address then the hostname is appended to noIPList.

def hostnameToIP():
    if args.verbose:
        print('Correlating hostnames to IP addresses\n')
    for hostname in hostnameList:
        try:
            ip = socket.gethostbyname(hostname)
            ipList.append(ip)
            ipHost = (hostname, ip)
            hostWithIPList.append(ipHost)
            if args.verbose:
                print('IP of ' + hostname + ' is ' + ip)
        except:
            noIPList.append(hostname)
            if args.verbose:
                print('No IP found for ' + hostname)

#This function first tests for the operating system and sets the ping paramater based off the OS. Once this is done,
#it iterates through ipList pinging each host a single time. If a host is up, it is tagged with "UP" and if the host is
#down, it is tagged with "DOWN". This data is appended to pingList.

def pingTest():
    if args.verbose:
        "Starting ping test"
    if opsys == "windows":
        parameter = "-n"
    else:
        parameter = "-c"
    for ip in ipList:
        pingCmd = ['ping', parameter, '1', ip]
        status = subprocess.call(pingCmd)
        if status == 0:
            if args.verbose:
                print(ip + ' UP')
            ipStatus = (ip, 'UP')
            pingList.append(ipStatus)
        else:
            if args.verbose:
                print(ip + ' DOWN')
            ipStatus = (ip, 'DOWN')
            pingList.append(ipStatus)

#The below function generates reports based off the actions performed. By default, it generates a hostname/IP list
#as well as a list with just IP addresses. If the -p option is used, it will also generate a report with the status of
#each host that was pinged.

def generateReports():
    ipFileName = (dt_string + "_IP_list.txt")
    ipFile = open(ipFileName, "a")
    for ip in ipList:
        ipFile.write(ip + '\n')
    ipFile.close()
    hostWithIPFileName = (dt_string + "_Host_and_IP_list.txt")
    hostWithIPFile = open(hostWithIPFileName, "a")
    for hostWithIP in hostWithIPList:
        hostWithIPFile.write(str(hostWithIP[0]) + ' ' + str(hostWithIP[1]) + '\n')
    hostWithIPFile.close()
    if args.ping:
        pingStatusFileName = (dt_string + "_Ping_Status.txt")
        pingStatusFile = open(pingStatusFileName, "a")
        for pingStatus in pingList:
            pingStatusFile.write(str(pingStatus[0]) + ' ' + str(pingStatus[1]) + '\n')

if __name__ == '__main__':
    jsonHostnameValueExtraction(args.filepath)
    hostnameToIP()
    if args.ping:
        pingTest()
    generateReports()
