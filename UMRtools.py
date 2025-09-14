
import argparse, logging, os, sys
import json, requests, yaml, ssl

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
        logger.debug("UMRrouter created: "+f"{self}")

    def __str__(self):
        return json.dumps(self.__dict__)

    def connect(self):
        try:
            response = requests.post("https://"+self.addr+"/ubus/call/session",
                data={"jsonrpc":"2.0","method":"login","params":{"username":"ui","password":self.password,"timeout":2129920}},
                headers={"Content-Type": "application/json; charset=utf-8", 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' },
                verify=False,
            )
        except ssl.SSLCertVerificationError:
            logger.error("SSL Certificate unsigned.")
        except OSError as err:
            # print(response.json())
            logger.error(err)
            self.authCode = -1
        else:
            print(response.json())
