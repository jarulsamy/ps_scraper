import web_driver
import process_html
import getpass
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output_dir", required=False,
                help="Output directory of HTML files")

ap.add_argument("-u", "--username", required=False,
                help="Specify user as argument to circumvent prompt")

ap.add_argument("-p", "--password", required=False,
                help="Specify password as argument, NOT SECURE - NOT RECOMMENDED")

ap.add_argument("-nc", "--no_cleanup", required=False,
                help="Don't auto delete HTMLs download folder")

args = vars(ap.parse_args())

try:

    print("Welcome to the Laramie High School Powerschool Scraper!")
    print("Maintained by: Joshua Arulsamy")
    print("Please enter your Powerschool Username and Password")
    print("By using this software, you are consenting to this software ")
    print("logging in as the credentials specified and downloading grade data.")
    print("Please Note: ABSOLUTELY NO private data is transmitted to third-parties or shared!")
    print("")
    print("When entering a password, no characters will show.")
    print("")

    if args['username'] == None:
        user = input("Username: ")
    else:
        user = args['username']

    if args['password'] == None:
        pass_ = getpass.getpass()
    else:
        pass_ = args['password']

    web_driver.download_htmls(username=user, password=pass_, output=args['output_dir'])
    process_html.gen_excel(path=args['output_dir'])
    process_html.cleanup(path=args['output_dir'])
    
    exit(0)

except Exception as error:
    print('ERROR', error)
    exit(0)
