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

ENVT = "ciscoactiveadvisor.com"
CAA_LOGIN_API = "https://{}/asi/api/auth/cco/login"
CAA_LC_API =  "https://{}/asi/api/csoq/lifecycle"


class Caa_session:
    # Login to CAA using CCO credentials
    def __init__(self,cco_json,to=10):
        self.authenticated = False
        self.sess = requests.Session()
        headers = {"Content-Type": "application/json"}
        s = self.sess.post(CAA_LOGIN_API.format(ENVT),json=cco_json,verify=False,headers=headers)
        if s.status_code == 200:
            try:
                json.loads(s.text)
            except:
                #Active advisor must be down
                print("Cannot access Cisco Active Advisor. Try again later")
                sys.exit(2)
            resp_json = json.loads(s.content.decode('utf-8'))
            self.token = resp_json['token']
            self.authenticated = True
        else:
            print(s.raise_for_status())

    # Get Lifecycle information from CAA
    def get_lc_info(self,post_params):
        headers = {"X-API-AUTH-TOKEN" : self.token,"Content-Type" :"application/json"}
        s = self.sess.post(CAA_LC_API.format(ENVT),data=json.dumps(post_params),verify=False,headers=headers)
        if s.status_code == 200:
            return(json.loads(s.text))
        else:
            print(s.raise_for_status())
