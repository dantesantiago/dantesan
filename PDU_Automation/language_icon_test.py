# 2022 - PANDUIT
#      - PDU Webpage : Language Icon Test
#      - by dantesan-sada--2022-10-18

import time

from selenium import webdriver


#sys.path.append()

import pdu_py_sel.utils.selenium_utils
from pdu_py_sel.utils.selenium_utils import login_pdu
from pdu_py_sel.utils.selenium_utils import logout_pdu
from pdu_py_sel.utils.selenium_utils import close_Chrome
from pdu_py_sel.utils.selenium_utils import set_panel_to_icon_item

from pdu_py_sel.page_objects.pdu_summary_wp import AL_LANGUAGE

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
LANGUAGE_MENU_ITEMS = [ "English",
                        "Françcais",
                        "Italiano",
                        "한국어",
                        "Deutsch",
                        "Español",
                        "日本語",
                        "中文"
                      ]

WINDOW_TITLE_NAMES = [ "Monitored & Switched Per Outlet PDU",
                       "Chaque Sortie d'UDC Contrôlée & Commutée",
                       "PDU monitorato & commutato per presa",
                       "모니터링 및 전환 당 콘센트",
                       "jeden Ausgangssteckplatz der PDU überwacht und geschaltet",
                       "PDU Monitoreo por Salida y Switcheado",
                       "アウトレットPDU監視や切り換え",
                       "每个出口PDU监控和切换"
                     ]


# CONSTANTS




#driver = webdriver.Firefox()
driver = webdriver.Chrome(options=chrome_options)


def get_driver():
    return driver

if __name__ == "__main__":

    login_pdu(driver)

    set_panel_to_icon_item(driver, AL_LANGUAGE, 
                            list(LANGUAGE_MENU_ITEMS), list(WINDOW_TITLE_NAMES))

    logout_pdu(driver)

    close_Chrome(driver)


#----------------------------------- END --------------------------------
