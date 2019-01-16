import web_driver
import process_html
import getpass
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output_dir", required=False,
                help="Output directory of HTML files")

args = vars(ap.parse_args())

try:
    user = input("Username: ")
    pass_ = getpass.getpass()
    web_driver.download_htmls(username=user, password=pass_, output=args['output_dir'])
    process_html.gen_excel(path=args['output_dir'])
except Exception as error:
    print('ERROR', error)
    exit(0)
