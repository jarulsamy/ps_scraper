import web_driver
import process_html
import getpass
import argparse
import os
import sys
from pyfiglet import Figlet
from guiUtils import Spinner, HiddenPrints

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output_dir", required=False,
                help="Output path of Excel Doc", default="Grades.xlsx")

ap.add_argument("-u", "--username", required=False,
                help="Specify user as argument to circumvent prompt, must use -p")

ap.add_argument("-p", "--password", required=False,
                help="Specify password as argument")

ap.add_argument("-url", "--url", required=False,
                help="Specify custom URL for Powerschool, probably won't work :P")
args = vars(ap.parse_args())

f = Figlet()
print(f.renderText("Powerschool\nScraper"))
print(f.renderText(""))

if args['username'] is None:
    print("Please enter your Powerschool Username and Password")
    print("When entering a password, no characters will show.")
    user = input("Username: ")
else:
    user = args['username']
if args['password'] is None:
    pass_ = getpass.getpass()
else:
    pass_ = args['password']


with Spinner():
    html_data = web_driver.download_htmls(
        username=user,
        password=pass_,
        url=args["url"]
    )
    process_html.gen_excel(html_data, args["output_dir"])

print("\nDone!")
sys.exit(0)
