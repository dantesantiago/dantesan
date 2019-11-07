from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

import time


from selenium_utils import open_mgmt_console_subs
from selenium_utils import wait_and_get_element
from selenium_utils import wait_and_get_label


from msp_d3e_utils import ent_id_and_passwd
from msp_d3e_utils import enter_card_details_and_submit
from msp_d3e_utils import get_usremail
from msp_d3e_utils import d3e_trial
from msp_d3e_utils import enter_trial_code
from msp_d3e_utils import d3e_standard
from msp_d3e_utils import d3e_premium
from msp_d3e_utils import chk_download_and_press_link
from msp_d3e_utils import sign_in_link_and_login


driver = webdriver.Firefox()
#driver = webdriver.Chrome()



if __name__ == "__main__":

    d3e_trial(driver)
    sign_in_link_and_login(driver)

    d3e_standard(driver)
    sign_in_link_and_login(driver)

    d3e_premium(driver)

    driver.quit()
