# 2022 - PANDUIT
#      - PDU Webpage : Selenium python utilities
#      - by dantesan-sada--2022-08-31

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import pdu_py_sel.utils.selenium_utils
from pdu_py_sel.utils.selenium_utils import open_webpage
from pdu_py_sel.utils.selenium_utils import wait_and_get_elem_by
from pdu_py_sel.utils.selenium_utils import enter_text
from pdu_py_sel.utils.selenium_utils import click_button
from pdu_py_sel.utils.selenium_utils import check_xpath_exists
from pdu_py_sel.utils.selenium_utils import click_dropdown_item

from pdu_py_sel.page_objects.pdu_summary_wp import click_username

from pdu_py_sel.page_objects.pdu_summary_wp import CHANGE_PASSWORD
from pdu_py_sel.page_objects.pdu_summary_wp import USER_ACCOUNTS
from pdu_py_sel.page_objects.pdu_summary_wp import LOG_OUT

from pdu_py_sel.utils.ssh_utils import run_command


import pdu_py_sel.utils.pdu_webpage_class 
from pdu_py_sel.utils.pdu_webpage_class import PDU_WEBPAGE_CLASS

# dantesan--sada--2022-09-28
import pdu_py_sel.utils.automation_utils
from pdu_py_sel.utils.automation_utils import CONTINUE_MSG
from pdu_py_sel.utils.automation_utils import MONITORED_LCTR
from pdu_py_sel.utils.automation_utils import USERNAME_ID_LCTR
from pdu_py_sel.utils.automation_utils import PASSWORD_ID_LCTR
from pdu_py_sel.utils.automation_utils import LOGIN_BTTN_LCTR
from pdu_py_sel.utils.automation_utils import CONTINUE_MSG_LCTR
from pdu_py_sel.utils.automation_utils import CONTINUE_MSG_OK_LCTR

from pdu_py_sel.utils.automation_utils import write_log
from pdu_py_sel.utils.automation_utils import debug_func


#driver = webdriver.Firefox()

chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('ignore-certificate-errors')
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)


def get_driver():
    return driver

if __name__ == "__main__":

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

    # press username menu
    username_bttn = click_username(driver, usrnm)
    write_log("{0} - username pressed.".format(__name__))

    time.sleep(5)

    # logout
    log_out_we = click_dropdown_item(driver, LOG_OUT)
    write_log("{0} - Log Out clicked.".format(__name__))
    time.sleep(5)

    driver.quit()
    write_log("END: {0} - Chromedriver quits.".format(__name__))

#----------------------------------- END --------------------------------
