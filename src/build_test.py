import web_driver
import process_html
import os
from subprocess import Popen, PIPE

ret = os.system(
    f"python main.py --username {os.getenv('test_user')} --password {os.getenv('test_password')}")
if ret != 0:
    raise Exception("Failed Test!")
