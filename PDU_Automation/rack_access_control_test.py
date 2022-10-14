# 2022 - PANDUIT
#      - Test: Rack Acces Control 
#      - by dantesan-sada--2022-08-31

import time
import sys

from selenium import webdriver

#import pdu_py_sel.utils.selenium_utils
from pdu_py_sel.utils.selenium_utils import click_dropdown_item
from pdu_py_sel.utils.selenium_utils import close_Chrome
from pdu_py_sel.utils.selenium_utils import click_svg_icon
from pdu_py_sel.utils.selenium_utils import login_pdu
from pdu_py_sel.utils.selenium_utils import logout_pdu
from pdu_py_sel.utils.selenium_utils import close_Chrome


#import pdu_py_sel.utils.pdu_webpage_class 
#from pdu_py_sel.utils.pdu_webpage_class import PDU_WEBPAGE_CLASS
from pdu_py_sel.utils.pdu_webpage_class import chrome_options

from pdu_py_sel.page_objects.pdu_summary_wp import AL_SETTINGS
from pdu_py_sel.page_objects.pdu_summary_wp import RACK_ACCESS_CONTROL


#import pdu_py_sel.utils.pdu_webpage_class 

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

# LOCATORS


#driver = webdriver.Firefox()
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
    write_log("{0} - Open Rack Access Control Panel.".format(set_panel_to_RAC.__name__))
    time.sleep(2)


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

    login_pdu(driver)

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
        # print the error
        print("{0} - ERROR in create_card_data() : {1}"
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
    logout_pdu(driver)

#----------------------------------- END --------------------------------
