import base64
import hashlib
import hmac
import re

import requests


class Powerschool(object):
    def __init__(self, uname, pword, url=None):
        super().__init__()

        if url is None:
            url = "https://ps.acsd1.org/"

        self.uname = uname
        self.pword = pword
        self.url = url
        self.session = requests.session()
        self.auth()

    def _getAuthData(self):
        r = self.session.get(self.url)

        if r.status_code != requests.codes.ok:
            raise Exception("Unable to retrieve authentication tokens from PS server.")

        self.auth_data = {}

        pstoken = re.search(
            r'<input type="hidden" name="pstoken" value="(.*?)" \/>', r.text, re.S
        )
        self.auth_data["pstoken"] = pstoken.groups()[0]

        contextData = re.search(
            r'<input type="hidden" name="contextData" value="(.*?)" \/>', r.text, re.S
        )
        self.auth_data["contextData"] = contextData.groups()[0]

        if "<input type=hidden name=ldappassword value=''>" in r.text:
            self.auth_data["ldap"] = True
        else:
            self.auth_data["ldap"] = False

    def auth(self):
        self._getAuthData()

        dbpw = hmac.new(
            self.auth_data["contextData"].encode("ascii"),
            self.pword.lower().encode("ascii"),
            hashlib.md5,
        ).hexdigest()
        pw = hmac.new(
            self.auth_data["contextData"].encode("ascii"),
            base64.b64encode(hashlib.md5(self.pword.encode("ascii")).digest()).replace(
                b"=", b""
            ),
            hashlib.md5,
        ).hexdigest()

        fields = {
            "pstoken": self.auth_data["pstoken"],
            "contextData": self.auth_data["contextData"],
            "dbpw": dbpw,
            "serviceName": "PS Parent Portal",
            "pcasServerUrl": "/",
            "credentialType": "User Id and Password Credential",
            "account": self.uname,
            "pw": pw,
        }

        if self.auth_data["ldap"]:
            fields["ldappassword"] = self.pword

        r = self.session.post(self.url + "guardian/home.html", data=fields)

        if u"Grades and Attendance" not in r.text:
            pserror = re.search(
                r'<div class="feedback-alert">(.*?)<\/div>', r.text, re.S
            )

            if pserror:
                raise Exception(pserror.groups()[0])
            else:
                raise Exception("Unable to login to PS server.")
        else:
            print(r.text)
            # return user(self, r.text)
