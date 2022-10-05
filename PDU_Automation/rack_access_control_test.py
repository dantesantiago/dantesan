# 2022 - PANDUIT
#      - Test: Rack Acces Control 
#      - by dantesan-sada--2022-08-31

import time
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

#import pdu_py_sel.utils.selenium_utils
from pdu_py_sel.utils.selenium_utils import open_webpage
from pdu_py_sel.utils.selenium_utils import wait_and_get_elem_by
from pdu_py_sel.utils.selenium_utils import enter_text
from pdu_py_sel.utils.selenium_utils import click_button
from pdu_py_sel.utils.selenium_utils import check_xpath_exists
from pdu_py_sel.utils.selenium_utils import click_dropdown_item

from pdu_py_sel.page_objects.pdu_summary_wp import click_username
from pdu_py_sel.page_objects.pdu_summary_wp import click_svg_icon

from pdu_py_sel.page_objects.pdu_summary_wp import CHANGE_PASSWORD
from pdu_py_sel.page_objects.pdu_summary_wp import USER_ACCOUNTS
from pdu_py_sel.page_objects.pdu_summary_wp import LOG_OUT

from pdu_py_sel.page_objects.pdu_summary_wp import AL_SETTINGS
from pdu_py_sel.page_objects.pdu_summary_wp import RACK_ACCESS_CONTROL


#import pdu_py_sel.utils.pdu_webpage_class 
from pdu_py_sel.utils.pdu_webpage_class import PDU_WEBPAGE_CLASS

#import pdu_py_sel.page_objects.rack_access_control_pobj
from pdu_py_sel.page_objects.rack_access_control_pobj import RAC_CLASS
from pdu_py_sel.page_objects.rack_access_control_pobj import create_card_data
from pdu_py_sel.page_objects.rack_access_control_pobj import delete_cards_with_dnd_list

from pdu_py_sel.utils.automation_utils import write_log
from pdu_py_sel.utils.automation_utils import debug_func


# dantesan--sada--2022-09-29
import pdu_py_sel.utils.automation_utils
from pdu_py_sel.utils.automation_utils import write_log
from pdu_py_sel.utils.automation_utils import debug_func

from pdu_py_sel.utils.automation_utils import CONTINUE_MSG
from pdu_py_sel.utils.automation_utils import MONITORED_LCTR
from pdu_py_sel.utils.automation_utils import USERNAME_ID_LCTR
from pdu_py_sel.utils.automation_utils import PASSWORD_ID_LCTR
from pdu_py_sel.utils.automation_utils import LOGIN_BTTN_LCTR
from pdu_py_sel.utils.automation_utils import CONTINUE_MSG_LCTR
from pdu_py_sel.utils.automation_utils import CONTINUE_MSG_OK_LCTR


# LOCATORS


#driver = webdriver.Firefox()

chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('ignore-certificate-errors')
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)


def get_driver():
    return driver


# Set the panel to Rack Access Control
#   Press settings icon -> Rack Access Control
#
# set_panel_to_RAC()
#
# no parameters
#
# returns - None
#
def set_panel_to_RAC():
    # select Settings
    click_svg_icon(driver, AL_SETTINGS)
    time.sleep(2)
    
    # click Rack Access Control
    rac_we = click_dropdown_item(driver, RACK_ACCESS_CONTROL)
    time.sleep(2)


# Close Chrome. - dantesan--sada--2022-10-05
#   
#
# close_Chrome
#
# the driver
#
# returns - None
#
def close_Chrome(driver):
    driver.quit()
    write_log("END: {0} - Chromedriver quits.".format(__name__))


if __name__ == "__main__":


    # dantesan--sada--2022-09-19 - check argument.
    args = sys.argv[1:]
    if len(args) == 0:
        num_cards = None
        print("\npython rack_access_control_test.py [number_of_cards_to_add]\n")
        print("\n Since there is no argument,\n \
        the number of cards = {0}.".format(RAC_CLASS.MAX_NUM_CARDS))
    else:
        num_cards = int(args[0])

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

    # Settings -> Rack Access Control
    set_panel_to_RAC()

    # add 'wait' var!
    delete_called = False
    # Delete Cards
    dont_del_list = ["100001"]
    while(delete_called is False):
        delete_called = delete_cards_with_dnd_list(driver, dont_del_list)

    # Settings -> Rack Access Control
    set_panel_to_RAC()

    # Add Cards
    rtn_list = create_card_data(driver, num_cards)
    if (rtn_list[0] is False):
        write_log("{0} - ERROR in create_card_data() : {1}"
            .format(__name__, rtn_list[1]))
        close_Chrome(driver)

    # Settings -> Rack Access Control
    set_panel_to_RAC()

    # add 'wait' var!
    delete_called = False
    # Delete Cards
    #dont_del_list = ["100001"]
    while(delete_called is False):
        delete_called = delete_cards_with_dnd_list(driver, dont_del_list)

    # LOGOUT
    # press username menu
    username_bttn = click_username(driver, usrnm)
    write_log("{0} - username pressed.".format(__name__))

    # logout
    log_out_we = click_dropdown_item(driver, LOG_OUT)
    write_log("{0} - Log Out clicked.".format(__name__))
    time.sleep(5)

    close_Chrome(driver)


#----------------------------------- END --------------------------------
