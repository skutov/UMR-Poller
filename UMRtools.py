#! /usr/bin/env python3

import argparse, logging, os, sys
import json, requests, yaml, ssl
import http.client as httplib

logger = logging.getLogger(__name__)

class UMRrouter:
    """
        Router auth states:
        -1 - Error, not reachable
         0 - Initialised and not connected
        >0 - Logged in and authorised
    """
    def __init__(self, name, addr, password, freq, SSLVerify):
        self.name = name
        self.addr = addr
        self.password = password
        self.freq = freq
        self.SSLVerify = SSLVerify
        self.authCode = 0
        self.session = requests.Session()

        self.session.headers.update(
            {
                "Host": self.addr,
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0",
                "Accept": "*/*",
                "Accept-Language": "en-GB,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "content-type": "application/json; charset=utf-8",
                "Origin": f"https://{self.addr}",
                "DNT": "1",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Priority": "u=4",
            }
        )

        logger.debug("UMRrouter created: "+f"{self.name}")

    def __str__(self):
        return json.dumps(self.__dict__)

    def connect(self):
        try:
            response = self.session.post(
                "https://"+self.addr+"/ubus/call/session",
                headers={
                    "Referer": f"https://{self.addr}",
                    "Priority": "u=0",
                    "content-type": None,
                },
                json={
                    "jsonrpc":"2.0",
                    "method":"login",
                    "params":{
                        "username":"ui",
                        "password":self.password,
                        "timeout":2129920
                    }
                },
                verify=self.SSLVerify
            )

        except ssl.SSLCertVerificationError:
            logger.error("SSL Certificate unsigned.")
        except httplib.BadStatusLine:
            logger.error("Bad Status Line received")
            print(response.request.url)
            print(response.request.body)
            print(response.request.headers)
        except OSError as err:
            # print(response.json())
            logger.error(err)
            self.authCode = -1
        else:
            auth = "Bearer " + response.json()["result"]["ubus_rpc_session"]
            self.session.headers.update({"authorization": auth})
            logger.info("Login to "+self.name+" successful, auth id: "+auth)

    def getDeviceStatus(self):
        try:
            response = self.session.post(
                "https://"+self.addr+"/ubus/call/uimqtt",
                headers={
                    "Referer": f"https://{self.addr}",
                    "Priority": "u=0",
                    "content-type": None,
                },
                json={
                    "jsonrpc":"2.0",
                    "method":"GetDeviceStatus",
                    "params":{
                    }
                },
                verify=self.SSLVerify
            )

        except ssl.SSLCertVerificationError:
            logger.error("SSL Certificate unsigned.")
        except httplib.BadStatusLine:
            logger.error("Bad Status Line received")
            print(response.request.url)
            print(response.request.body)
            print(response.request.headers)
        except OSError as err:
            # print(response.json())
            logger.error(err)
            self.authCode = -1
        else:
            logger.info("GetDeviceStatus to "+self.name+" successful, result:"+f"{response.json()}")
