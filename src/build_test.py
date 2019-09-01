import web_driver
import process_html
import os

print("Username: ", os.getenv("test_user"))

web_driver.download_htmls(username=os.getenv("test_user"), password=os.getenv("test_password"))
process_html.gen_excel()
process_html.cleanup(everything=True)
