# -*- coding: utf-8 -*-
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def download_htmls(username=None, password=None, url=None):
    if url is None:
        url = "https://ps.acsd1.org/guardian/home.html"

    # Possible grades to find correct hyperlinks
    possible_grades = ("A", "B", "C", "D", "F")
    grade_pages = []
    html_data = []

    # Headless options
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)

    # Switch to new URL
    driver.get(url)

    # Find Username, password, and button
    uname = driver.find_element_by_name("account")
    pword = driver.find_element_by_name("pw")
    button = driver.find_element_by_id("btn-enter-sign-in")

    # Substitite with Username and Password
    uname.send_keys(username)
    pword.send_keys(password)

    # Submit
    button.click()

    try:
        driver.find_element_by_class_name("feedback-alert")
        print("Invalid Username or Password")
        sys.exit(1)
    except NoSuchElementException:
        pass
        # print("Successfully Logged in...")

    # Find the right hyperlinks.
    class_pages = driver.find_elements_by_class_name("bold")
    for i in class_pages:
        if str(i.text)[0] in possible_grades:
            grade_pages.append(i)

    # Iterate through all class pages and save HTML
    for i in grade_pages:
        # Open and switch to new tab
        i.send_keys(Keys.CONTROL + Keys.RETURN)
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])

        # Wait till element loads, prevents incomplete page downloads
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ng-binding"))
            )
        # Timeout of 10 seconds
        except TimeoutException:
            print("Loading took too long!")
            sys.exit(0)

        # Save the source to memory
        html_data.append(driver.page_source.encode("utf-8").strip())

        # Cleanup, switch back to main tab
        driver.switch_to.window(driver.window_handles[0])

    # Kill main window
    driver.close()

    # print("Done grabbing HTMLs")
    return html_data
