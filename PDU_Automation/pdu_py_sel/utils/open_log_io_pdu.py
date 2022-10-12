# 2022 - PANDUIT
#      - PDU Webpage : Selenium python utilities
#      - by dantesan-sada--2022-08-31

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

#import selenium_utils
#from selenium_utils import open_webpage
#from selenium_utils import wait_and_get_elem_by
#from selenium_utils import enter_text
#from selenium_utils import click_button
#from selenium_utils import check_xpath_exists
#from selenium_utils import click_dropdown_item


from ..page_objects import pdu_summary_wp#

from ..page_objects.pdu_summary_wp import CHANGE_PASSWORD
from ..page_objects.pdu_summary_wp import USER_ACCOUNTS
from ..page_objects.pdu_summary_wp import LOG_OUT

from ssh_utils import run_command


import pdu_webpage_class 
from pdu_webpage_class import PDU_WEBPAGE_CLASS

# dantesan--sada--2022-09-28
import automation_utils
from automation_utils import CONTINUE_MSG
from automation_utils import MONITORED_LCTR
from automation_utils import USERNAME_ID_LCTR
from automation_utils import PASSWORD_ID_LCTR
from automation_utils import LOGIN_BTTN_LCTR
from automation_utils import CONTINUE_MSG_LCTR
from automation_utils import CONTINUE_MSG_OK_LCTR

from automation_utils import write_log
from automation_utils import debug_func




#----------------------------------- END --------------------------------
