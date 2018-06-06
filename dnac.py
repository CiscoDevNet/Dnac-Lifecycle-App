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

import requests
import json
import sys
import uuid
import time
from requests.auth import HTTPBasicAuth


#Global variables
BASIC_AUTH_API = "https://{}/api/system/v1/identitymgmt/login"
DEVICES_API = "https://{}/api/v1/network-device/{}/{}"
DEVICE_CT_API = "https://{}/api/v1/network-device/count"
DNACAAP_ITSM_POST_API = "https://{}/api/dnacaap/v1/dnacaap/core/dna/events/{}/event"
ITSM_BAPI_NAME="Publish DNA Event"
ITSM_SYSTEM_NAME = "ServiceNow"
TEST_EVENT_POST_BODY= '''
{
    "id": "{}",
    "name": "Test",
    "category": "Info",
    "domain": "EOL",
    "description": "This is a test message",
    "type": "Network",
    "status": "New",
    "severity": "P5",
    "timestamp": "",
    "tenantId": "",
    "namespace": "",
    "version": "",
    "thresholdDefinitions": "",
    "assignedTo": "",
    "isCorrelatedEvent": "",
    "actualServiceId": "",
    "workflowIndicator": "RFC",
    "enrichmentInfo": {
        "details":"Testing ITSM"
    }
}
'''
HWEOL_EVENT_POST_BODY= '''
{
    "id": "{}",
    "name": "Hardware End of Life",
    "category": "Warn",
    "domain": "EOL",
    "description": "This device may be end-of-life",
    "type": "Network",
    "status": "New",
    "severity": "P2",
    "timestamp": "",
    "tenantId": "",
    "namespace": "",
    "version": "",
    "thresholdDefinitions": "",
    "assignedTo": "",
    "isCorrelatedEvent": "",
    "actualServiceId": "",
    "workflowIndicator": "RFC",
    "enrichmentInfo": {
        "details":
        {
            "device": {
                "macAddress": "{}",
                "hostname": "{}",
                "node": "{}",
                "softwareVersion": "{}",
                "productId": "{}"
            },
            "eol":{
                "announceDate" : "{}",
                "eoSaleDate": "{}",
                "eoSupportDate": "{}",
                "MigrationPid": "{}"
            }
        }
    }
}
'''
PSIRT_EVENT_POST_BODY = '''
{
    "id": "{}",
    "name": "Security Advisories",
    "category": "Warn",
    "domain": "EOL",
    "description": "This device has security advisories",
    "type": "Network",
    "status": "New",
    "severity": "P2",
    "timestamp": "",
    "tenantId": "",
    "namespace": "",
    "version": "",
    "thresholdDefinitions": "",
    "assignedTo": "",
    "isCorrelatedEvent": "",
    "actualServiceId": "",
    "workflowIndicator": "RFC",
    "enrichmentInfo": {
        "details":
        {
            "device": {
                "macAddress": "{}",
                "hostname": "{}",
                "node": "{}",
                "softwareVersion": "{}",
                "productId": "{}"
            },
            "psirts":{
                "psirts": "{}"
            }
        }
    }
}
'''



class Dnac_session:

#Login to DNAC
    def __init__(self,ip, user, pwd):
        self.sess = requests.Session()
        self.sess.cookie = {}
        self.ip = ip
        self.authtoken = ""
        try:
            r = self.sess.get(BASIC_AUTH_API.format(ip), auth=HTTPBasicAuth(user, pwd), timeout=10, verify=False)
            if r.status_code == 200:
                # Add the JWT token to header
                ckies = r.headers['Set-Cookie'].split(";")
                for ckie in ckies:
                    try:
                        name, value = ckie.split('=')
                    except ValueError:
                        name, value = "", ""
                    if name == "X-JWT-ACCESS-TOKEN":
                        self.authtoken = value
                        self.sess.cookie[name] = value
                print("\n########### DNAC Login Successful ##########")
            else:
                print(r.content.decode("utf-8"))
                sys.exit(1)
        except requests.exceptions.ConnectionError:
            sys.exit('Unable to connect to Cluster')

#Get Event id (UUID)
    def get_eventid(self):
        e_id = uuid.uuid4()
        return e_id

#Get proper date format
    def date_format(self,epoch_num):
        # convert into secs and make it human readable
        format_date = time.strftime('%Y-%m-%d', time.localtime(epoch_num / 1000))
        return format_date

#Get Device Count
    def get_dev_count(self):
        r = self.sess.get(DEVICE_CT_API.format(self.ip), cookies=self.sess.cookie, verify=False)
        ct_resp = r.json()
        return ct_resp["response"]

#Get Devices
    def get_devices(self, start, limit):
        r = self.sess.get(DEVICES_API.format(self.ip, start, limit), cookies=self.sess.cookie, verify=False)
        dev_resp = r.json()
        return dev_resp

#Post to ServiceNow
    def post_itsm(self,dev,type):
        eventid = self.get_eventid()
        body=""
        if(type == "HWEOL"):
            body = json.loads(HWEOL_EVENT_POST_BODY)
            body["id"] = str(eventid)
            body["enrichmentInfo"]["details"]["device"]["macAddress"] = dev["mac"]
            body["enrichmentInfo"]["details"]["device"]["hostname"] = dev["hostname"]
            body["enrichmentInfo"]["details"]["device"]["node"] = dev["serial"]
            body["enrichmentInfo"]["details"]["device"]["softwareVersion"] = dev["swVersion"]
            body["enrichmentInfo"]["details"]["device"]["productId"] = dev["pid"]
            body["enrichmentInfo"]["details"]["eol"]["announceDate"] = self.date_format(int(dev["hweol"]["externalAnnounceDate"]))
            body["enrichmentInfo"]["details"]["eol"]["eoSaleDate"] = self.date_format(int(dev["hweol"]["hweoxEndOfSaleDate"]))
            body["enrichmentInfo"]["details"]["eol"]["eoSupportDate"] = self.date_format(int(dev["hweol"]["hweoxLastSupportDate"]))
            body["enrichmentInfo"]["details"]["eol"]["MigrationPid"] = dev["hweol"]["migrationPidInfo"][0]["migrationPid"]
        elif(type == "PSIRT"):
            body = json.loads(PSIRT_EVENT_POST_BODY)
            body["id"] = str(eventid)
            body["enrichmentInfo"]["details"]["device"]["macAddress"] = dev["mac"]
            body["enrichmentInfo"]["details"]["device"]["hostname"] = dev["hostname"]
            body["enrichmentInfo"]["details"]["device"]["node"] = dev["serial"]
            body["enrichmentInfo"]["details"]["device"]["softwareVersion"] = dev["swVersion"]
            body["enrichmentInfo"]["details"]["device"]["productId"] = dev["pid"]
            body["enrichmentInfo"]["details"]["psirts"] = dev["psirts"]
        elif(type == "TEST"):
            body = json.loads(TEST_EVENT_POST_BODY)
            body["id"] = str(eventid)
        # Add Extra BAPI name header
        headers = {"__bapiName" :ITSM_BAPI_NAME,"end_system": ITSM_SYSTEM_NAME,"X-AUTH-TOKEN" : self.authtoken }
        self.sess.headers = headers
        r = self.sess.post(DNACAAP_ITSM_POST_API.format(self.ip,eventid), headers=self.sess.headers,  json=body, verify=False)
        if r.status_code == 202:
            itsm_resp = r.json()
            return itsm_resp["message"]
        else:
            return "No ITSM"
            sys.exit(1)
