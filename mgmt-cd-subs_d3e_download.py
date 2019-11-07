# 2019 - Cigent Technology, Inc.
#      - MSP D3E Subscription: Verify odwnload link for each subscription plan.
#      - by dantesan


from selenium import webdriver

import time

from utils.msp_d3e_utils import ent_id_and_passwd
from utils.msp_d3e_utils import enter_card_details_and_submit
from utils.msp_d3e_utils import get_usremail
from utils.msp_d3e_utils import d3e_trial
from utils.msp_d3e_utils import enter_trial_code
from utils.msp_d3e_utils import d3e_standard
from utils.msp_d3e_utils import d3e_premium_new
from utils.msp_d3e_utils import chk_download_and_press_link
from utils.msp_d3e_utils import verify_lic_price
from utils.msp_d3e_utils import set_billing_method
from utils.msp_d3e_utils import verify_prices
from utils.msp_d3e_utils import verify_email

from utils.msp_d3e_utils import FIRST_CREDIT_CARD_NUM
from utils.msp_d3e_utils import VALID_EXP_DT
from utils.msp_d3e_utils import VALID_CVC
from utils.msp_d3e_utils import USRPASSWD
from utils.msp_d3e_utils import D3E_UNIT_PRICE
from utils.msp_d3e_utils import D3E_STD
from utils.msp_d3e_utils import BILL_MONTHLY
from utils.msp_d3e_utils import BILL_ANNUALLY

from utils.ssh_utils import run_command


driver = webdriver.Firefox()
#driver = webdriver.Chrome()

# 2019-09-11 
TRIAL_CODE = "SECURITY"



if __name__ == "__main__":

    #tc_ok = True
    tc_ok = False    # Suddenly, trial code is set! 
                      #    Earlier, any value would do!

    if tc_ok:
        d3e_trial(driver)
        usremail = get_usremail()
        ent_id_and_passwd(driver, usremail, USRPASSWD)
        driver.maximize_window()
        # enter trial code
        print("\nTrial Code: {}".format(TRIAL_CODE))
        enter_trial_code(driver, TRIAL_CODE)
        time.sleep(3)
        chk_download_and_press_link(driver)
        time.sleep(3)

   
    usremail = get_usremail()
    # verify license price inside email and passwd entry window
    chk_billing_method = False
    if chk_billing_method: 
        num_lics = d3e_standard(driver, chk_billing_method)
        ent_id_and_passwd(driver, usremail, USRPASSWD, D3E_STD, num_lics)
    else:
        num_lics = d3e_standard(driver)
        ent_id_and_passwd(driver, usremail, USRPASSWD, D3E_STD, num_lics)

    # verify email address
    verify_email(driver, usremail)

    enter_card_details_and_submit(driver, FIRST_CREDIT_CARD_NUM, VALID_EXP_DT, VALID_CVC, True)
    driver.maximize_window()
    time.sleep(4)
    chk_download_and_press_link(driver)
    time.sleep(3)

    d3e_premium_new(driver)
    driver.maximize_window()
    time.sleep(3)

    driver.quit()
#----------------------------------- END --------------------------------
