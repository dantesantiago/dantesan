# 2019 - Cigent Technology, Inc.
#      - MSP D3E Subscription: Selenium python utilities
#      - by dantesan

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

import time

from inspect import currentframe, getframeinfo

def open_mgmt_console_subs(driver):
    driver.get("https://mgmt-console-dev.cigent.com/subscriptions/d3e")
    #assert "Management Console" in driver.title
    assert "Central Console" in driver.title
    # maximize window
    #driver.maximize_window()
    # set window size
    driver.set_window_size(1525, 600)
    time.sleep(3)


def wait_and_get_element(driver, element_by_css):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, element_by_css)))
    element_name = driver.find_element_by_css_selector(element_by_css)
    element_name.send_keys(Keys.NULL)
    # move mouse over 
    ActionChains(driver).move_to_element(element_name).perform()
    return element_name


def wait_and_get_label(driver, css_selector):
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
    element_name = driver.find_element_by_css_selector(css_selector)
    # move mouse over 
    ActionChains(driver).move_to_element(element_name).perform()
    print(element_name.text)
    return element_name


# To bypass WebDriverWait() - set dont_wait = True ... or False or anything!
def wait_and_get_elem_by(driver, find_by, element_by, dont_wait = None):

    if dont_wait == None:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((find_by, element_by)))

    if find_by == By.ID:
        element_name = driver.find_element_by_id(element_by)
    elif find_by == By.CSS_SELECTOR:
        element_name = driver.find_element_by_css_selector(element_by)
    elif find_by == By.XPATH:
        element_name = driver.find_element_by_xpath(element_by)
    elif find_by == By.LINK_TEXT:
        element_name = driver.find_element_by_link_text(element_by)
    elif find_by == By.PARTIAL_LINK_TEXT:
        element_name = driver.find_element_by_partial_link_text(element_by)
    elif find_by == By.NAME:
        element_name = driver.find_element_by_name(element_by)
    elif find_by == By.TAG_NAME:
        element_name = driver.find_element_by_tag_name(element_by)
    elif find_by == By.CLASS_NAME:
        element_name = driver.find_element_by_class_name(element_by)

    # move mouse over 
    ActionChains(driver).move_to_element(element_name).perform()
    return element_name


# To bypass WebDriverWait() - set dont_wait = True ... or False or anything!
def wait_and_get_elements_by(driver, find_by, element_by, dont_wait = None):
    
    if dont_wait == None:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((find_by, element_by)))

    if find_by == By.ID:
        element_name = driver.find_elements_by_id(element_by)
    elif find_by == By.CSS_SELECTOR:
        element_name = driver.find_elements_by_css_selector(element_by)
    elif find_by == By.XPATH:
        element_name = driver.find_elements_by_xpath(element_by)
    elif find_by == By.LINK_TEXT:
        element_name = driver.find_elements_by_link_text(element_by)
    elif find_by == By.PARTIAL_LINK_TEXT:
        element_name = driver.find_elements_by_partial_link_text(element_by)
    elif find_by == By.NAME:
        element_name = driver.find_elements_by_name(element_by)
    elif find_by == By.TAG_NAME:
        element_name = driver.find_elements_by_tag_name(element_by)
    elif find_by == By.CLASS_NAME:
        element_name = driver.find_elements_by_class_name(element_by)

    # move mouse over 
    #ActionChains(driver).move_to_element(element_name).perform()
    return element_name


def get_fn():
    cf = currentframe()
    filename = getframeinfo(cf.f_back).filename
    return(filename)


def get_lineno():
    cf = currentframe()
    return(cf.f_back.f_lineno)


#---------------------------------- END -------------------------------------
