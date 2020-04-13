import re

import requests
from bs4 import BeautifulSoup


class Powerschool(object):
    def __init__(self, uname, pword, url=None):
        super().__init__()

        if url is None:
            url = "https://ps.acsd1.org/"
        elif url[-1] != "/":
            url += "/"

        self.uname = uname
        self.pword = pword

        self.url = url
        self.homepage = url + "guardian/home.html"
        self.base_url = url + "guardian/"

        self.session = requests.session()
        self.auth()
        self._get_hyperlinks()

    def auth(self):

        auth_data = {
            "dbpw": self.pword,
            "translator_username": "",
            "translator_password": "",
            "translator_ldappassword": "",
            "returnUrl": "",
            "serviceName": "PS Parent Portal",
            "serviceTicket": "",
            "pcasServerUrl": "/",
            "credentialType": "User Id and Password Credential",
            "ldappassword": self.pword,
            "request_locale": "en_US",
            "account": self.uname,
            "pw": self.pword,
            "translatorpw": "",
        }

        r = self.session.post(self.homepage, auth_data)

        if u"Grades and Attendance" not in r.text:
            pserror = re.search(
                r'<div class="feedback-alert">(.*?)<\/div>', r.text, re.S
            )

            if pserror:
                raise Exception(pserror.groups()[0])
            else:
                raise Exception("Unable to login to PS server.")

    def _get_hyperlinks(self):
        r = self.session.get(self.homepage)
        soup = BeautifulSoup(r.text, features="lxml")

        self.grade_links = []
        for link in soup.find_all("a"):
            sub_link = link.get("href")
            if "scores" in sub_link and "begdate" in sub_link:
                real_link = self.base_url + sub_link
                self.grade_links.append(real_link)
