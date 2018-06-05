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
import sys
from requests.auth import HTTPBasicAuth


#Global variables
BASIC_AUTH_API = "https://{}/api/system/v1/identitymgmt/login"
DEVICES_API = "https://{}/api/v1/network-device/{}/{}"
DEVICE_CT_API = "https://{}/api/v1/network-device/count"

class Dnac_session:

#Login to DNAC
    def __init__(self,ip, user, pwd):
        self.sess = requests.Session()
        self.sess.cookie = {}
        self.ip = ip
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
                    self.sess.cookie[name] = value
                print("\n########### DNAC Login Successful ##########")
            else:
                print(r.content.decode("utf-8"))
                sys.exit(1)
        except requests.exceptions.ConnectionError:
            sys.exit('Unable to connect to Cluster')

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
