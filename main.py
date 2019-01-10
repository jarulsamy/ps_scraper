from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

possible_grades = "A B C D F"
grade_pages = []

driver = webdriver.Chrome()
website = driver.get("https://ps.acsd1.org/public/")

time.sleep(2)

uname = driver.find_element_by_name("account")
pword = driver.find_element_by_name("pw")
button = driver.find_element_by_id("btn-enter-sign-in")
# button = driver.find_element_by_class_name("submit")

time.sleep(0.5)

uname.send_keys("*")
pword.send_keys("*")

time.sleep(0.3)

button.click()

time.sleep(1)
url = "https://ps.acsd1.org/guardian/home.html"
driver.get(url)

def gen_pages():
    grade_pages = []
    class_pages = driver.find_elements_by_class_name("bold")
    for i in class_pages:
        if str(i.text)[0] in possible_grades:
            grade_pages.append(i)
    
    return grade_pages


# f = open("grades.html", "w")
grade_pages = gen_pages()

for i in grade_pages:
    f = open("Downloads/" + str(grade_pages.index(i)) + ".html", "w+")
    # i.click()
    i.send_keys(Keys.CONTROL + Keys.RETURN)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(5)
    f.write(driver.page_source.encode('utf-8').strip())
    driver.close()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
    # driver.execute_script("window.history.go(-1)")
    f.close()
    time.sleep(1)

time.sleep(.1)

driver.close()


# f.close()
