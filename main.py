import web_driver
import process_html
import cred

web_driver.download_htmls(username=cred.username, password=cred.password)

process_html.gen_excel()
