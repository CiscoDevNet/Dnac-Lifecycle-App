#! /usr//bin/env python


'''

Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

'''

__copyright__ = "Copyright (c) 2018 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.0"

import argparse
import pprint
import sys
import getpass
from urllib.request import urlopen
from urllib.error import URLError
import socket
import json
import os
import warnings
from caa import Caa_session
from dnac import Dnac_session
from xl import xl

LC_CHUNK = 10
DEVICE_CHUNK = 10
OS_TYPE_LIST = {"ACNS","ACSW","ALTIGAOS","ASA","ASYNCOS","CATOS","CDS-IS","CDS-TV","CDS-VN","CDS-VQE","CTS","CUSP","ECDS","FWSM-OS","GSS","IOS","IOS XR",
                "IOS-XE","IPS","NAM","NX-OS","NX-OS ACI","ONS","PIXOS","SAN-OS","STAR OS","TC","TE","UCS NX-OS","VCS","VDS-IS","WAAS",
                "WANSW BPX/IGX/IPX","WEBNS","WLC","WLSE-OS","XC"}
LC_TYPE = ["PSIRT","HWEOL","TEST"]

#Check for internet/network connection
def internet_on():
    try:
        urlopen('http://www.ciscoactiveadvisor.com',timeout=2)
        return True
    except URLError as err:
        return False

# Quick check if the entered ip address is a valid one
def valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

#Check if OS Type is in the category
def check_type(type):
    if(type in OS_TYPE_LIST):
        return True
    else:
        return False


