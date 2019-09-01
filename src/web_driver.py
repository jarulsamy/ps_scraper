from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from sys import exit as e
import os

def download_htmls(username=None, password=None, output=None):
    if output == None:
        output = Path("Downloads")

    if not os.path.exists(str(output)):
        os.makedirs(str(output))

    # Possible grades to find correct Hyperlinks
    possible_grades = "A B C D F"
    grade_pages = []

    # Headless options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('log-level=3')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    # Switch to new URL
    url = "https://ps.acsd1.org/guardian/home.html"
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
        e()
    except NoSuchElementException:
        print("Successfully Logged in...")

    # Find the right hyperlinks.
    class_pages = driver.find_elements_by_class_name("bold")
    for i in class_pages:
        if str(i.text)[0] in possible_grades:
            grade_pages.append(i)

    # Iterate through all class pages and download HTMLs
    for i in grade_pages:
        file_name = Path(str(grade_pages.index(i)) + ".html")
        print(f"Writing {file_name}...")
        total_path = str(output / file_name)
        f = open(total_path, "wb")

        # Open and switch to new tab
        i.send_keys(Keys.CONTROL + Keys.RETURN)
        driver.switch_to.window(driver.window_handles[-1])
        
        # Wait till element loads, prevents incomplete page downloads
        try:
            time_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ng-binding')))
        # Timeout of 10 seconds
        except TimeoutException:
            print("Loading took too much time!")
            print("Likely an internet issue!")
            e()

        # Save the source to file
        f.write(driver.page_source.encode('utf-8').strip())
        driver.close()

        # Cleanup, switch back to main tab
        driver.switch_to.window(driver.window_handles[0])
        f.close()

    # Kill main window
    driver.close()

    print("Done grabbing HTMLs")
