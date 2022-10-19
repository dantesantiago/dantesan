# 2022 - PANDUIT
#      - PDU Webpage : Event Icon Test
#      - by dantesan-sada--2022-10-18

import time

from selenium import webdriver


#sys.path.append()

import pdu_py_sel.utils.selenium_utils
from pdu_py_sel.utils.selenium_utils import login_pdu
from pdu_py_sel.utils.selenium_utils import logout_pdu
from pdu_py_sel.utils.selenium_utils import close_Chrome
from pdu_py_sel.utils.selenium_utils import set_panel_to_icon_item

from pdu_py_sel.page_objects.pdu_summary_wp import AL_EVENT

#import pdu_py_sel.utils.pdu_webpage_class 
#from pdu_py_sel.utils.pdu_webpage_class import PDU_WEBPAGE_CLASS
from pdu_py_sel.utils.pdu_webpage_class import chrome_options

from pdu_py_sel.utils.ssh_utils import run_command


import pdu_py_sel.utils.pdu_webpage_class 
from pdu_py_sel.utils.pdu_webpage_class import PDU_WEBPAGE_CLASS


from pdu_py_sel.utils.automation_utils import write_log
from pdu_py_sel.utils.automation_utils import debug_func


# CONSTANTS

# Download window to be checked later ...
EVENT_MENU_ITEMS = [ "Event Log",
                    #"Download Event Log",
                    "Data Log"#,
                    #"Download Data Log"
                   ]

WINDOW_TITLE_NAMES = [ "Event Log",
                    #"Download Event Log",
                    "Data Log"#,
                    #"Download Data Log"
                     ]


# CONSTANTS




#driver = webdriver.Firefox()
driver = webdriver.Chrome(options=chrome_options)


def get_driver():
    return driver

if __name__ == "__main__":

    login_pdu(driver)

    set_panel_to_icon_item(driver, AL_EVENT, 
                            list(EVENT_MENU_ITEMS), list(WINDOW_TITLE_NAMES))

    logout_pdu(driver)

    close_Chrome(driver)


#----------------------------------- END --------------------------------
