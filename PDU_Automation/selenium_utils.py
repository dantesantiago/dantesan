# 2022 - PANDUIT
#      - PDU Webpage : Selenium python utilities
#      - by dantesan-sada--2022-08-31

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import time
from inspect import currentframe, getframeinfo
import sys, os

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import pdu_webpage_class
from pdu_webpage_class import PDU_WEBPAGE_CLASS


from ..page_objects.pdu_summary_wp import CHANGE_PASSWORD
from ..page_objects.pdu_summary_wp import USER_ACCOUNTS
# show this is another way to import
from pdu_py_sel.page_objects.pdu_summary_wp import LOG_OUT 

from automation_utils import write_log
from automation_utils import debug_func

import automation_utils
from automation_utils import CONTINUE_MSG
from automation_utils import MONITORED_LCTR
from automation_utils import USERNAME_ID_LCTR
from automation_utils import PASSWORD_ID_LCTR
from automation_utils import LOGIN_BTTN_LCTR
from automation_utils import CONTINUE_MSG_LCTR
from automation_utils import CONTINUE_MSG_OK_LCTR


ID = "id"
CSS = "css"
XPATH = "xpath"
LINK_TEXT = "link_text"
PARTIAL_LINK_TEXT = "partial_link_text"
NAME = "name"
TAG_NAME = "tag_name"
CLASS_NAME = "class_name"


def open_webpage(driver, pdu_webpage_obj):
    
    write_log("{0} ... as named ...".format(open_webpage.__name__))
    automation_pdu_wp = "https://{0}/#/login?_k=f4wu0l".format(pdu_webpage_obj.ip_address())
    driver.get(automation_pdu_wp)
    #assert AUTOMATION_PDU_TITLE in driver.title
    # maximize window
    driver.maximize_window()
    # set window size
    #driver.(1525, 600)  
    #time.sleep(3)


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
        try:
            WebDriverWait(driver, 30).until(EC.visibility_of_element_located((find_by, element_by)))
        except:
            write_log("{0} - NoneTypeError FIND_BY: {1}, LOCATOR: {2}"
                .format(wait_and_get_elem_by.__name__, find_by, element_by))
            return None

    if find_by == By.ID:
        element_name = driver.find_element(ID, element_by)
    elif find_by == By.CSS_SELECTOR:
        element_name = driver.find_element(CSS, element_by)
    elif find_by == By.XPATH:
        element_name = driver.find_element(XPATH, element_by)
    elif find_by == By.LINK_TEXT:
        element_name = driver.find_element(LINK_TEXT, element_by)
    elif find_by == By.PARTIAL_LINK_TEXT:
        element_name = driver.find_element(PARTIAL_LINK_TEXT, element_by)
    elif find_by == By.NAME:
        element_name = driver.find_element(NAME, element_by)
    elif find_by == By.TAG_NAME:
        element_name = driver.find_element(TAG_NAME, element_by)
    elif find_by == By.CLASS_NAME:
        element_name = driver.find_element(CLASS_NAME, element_by)

    # move mouse over 
    ActionChains(driver).move_to_element(element_name).perform()
    return element_name


#
# Function name: check_xpath_exists
#
# https://stackoverflow.com/questions/9567069/checking-if-element-exists-with-python-selenium
#
# Check if the webelement given the xpath exists.
#
# dantesan--sada--20022-09-13 
#
# driver - the WbDriver
# xpath = The xpath to check 
#
# returns True, if existing, and False, if bot.
#  
def check_xpath_exists(driver, xpath):
    try:
        driver.find_element(XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


# To bypass WebDriverWait() - set dont_wait = True ... or False or anything!
def wait_and_get_elements_by(driver, find_by, element_by, dont_wait = None):
    
    if dont_wait == None:
        try:
            WebDriverWait(driver,30).until(EC.visibility_of_element_located((find_by, element_by)))
        except:
            write_log("{0} - NoneTypeError FIND_BY: {1}, LOCATOR: {2}"
                .format(wait_and_get_elements_by.__name__, find_by, element_by))
            return None

    if find_by == By.ID:
        element_names = driver.find_elements(ID, element_by)
    elif find_by == By.CSS_SELECTOR:
        element_names = driver.find_elements(CSS, element_by)
    elif find_by == By.XPATH:
        element_names = driver.find_elements(XPATH, element_by)
    elif find_by == By.LINK_TEXT:
        element_names = driver.find_elements(LINK_TEXT, element_by)
    elif find_by == By.PARTIAL_LINK_TEXT:
        element_names = driver.find_elements(PARTIAL_LINK_TEXT, element_by)
    elif find_by == By.NAME:
        element_names = driver.find_elements(NAME, element_by)
    elif find_by == By.TAG_NAME:
        element_names = driver.find_elements(TAG_NAME, element_by)
    elif find_by == By.CLASS_NAME:
        element_names = driver.find_elements(CLASS_NAME, element_by)

    # move mouse over 
    #ActionChains(driver).move_to_element(element_name).perform()
    return element_names


# Verify element/s is/are invisible. - dantesan--sada--20022-09-21
#
# verify_element_invisible
#
# driver  - WebDriver
# find_by - which BY to use - see wait_and_get_elem_by()
# element_lctr - element locator, the value of the BY locator
#
# Returns True if element is invisible. 
#
def verify_element_invisible(driver, find_by, element_by):

    invisible = True
    try:
       WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((find_by, element_by)))
    except:
        write_log("{0} - Invisiblity check failed! FIND_BY: {1}, LOCATOR: {2}"
           .format(verify_element_invisible.__name__, find_by, element_by))
        invisible = False

    return invisible


