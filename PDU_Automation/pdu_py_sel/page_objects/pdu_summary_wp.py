# 2022 - PANDUIT
#      - Page Object: PDU Summary 
#      - by dantesan-sada--2022-08-31
import time

#import sys, os
#file_dir = os.path.dirname("../utils")
#sys.path.append(file_dir)

from ..utils import selenium_utils

from ..utils.selenium_utils import wait_and_get_elem_by
from ..utils.selenium_utils import enter_text
from ..utils.selenium_utils import click_button

from ..utils.selenium_utils import ID
from ..utils.selenium_utils import XPATH
from ..utils.selenium_utils import NAME

# CONSTANTS

# MENU ITEM NAMES
# username -----------------------------------------
CHANGE_PASSWORD = 'Change Password'
USER_ACCOUNTS = "User Accounts"
LOG_OUT = "Log Out"
# username -----------------------------------------

# settings -----------------------------------------
RACK_ACCESS_CONTROL = "Rack Access Control"

# settings -----------------------------------------
# MENU ITEM NAMES

#svgs aria-label's

AL_HOME = 'home'
AL_SETTINGS = 'settings-option'

#svgs aria-label's



# CONSTANTS

# LOCATORS

# LOCATORS


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
def click_username(driver, username):
    username_xpath = "//button/span[text() = '{0}']".format(username)
    username_bttn = click_button(driver, XPATH, username_xpath)
    return username_bttn


#---------------------------------- END -------------------------------------
