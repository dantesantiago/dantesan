# 2022 - PANDUIT
#      - PDU Webpage : Selenium python utilities
#      - by dantesan-sada--2022-08-31

import time

from selenium import webdriver

import pdu_py_sel.utils.selenium_utils
from pdu_py_sel.utils.selenium_utils import login_pdu
from pdu_py_sel.utils.selenium_utils import logout_pdu
from pdu_py_sel.utils.selenium_utils import close_Chrome

#import pdu_py_sel.utils.pdu_webpage_class 
#from pdu_py_sel.utils.pdu_webpage_class import PDU_WEBPAGE_CLASS
from pdu_py_sel.utils.pdu_webpage_class import chrome_options

from pdu_py_sel.utils.ssh_utils import run_command


import pdu_py_sel.utils.pdu_webpage_class 
from pdu_py_sel.utils.pdu_webpage_class import PDU_WEBPAGE_CLASS


from pdu_py_sel.utils.automation_utils import write_log
from pdu_py_sel.utils.automation_utils import debug_func


#driver = webdriver.Firefox()
driver = webdriver.Chrome(options=chrome_options)


def get_driver():
    return driver

if __name__ == "__main__":

    login_pdu(driver)

    logout_pdu(driver)

    close_Chrome(driver)


#----------------------------------- END --------------------------------
