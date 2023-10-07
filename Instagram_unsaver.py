import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


options = Options


# ***For debugging uncomment this***
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)


def login(username, password):
    driver.get("https://www.instagram.com/")
    try:
        username_input = WebDriverWait(driver, timeout=15).until(lambda d: driver.find_element(By.XPATH, "//*[@id='loginForm']/div/div[1]/div/label/input"))
        password_input = WebDriverWait(driver, timeout=15).until(lambda d: driver.find_element(By.XPATH, "//*[@id='loginForm']/div/div[2]/div/label/input"))
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button = WebDriverWait(driver, timeout=5).until(lambda d: driver.find_element(By.XPATH, "//*[@id='loginForm']/div/div[3]/button/div"))
        login_button.click()
        time.sleep(3)
    except Exception as err:
        print("**Error has Occurred**\n", "Error: ", err)
        driver.quit()


def click_first_post():
    driver.get("https://www.instagram.com/utahsveryown/saved/all-posts/")
    try:
        t = WebDriverWait(driver, timeout=10).until(lambda d: driver.find_elements(By.CLASS_NAME, "_aagw"))
        t[0].click()
    except Exception as err:
        print("**Couldn't find first post**\n", "Error: ", err)
        driver.quit()


def erase_all(username):
    posts_unsaved = 0
    click_first_post()
    try:
        next_button = WebDriverWait(driver, timeout=5).until(lambda d: driver.find_element(By.CLASS_NAME, "_abl-"))
        unsave_div = WebDriverWait(driver, timeout=5).until(lambda d: driver.find_element(By.CLASS_NAME, "_aamz"))
        unsave_button = WebDriverWait(driver, timeout=5).until(lambda d: unsave_div.find_element(By.CLASS_NAME, "x1lliihq.x1n2onr6"))
        unsave_button.click()
        next_button.click()
        posts_unsaved += 1
        print("Erased: " + str(posts_unsaved))
    except Exception as err:
        print("**Couldn't find next post**\n", "Error: ", err)
        driver.quit()
    while True:
        try:
            next_button = driver.find_element(By.CLASS_NAME, "_aaqg._aaqh")
            unsave_div = driver.find_elements(By.CLASS_NAME, "_aamz")
        except NoSuchElementException:  # unsave the last post
            last_unsave_button = driver.find_elements(By.CLASS_NAME, "x6s0dn4.x78zum5.xdt5ytf.xl56j7k")
            last_unsave_button[4].click()
            posts_unsaved += 1
            print("Erased: " + str(posts_unsaved))
            print("Done")
            break
        for n in unsave_div:
            unsave_button = n.find_element(By.CLASS_NAME, "x1lliihq.x1n2onr6")
            unsave_button.click()
            time.sleep(.2)
            next_button.click()
            posts_unsaved += 1
            if posts_unsaved == 99:
                time.sleep(2)
            print("Erased: " + str(posts_unsaved))


def main():
    username = ""   #Enter your Username
    password = ""      #Enter your Password
    login(username, password)
    erase_all(username)
    driver.close()


main()