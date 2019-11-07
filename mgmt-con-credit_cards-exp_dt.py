from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.action_chains import ActionChains

import time
import random


from selenium_utils import open_mgmt_console_subs
from selenium_utils import wait_and_get_element
from selenium_utils import wait_and_get_label
from selenium_utils import wait_and_get_elem_by
from selenium_utils import wait_and_get_elements_by

driver = webdriver.Firefox()
#driver = webdriver.Chrome()

D3E_LHT  = "D3E Light"
rand_num = random.randint(1, 8001)
usr_nm   = "selenium" + str(rand_num)
USREMAIL = usr_nm + "@cigent.com"
USRPASSWD = "Cigent0813"
FIRST_CREDIT_CARD_NUM = "4242424242424242"

INVALID_EXP_DT = "MM/YY"  
VALID_CVC    = "777"
VALID_ZIP    = "33901"

def d3_Light():
    print("\nShow D3 Light subscriptions page\n")
    open_mgmt_console_subs(driver)
    # get button
    d3e_lt_button = wait_and_get_element(driver, "button.buy-it-btn.mat-flat-button")
    time.sleep(1)
    # press it
    d3e_lt_button.send_keys(Keys.RETURN)
    # get D3E_LHT label
    d3e_lt_lbl = wait_and_get_label(driver, "h2.receipt-title")
    assert  d3e_lt_lbl.text == D3E_LHT
    time.sleep(1)


def ent_id_and_passwd():
    email_text = wait_and_get_elem_by(driver, By.ID, "mat-input-0")
    time.sleep(1)
    print("enter e-mail ...")
    email_text.send_keys(USREMAIL)
    print("User Email: %s\n" % USREMAIL)
    # passwd
    passwd_text = wait_and_get_elem_by(driver, By.ID, "mat-input-1")
    time.sleep(1)
    print("enter passwd ...\n")
    passwd_text.send_keys(USRPASSWD)
    # confirm passwd
    confpw_text = wait_and_get_elem_by(driver, By.ID, "mat-input-2")
    time.sleep(1)
    print("confirm passwd ...\n")
    confpw_text.send_keys(USRPASSWD)
    # press next button
    d3e_lt_buttons = driver.find_elements_by_css_selector("button.mat-stroked-button.mat-primary")
    next_btn = d3e_lt_buttons[1]
    time.sleep(1)
    next_btn.send_keys(Keys.RETURN)

def enter_card_details_and_submit(card_num):

    print("Use card number ...")
    print(card_num)
    driver.switch_to.frame(frame_reference=driver.find_element(By.XPATH, '//iframe[@name="__privateStripeFrame5"]'))
    
    card_num_text = wait_and_get_elem_by(driver, By.NAME, "cardnumber")
    exp_dt        = wait_and_get_elem_by(driver, By.NAME, "exp-date")
    cvc           = wait_and_get_elem_by(driver, By.NAME, "cvc")
    card_num_text.send_keys(card_num)
    print("Use invalid date = %s" % INVALID_EXP_DT) # Won't allow or be set!
    exp_dt.send_keys(INVALID_EXP_DT)
    cvc.send_keys(VALID_CVC)
    postal        = wait_and_get_elem_by(driver, By.NAME, "postal")
    postal.send_keys(VALID_ZIP)


    time.sleep(1)
    # press Submit button
    driver.switch_to.default_content()
    submit_btn = wait_and_get_element(driver, "button.mat-flat-button.mat-primary.ng-star-inserted")
    submit_btn.send_keys(Keys.RETURN)
    time.sleep(5)

    #check error notice ...
    err_msg = "Your card's expiration date is incomplete."
    err_located = wait_and_get_elem_by(driver, By.ID, "card-errors")
   
    assert(err_msg == err_located.text) 
    return


if __name__ == "__main__":


    card_num = FIRST_CREDIT_CARD_NUM

    d3_Light()
    ent_id_and_passwd()
    enter_card_details_and_submit(card_num)

    driver.close()


