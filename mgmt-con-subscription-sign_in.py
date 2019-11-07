# 2019 - Cigent Technology, Inc.
#      - MSP D3E Subscription: Verify subscription license activation.
# by dantesan

from selenium import webdriver

import time


from utils.msp_d3e_utils import ent_id_and_passwd
from utils.msp_d3e_utils import enter_card_details_and_submit
from utils.msp_d3e_utils import get_usremail
from utils.msp_d3e_utils import d3e_standard
from utils.msp_d3e_utils import sign_in_link_and_login
from utils.msp_d3e_utils import press_ok_in_YAAE_notice
from utils.msp_d3e_utils import verify_login_screen
from utils.msp_d3e_utils import login_and_sign_in
from utils.msp_d3e_utils import verify_names
from utils.msp_d3e_utils import verify_dashboard
from utils.msp_d3e_utils import verify_dashboard_img_labels

from utils.msp_d3e_utils import verify_licenses_labels
from utils.msp_d3e_utils import get_subscription_id
from utils.msp_d3e_utils import verify_subscription_id

from utils.msp_d3e_utils import VALID_EXP_DT
from utils.msp_d3e_utils import VALID_CVC
from utils.msp_d3e_utils import USRPASSWD
from utils.msp_d3e_utils import FIRST_CREDIT_CARD_NUM
from utils.msp_d3e_utils import SECND_CREDIT_CARD_NUM

from utils.selenium_utils import get_fn
from utils.selenium_utils import get_lineno

driver = webdriver.Firefox()
#driver = webdriver.Chrome()


if __name__ == "__main__":

    filename = get_fn()
    card_num = FIRST_CREDIT_CARD_NUM
    # create new user
    print("\nCreate a new user ...\n")
    usremail = get_usremail()
    d3e_standard(driver)
    ent_id_and_passwd(driver, usremail, USRPASSWD)
    enter_card_details_and_submit(driver, card_num, VALID_EXP_DT, VALID_CVC, True)
    time.sleep(5)

    # get the subscription id/order number
    subscription_id = get_subscription_id(driver)

    print("\nPress the \'Sign in instead\' link ...\n")
    d3e_standard(driver)
    sign_in_link_and_login(driver)

    # verify login page is shown
    verify_login_screen(driver)

    #runYAAE = False  # Set True after BUG_935 fix.
    runYAAE = True
    if runYAAE:
        # enter new user to get into 'Your Account Already Exists' (YAAE)
        print("\n{}:{} -- Enter the same user and another credit card info to go".format(filename, get_lineno()))
        print("\t\t\t\t\tto Your Account Already Exists notice ...\n")
        card_num = SECND_CREDIT_CARD_NUM
        d3e_standard(driver)
        ent_id_and_passwd(driver, usremail, USRPASSWD)
        enter_card_details_and_submit(driver, card_num, VALID_EXP_DT, VALID_CVC, True)
        time.sleep(5)

        # Press 'OK' in YAAE notice    
        press_ok_in_YAAE_notice(driver)

        # verify login page is shown
        verify_login_screen(driver)

        # login and/or sign in    - usrname is prefilled
        login_and_sign_in(driver, "", USRPASSWD)

        # Verify names
        verify_names(driver, usremail)

        # Verify labels
        verify_licenses_labels(driver)

        # Verify subscription id
        verify_subscription_id(driver, subscription_id)      

    else:
        # login and/or sign in    - usrname is prefilled
        login_and_sign_in(driver, usremail, USRPASSWD)
        # temp - Verify Dashboard
        verify_dashboard(driver, usremail)
        verify_dashboard_img_labels(driver)
    
    #driver.quit()
