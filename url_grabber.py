from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import cred

driver = webdriver.Chrome()
website = driver.get("https://ps.acsd1.org/public/")

time.sleep(2)

# Find Username, password, and button
uname = driver.find_element_by_name("account")
pword = driver.find_element_by_name("pw")
button = driver.find_element_by_id("btn-enter-sign-in")

time.sleep(0.5)

# Substitite with Username and Password
uname.send_keys(cred.username)
pword.send_keys(cred.password)

time.sleep(0.3)

button.click()

time.sleep(1)

# Switch to new URL 
url = "https://ps.acsd1.org/guardian/home.html"
driver.get(url)

def gen_pages():

    # Possible grades to find correct Hyperlinks
    possible_grades = "A B C D F"
    grade_pages = []
    
    class_pages = driver.find_elements_by_class_name("bold")
    for i in class_pages:
        if str(i.text)[0] in possible_grades:
            grade_pages.append(i)
    
    return grade_pages


# f = open("grades.html", "w")
grade_pages = gen_pages()

for i in grade_pages:
    f = open("Downloads/" + str(grade_pages.index(i)) + ".html", "wb")

    # Open and switch to new tab
    i.send_keys(Keys.CONTROL + Keys.RETURN)
    driver.switch_to.window(driver.window_handles[-1])

    # Save the source to file
    time.sleep(5)
    f.write(driver.page_source.encode('utf-8').strip())
    driver.close()

    # Cleanup, switch back to main tab
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    f.close()
    time.sleep(1)

# Kill main window
time.sleep(.1)
driver.close()