# Verify element/s is/are visible. - dantesan--sada--20022-09-22
#
# verify_element_visible
#
# driver  - WebDriver
# find_by - which BY to use - see wait_and_get_elem_by()
# element_lctr - element locator, the value of the BY locator
#
# Returns True if element is visible. 
#
def verify_element_visible(driver, find_by, element_by):
    
    visible = True
    try:
       WebDriverWait(driver, 3).until(EC.visibility_of_element_located((find_by, element_by)))
    except:
        write_log("{0} - Visiblity check failed! FIND_BY: {1}, LOCATOR: {2}"
           .format(verify_element_invisible.__name__, find_by, element_by))
        visible = False

    return visible


def get_fn():
    cf = currentframe()
    filename = getframeinfo(cf.f_back).filename
    return(filename)


def get_lineno():
    cf = currentframe()
    return(cf.f_back.f_lineno)


# enter text - dantesan--sada--20022-09-08
#
# Enter a text into the textbox given the BY locator.
#
# driver  - WebDriver
# find_by - which BY to use - see wait_and_get_elem_by()
# element_lctr - element locator, the value of the BY locator
# new_text - the text to write in the textbox 
#
# Returns the webelement. 
#
def enter_text(driver, find_by, element_lctr, new_text):
    textbox = wait_and_get_elem_by(driver, find_by, element_lctr)
    try:
        textbox.click()
        textbox.send_keys(Keys.HOME)
        textbox.send_keys(new_text)
    except:
        write_log("{0} - NoneTypeError XPATH: {1}".format(enter_text.__name__, element_lctr))
    return textbox


# click the button - dantesan--sada--20022-09-08
# 
# Click the button identified or located by the BY element locator.
#
# driver  - WebDriver
# find_by - which BY to use - see wait_and_get_elem_by()
# element_lctr - element locator, the value of the BY locator
#
# returns the webelement 
#
# new_text - Later, use if label should change after clicking.
def click_button(driver, find_by, element_lctr, new_text=None ):
    button = wait_and_get_elem_by(driver, find_by, element_lctr)

    try:
        button.click()
    except:
        write_log("{0} - NoneTypeError XPATH: {1}".format(click_button.__name__, element_lctr))

    return button


#
# Function name: click_dropdown_item
#                (click_username_drpdwn_item)
#
# Click the username button menu item.
#
# dantesan--sada--20022-09-09 
#
# driver  - WebDriver
# item_text - the item text
#
# returns the webelement
#  
def click_dropdown_item(driver, item_text):
    menu_item_xpath = "//a/span[text() = '{0}']".format(item_text)
    menu_item_we = wait_and_get_elem_by(driver, XPATH, menu_item_xpath)

    try:
        menu_item_we.click()
    except:
        write_log("{0} - NoneTypeError Menu Item Name: {1}".format(click_dropdown_item.__name__, item_text))

    return menu_item_we


# click the button given its name. - dantesan--sada--20022-09-14
# 
# click_named_button
#
# driver  - WebDriver
# button_name - the button name
#
# returns the webelement 
#
#
def click_named_button(driver, button_name):
    button_xpath = "//span[text() = '{0}']".format(button_name)
    button = wait_and_get_elem_by(driver, XPATH, button_xpath)

    try:
        button.click()
    except:
        write_log("{0} - NoneTypeError Button Name: {1}".format(click_named_button.__name__, button_name))

    return button


# Verify Label exists. - dantesan--sada--20022-10-05
# 
# verify_span_label
#
# driver  - WebDriver
# label_str - the label 
#
# returns the webelement 
#
#
def verify_span_label(driver, label_str):
    label_xpath = "//span[text() = '{0}']".format(label_str)

    try:
        label = wait_and_get_elem_by(driver, XPATH, label_xpath)
    except:
        write_log("{0} - NoneTypeError Label Name: {1}".format(verify_span_label.__name__, label_str))

    return label


# 
# Click item menu that has no 'span'.
#
# click_a_dropdown_item
#
# dantesan--sada--20022-09-14 
#
# driver  - WebDriver
# item_text - the item text
#
# returns the webelement
#  
def click_a_dropdown_item(driver, item_text):
    menu_item_xpath = "//a[text() = '{0}']".format(item_text)
    menu_item_we = wait_and_get_elem_by(driver, XPATH, menu_item_xpath)

    try:
        menu_item_we.click()
    except:
        write_log("{0} - NoneTypeError Menu Item Name: {1}"
            .format(click_a_dropdown_item.__name__, item_text))

    return menu_item_we


