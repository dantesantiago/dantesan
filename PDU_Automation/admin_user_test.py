# 2022 - PANDUIT
#      - PDU Webpage : Admin User Test
#      - by dantesan-sada--2022-10-19

import time

from selenium import webdriver

import pdu_py_sel.utils.pdu_webpage_class
import pdu_py_sel.utils.selenium_utils
from pdu_py_sel.page_objects.pdu_summary_wp import AL_ADMIN_USER
from pdu_py_sel.utils.automation_utils import debug_func, write_log
#import pdu_py_sel.utils.pdu_webpage_class 
#from pdu_py_sel.utils.pdu_webpage_class import PDU_WEBPAGE_CLASS
from pdu_py_sel.utils.pdu_webpage_class import (PDU_WEBPAGE_CLASS,
                                                chrome_options)
from pdu_py_sel.utils.selenium_utils import (close_Chrome, login_pdu,
                                             logout_pdu,
                                             set_panel_to_icon_item)
from pdu_py_sel.utils.ssh_utils import run_command

#sys.path.append()










# CONSTANTS

ADMIN_USER_MENU_ITEMS = [ "Change Password",
                          "User Accounts",
                          "Log Out"
                        ]  
# Log In button verifies Log Out was done.
WINDOW_TITLE_NAMES = [ "Change Password",
                       "User Settings"
                       "Log In"
                     ]


# CONSTANTS




#driver = webdriver.Firefox()
driver = webdriver.Chrome(options=chrome_options)


def get_driver():
    return driver

if __name__ == "__main__":

    login_pdu(driver)

    rtn_list = set_panel_to_icon_item(driver, AL_ADMIN_USER, 
                                      list(ADMIN_USER_MENU_ITEMS), 
                                      list(WINDOW_TITLE_NAMES))
    if(rtn_list[0] is False):
        write_log("{0} - {1}".format(__name__, rtn_list[1]), None, True)
        write_log("{0} - Error in verifying admin user menu item windows."
            .format(__name__), None, True)   

    logout_pdu(driver)

    close_Chrome(driver)


#----------------------------------- END --------------------------------