# Provide different offsets for user input based on DEVICE_CHUNK above
def get_dev_offset(dcount,chunk): #user input
    loop_num = dcount / chunk if dcount % chunk == 0 else (dcount // chunk + 1)
    if loop_num == 1:  # dcount < 100
        offset = "1-" + str(dcount)
    if dcount > (chunk-1):
        # Display options to the user to enter
        i = 0
        start = 1
        display_string = "\nPlease select the devices - "
        while (i < loop_num):
            display_string = display_string + "[" + str(start) + "-" + (
                str(start + (chunk-1)) if (start + (chunk-1)) < dcount else str(dcount)) + "]"
            start = start + chunk
            i = i + 1
        offset = input(display_string)
    return offset

# Extract all relevant information from device data
def map_ddata(devices):
    dev_dict = dict()
    dup_dev_dict = dict()
    template = '{:<30} {:<20} {:<6}'
    table_headers = ['Hostname', 'PlatformId', 'Serial']
    table_ul = ['--------','----------','------']
    print (template.format(*table_headers))
    print(template.format(*table_ul))

    for dev in devices["response"]:
        if dev.get("platformId") != None and dev.get("platformId") != "":
            #Force IOS if no Software type found
            if (dev.get("softwareType") == "" or  dev.get("softwareType") == None):
                dev["softwareType"] = "IOS"
            #Check if Software type is supported by CAA else force IOS
            if(check_type(dev["softwareType"]) == False):
                if (dev["softwareType"] == "Cisco Controller"):
                    dev["softwareType"] = "WLC"
                else:
                    #Forcing it to IOS
                    dev["softwareType"] = "IOS"
            key = dev["platformId"] + ";"+ dev["softwareType"] + ";" + dev["softwareVersion"]
            devinfo = {}
            devinfo["hostname"] = dev["hostname"] if dev.get("hostname") != None else ""
            devinfo["type"] = dev["type"] if dev.get("type") != None else ""
            devinfo["serialNumber"] = dev["serialNumber"] if dev.get("serialNumber") != None else None
            devinfo["ip"] = dev["managementIpAddress"] if dev.get("managementIpAddress") != None else None
            devinfo["mac"] = dev["macAddress"] if dev.get("macAddress") != None else None
            devinfo["pid"] = dev["platformId"]
            devinfo["osType"] = dev["softwareType"]
            devinfo["swVersion"] = dev["softwareVersion"]
            dup_dev_dict[dev["serialNumber"]] = devinfo
            dev_dict[key] = devinfo
            # Print all device info
            print(template.format(devinfo["hostname"],dev["platformId"],devinfo["serialNumber"]))
        else:
            print(template.format(dev["hostname"],"---",dev["softwareType"]))
    print("\n")
    return dev_dict,dup_dev_dict

# Get json object for posting
def get_queryset_map(dev_dict):
    queryset_array = []
    queryset ={"queries":[]}
    ct = 0
    for key,value in dev_dict.items():
        if(ct%LC_CHUNK == 0 and ct != 0):
            queryset_array.append(queryset)
            queryset = {"queries":[]}
        queryjson ={}
        queryjson["pid"] = key.split(";")[0]
        queryjson["osType"] = key.split(";")[1]
        queryjson["swVersion"] = key.split(";")[2]
        queryset["queries"].append(queryjson)
        ct = ct +1
    queryset_array.append(queryset)
    return queryset_array

# Merge the results with duplicate device data with same OS type, version and PID
def merge_data(lc_resp, dup_data):
    merged_data = dict()
    # loop through responses
    for device in lc_resp["responses"]:
        #Loop through the dup_data
        for key,dup_device in dup_data.items():
            dev_details = {}
            if(device["pid"] == dup_device["pid"] and device["osType"] == dup_device["osType"] and
                    device["swVersion"] == dup_device["swVersion"]):
                dev_details["serial"] = dup_device["serialNumber"]
                dev_details["psirts"] = device["psirts"]
                dev_details["hweol"] = device["hweol"] if device.get("hweol") != None else None
                dev_details["sweol"] = device["sweol"] if device.get("sweol") != None else None
                dev_details["pid"] = dup_device["pid"]
                dev_details["osType"] = dup_device["osType"]
                dev_details["swVersion"] = dup_device["swVersion"]
                dev_details["hostname"] = dup_device["hostname"] if dup_device.get("hostname") is not None else None
                dev_details["type"] = dup_device["type"] if dup_device.get("type") is not None else None
                dev_details["serial"] = dup_device["serial"] if dup_device.get("serial") is not None else None
                dev_details["ip"] = dup_device["ip"] if dup_device.get("ip") is not None else None
                dev_details["mac"] = dup_device["mac"] if dup_device.get("mac") is not None else None
                dev_details["serial"] = dup_device["serialNumber"]
                dev_details["psirts"] = device["psirts"]
                dev_details["hweol"] = device["hweol"] if device.get("hweol") != None else None
                dev_details["sweol"] = device["sweol"] if device.get("sweol") != None else None
                dev_details["pid"] = device["pid"]
                dev_details["osType"] = device["osType"]
                dev_details["swVersion"] = device["swVersion"]
                dev_details["hostname"] = dup_device["hostname"] if dup_device.get("hostname") is not None else None
                dev_details["type"] = dup_device["type"] if dup_device.get("type") is not None else None
                dev_details["serial"] = dup_device["serial"] if dup_device.get("serial") is not None else None
                dev_details["ip"] = dup_device["ip"] if dup_device.get("ip") is not None else None
                dev_details["mac"] = dup_device["mac"] if dup_device.get("mac") is not None else None
                merged_data[key] = dev_details
    return merged_data

def main():

    #Suppress warnings
    warnings.filterwarnings("ignore")

    #set up the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['lifecycle'], type=str, help='command = "lifecycle" for security advisories, hardware ' \
                                                                                   'end-of-life and software end-of-life')
    parser.add_argument('-i','--ipaddress', type=str, help='DNA Center cluster ip address')
    parser.add_argument('-u', '--uname', type=str, default='admin', help='DNA Center login username')

    args = parser.parse_args()
    pp = pprint.PrettyPrinter(indent=4)

    #Basic checks
    if internet_on() == False:
        print ('You need internet connection to run the program')
        sys.exit('No Internet')
    if valid_ip(args.ipaddress) == False:
        print ('You need to provide a valid ipaddress')
        sys.exit('Invalid ipaddress')
    if args.uname == '':
        print ('You need to provide a valid DNAC login username')
        sys.exit('Invalid username')

    #Prompt for password
    dnacPwd = getpass.getpass("\nPlease enter the DNA Center \'{}\' user password for the {} cluster : ".format(args.uname,args.ipaddress))

    #Get DNAC object
    dnac = Dnac_session(args.ipaddress,args.uname,dnacPwd)

    print("\n########### Please enter CCO Credentials ##########")
    cco_pre ={}
    uname = input("\nPlease enter CCO user name: ")
    pwd = getpass.getpass("\nPlease enter CCO pwd: ")
    cco_pre["username"] = uname
    cco_pre["password"] = pwd

    #Login to CAA
    caa = Caa_session(cco_pre)

    if caa.authenticated == False:
        print('\n Invalid CCO Credentials')
        sys.exit(2)


    print("\n########### Successfully got CCO Credentials ##########")

    print("\n########### Trying to retrieve devices from DNA Cluster {} ##########".format(args.ipaddress))

    #Get Device count
    dcount = dnac.get_dev_count()

    print("\n########### Found {} devices in the cluster {} ##########".format(dcount,args.ipaddress))

    #Get Offset from user
    offset = get_dev_offset(dcount,DEVICE_CHUNK)

    #Get device list based on user offset
    start,end = offset.replace(" ","").split('-')

    print("\n")
    print("\n########### Retrieving {} devices from device #{}  ##########".format(int(end)-int(start)+1,start))

    devices = dnac.get_devices(start,int(end)-int(start)+1) # end-start = # of devices

    #Extract key data (pid/os type/os version)
    ddata_map,dup_ddata_map = map_ddata(devices)

    #Chunk them into array of 10 dev (max allowed to query lc)
    caa_array = get_queryset_map(ddata_map)


    #Check to see if they have DNACaaP ITSM installed
    ticket = "N"
    message = dnac.post_itsm("Dummy", LC_TYPE[2])
    if (message == "The request has been accepted for execution"):
        print("########## We detect DNACaaP ServiceNow package in your cluster ##########")
        ticket = input("\nWould you like to automatically generate a ticket for your lifecycle data? Type Y/N ")

    #Templates for displaying device and LC info
    template = '{:<20} {:<15} {:<6}'
    table_headers = ['PlatformId', 'S/w Type', 'S/w Version']
    table_ul = ['--------', '----------', '------']

    uber_data = dict()
    num_psirts = 0
    num_hweol = 0
    num_sweol = 0
    #Get lifecycle data -- loop through the json array
    for query_set in caa_array:
        print("\n")
        print("########## Retrieving Lifecycle info for these devices (max 10) ##########")
        print(template.format(*table_headers))
        print(template.format(*table_ul))
        for query in query_set["queries"]:
            print(template.format(query["pid"], query["osType"], query["swVersion"]))

        lc_data = caa.get_lc_info(query_set)
        tmp_uber_data = merge_data(json.loads(json.dumps(lc_data)),json.loads(json.dumps(dup_ddata_map)))
        uber_data = {**uber_data, **tmp_uber_data}

        for key in tmp_uber_data:
            dev = tmp_uber_data[key]
            if dev.get("psirts") != None and len(dev.get("psirts")) != 0 and dev.get("psirts") != "":
                for psirt in dev["psirts"]:
                    num_psirts += 1
                # Raise ITSM ticket if there are PSIRTs
                if(ticket == 'Y' or ticket == 'y'):
                    message = dnac.post_itsm(dev,LC_TYPE[0])
                    if (message == "The request has been accepted for execution"):
                        print("\n########## Created a ticket with ServiceNow for Security Advisories against  - {} ##########".format(
                                dev["hostname"]))
            num_sweol = num_sweol + 1 if dev.get("sweol") != None else num_sweol
            if dev.get("hweol") != None:
                num_hweol = num_hweol + 1
                # Raise ITSM ticket if there is HWEOL
                if (ticket == 'Y' or ticket == 'y'):
                    message = dnac.post_itsm(dev,LC_TYPE[1])
                    if (message == "The request has been accepted for execution"):
                       print("\n########## Created a ticket with ServiceNow for the EOL device  - {} ##########".format(dev["hostname"]))
    print("\n########## Summary of Lifecycle ##########")
    print("Number of PSIRTS - " +  str(num_psirts) )
    print("Number of HWEOL - " + str(num_hweol))
    print("Number of SWEOL - " + str(num_sweol))

    if(ticket != 'Y'):
        xl_sess = xl()
        xl_sess.create_xlsxwriter_xl(uber_data)
        print("\nPlease check \'lifecycle.xls\' in {} for the complete lifecycle information\n".format(os.getcwd()))

if __name__ == '__main__':
    main()