# Click the icon or button given its aria-label. - dantesan--sada--20022-09-21
# 
# click_aria_label_icon
#
# driver  - WebDriver
# aria_label - the button aria-label
#
# returns the webelement, if it exists!
#
#
def click_aria_label_icon(driver, aria_label):
    button_xpath = "//*[local-name()='svg' and @aria-label='{0}']".format(aria_label)
    try:
        icon_button = wait_and_get_elem_by(driver, XPATH, button_xpath)
        icon_button.click()
            
    except:
        write_log("{0} - NoneTypeError Icon with aria label: {1}"
            .format(click_aria_label_icon.__name__, aria_label))

    return icon_button


# Close Chrome. - dantesan--sada--2022-10-05
#   
# - moved from rack_access_control_test.py ...
# close_Chrome
#
# the driver
#
# returns - None
#
def close_Chrome(driver):
    driver.quit()
    write_log("END: {0} - Chromedriver quits.".format(__name__))
    sys.exit()


# Function name: click_svg_icon
#
# Click the icons or svgs given the aria-label.
#
# dantesan--sada--20022-09-13 
#
# driver  - WebDriver
# aria_label - the aria label
#
# returns the svg webelement
#  
def click_svg_icon(driver, aria_label):
    svg_icon_xpath = "//*[local-name()='svg' and @aria-label = '{0}']".format(aria_label)
    #svg_icon_we = wait_and_get_elem_by(driver, XPATH, svg_icon_xpath)
    try:
        svg_icon_we = click_button(driver, XPATH, svg_icon_xpath)
    except:
         write_log("{0} - NoneTypeError SVG Icon with aria label: {1}"
             .format(click_svg_icon.__name__, aria_label))
    return svg_icon_we


# Function name: login_pdu()
#
# Log in to the PDU webpage.
#
# dantesan--sada--20022-10-06   
#  - from open_log_io_pdu.py (not used) 
#
# driver  - WebDriver
#
#  
def login_pdu(driver):
    #pdu_webpage_class = pdu_webpage_class.PDU_WEBPAGE_CLASS()    #Will work, but better to be explicit. Did not work!
    ip_addr = PDU_WEBPAGE_CLASS.IP_ADDRESS
    usrnm = PDU_WEBPAGE_CLASS.USERNAME
    passwd = PDU_WEBPAGE_CLASS.PASSWD
    wp_str = PDU_WEBPAGE_CLASS.WEBPAGE_STRING

    pdu_wp_obj = PDU_WEBPAGE_CLASS(ip_address = ip_addr, username = usrnm, 
                                    password = passwd, webpage_string = wp_str)

    write_log("START: {0} - open PDU webpage.".format(__name__))
    open_webpage(driver, pdu_wp_obj)

    # Verify PDU webpage
    mon_and_switched_per_outlet = wait_and_get_elem_by(driver, By.XPATH, MONITORED_LCTR)
    assert(pdu_wp_obj.webpage_string() == mon_and_switched_per_outlet.text)

    username = enter_text(driver, By.ID, 
                           USERNAME_ID_LCTR, pdu_wp_obj.username())
    
    password = enter_text(driver, By.ID, 
                           PASSWORD_ID_LCTR, pdu_wp_obj.password())

    write_log("{0} - Press Login button.".format(__name__))
    login_bttn = click_button(driver, By.XPATH, LOGIN_BTTN_LCTR)

    time.sleep(5)

    # dantesan-sada--2022-09-13 - check if CONTINUE_MSG appears.
    if check_xpath_exists(driver, CONTINUE_MSG_LCTR):
        click_button(driver, By.XPATH, CONTINUE_MSG_OK_LCTR)
        write_log("{0} - CONTINUE_MSG_OK pressed.".format(__name__))

    time.sleep(5)


# Function name: logout_pdu()
#
# Log out of the PDU webpage.
#
# dantesan--sada--20022-10-06   
#  - from open_log_io_pdu.py (not used) 
#
# driver  - WebDriver
#
# 
def logout_pdu(driver):

    usrnm = PDU_WEBPAGE_CLASS.USERNAME
    # press username menu
    username_bttn = click_username(driver, usrnm)
    write_log("{0} - username pressed.".format(__name__))

    # logout
    log_out_we = click_dropdown_item(driver, LOG_OUT)
    write_log("{0} - Log Out clicked.".format(__name__))
    time.sleep(5)

    driver.quit()
    write_log("END: {0} - Chromedriver quits.".format(__name__))


#
# Function name: click_username
# 
# Click the username button.
#
# dantesan--sada--20022-09-09 
#
# driver  - WebDriver
# username - PDU_WEBPAGE_CLASS_OBJ.username()
#
# returns the username button or webelement
#
# DT221012 - Moved from pdu_summary_wp.py.
#  
def click_username(driver, username):
    username_xpath = "//button/span[text() = '{0}']".format(username)
    username_bttn = click_button(driver, XPATH, username_xpath)
    return username_bttn


#---------------------------------- END -------------------------------------
