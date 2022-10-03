# 2022 - PANDUIT
#      - PDU Webpage : Selenium python utilities
#      - by dantesan-sada--2022-09-01

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import time
import random

from utils.pdu_webpage_class import PDU_WEBPAGE_CLASS
from selenium_utils import get_driver
from selenium_utils import wait_and_get_element
from selenium_utils import wait_and_get_label
from selenium_utils import wait_and_get_elem_by
from selenium_utils import wait_and_get_elements_by
from ssh_utils import run_command

# CONSTANTS

LI_WIN_NAME  = "PDU Login Window"
LI_WIN = "LI_WIN"

# CONSTANTS


# PDU Initial Webpage
def enter_username_and_passwd(driver, username, usrpasswd):

    print("\n{} -------------------------------------------\n".format(LI_WIN))

    # username
    username_textbox = wait_and_get_elem_by(driver, By.ID, "username")
    print("Enter Username ...\n")
    username_textbox.send_keys(username)

    passwd_textbox = wait_and_get_elem_by(driver, By.ID, "password")
    time.sleep(1)
    print("Enter passwd ...\n")
    passwd_textbox.send_keys(usrpasswd)

    log_in_button = driver.find_elements_by_css_selector("button.???")
    next_btn = log_in_button
    time.sleep(1)
    next_btn.send_keys(Keys.RETURN)
    return


# Get Verification Code
def get_verification_code(usremail):
    ret_list = run_command("cd ~/selenium_ssh; python selenium_ssh.py 1 " + usremail)
    vc = ret_list[0]
    ver_code = vc.decode('utf-8')
    # remove newline
    ver_code = ver_code[0:-1]
    return(ver_code)




# has_zip_code - True or False
# added params for flexibility
# exp_date     - expiration date
# cvc_val      - 3-digit number
def enter_card_details_and_submit(driver, card_num, exp_date, cvc_val, has_zip_code):

    print("\n{} -------------------------------------------\n".format(PI_WIN))
    print("Use card number ... {}".format(card_num))
    #print(card_num)

    driver.switch_to.frame(frame_reference=wait_and_get_elem_by(driver, By.NAME, "__privateStripeFrame5"))
    card_num_text = wait_and_get_elem_by(driver, By.NAME, "cardnumber")
    card_num_text.click()
    time.sleep(1)
    card_num_text.send_keys(card_num)
    driver.switch_to.default_content()

    print("\nEnter expiry month/year ... {}".format(exp_date))
    iframe6 = wait_and_get_elem_by(driver, By.NAME, "__privateStripeFrame6")
    driver.switch_to.frame(iframe6)
    exp_dt = wait_and_get_elem_by(driver, By.NAME, "exp-date")
    exp_dt.click()
    time.sleep(1)
    exp_dt.send_keys(exp_date)
    driver.switch_to.default_content()

    print("\nEnter cvc ... {}".format(cvc_val))
    driver.switch_to.frame(frame_reference=wait_and_get_elem_by(driver, By.NAME, "__privateStripeFrame7"))
    cvc = wait_and_get_elem_by(driver, By.NAME, "cvc")
    cvc.click()
    time.sleep(1)
    cvc.send_keys(cvc_val)

    #if has_zip_code == True:
    #    postal        = wait_and_get_elem_by(driver, By.NAME, "postal")
    #    postal.send_keys(VALID_ZIP)

    print("\nPress \'Submit Payment\' button ...")
    time.sleep(1)
    # press Submit button
    driver.switch_to.default_content()
    submit_btn = wait_and_get_elem_by(driver, By.CSS_SELECTOR, "button.submit-payment.ng-tns-c8-0.ng-star-inserted")
    submit_btn.send_keys(Keys.RETURN)
    time.sleep(5)
    #Verify Window
    try:
        credit_card_ok_lbl = None
        if card_num == FIRST_CREDIT_CARD_NUM:
            thank_you_msg = 'Thank you for your order of D3E'
            credit_card_ok_lbl = wait_and_get_elem_by(driver, By.XPATH, "//b[text()='Thank you for your order of D3E']")
            print(thank_you_msg)
        else:
            acct_exists = 'Your Account Already Exists'
            credit_card_ok_lbl = wait_and_get_elem_by(driver, By.XPATH, "//h2[text()='Your Account Already Exists']")
            print(acct_exists)

        assert(credit_card_ok_lbl is not None)
        time.sleep(5)
    except Exception as e:
        #print("\nINVALID VALUES NOT ACCEPTED!\n") # For testing mgmt-con-credit_card-invalid_values.py 
                                                   # and raise below commented out.
        raise e

    return


def get_usremail():
    rand_num  = random.randint(1, 888888)
    usr_nm    = "selenium" + str(rand_num)
    usremail  = usr_nm + "@cigent.com"
    return usremail


def d3e_trial(driver):
    print("\nShow Cigent Trial page\n")
    open_mgmt_console_subs(driver)
    # get button
    d3e_trial_button = wait_and_get_element(driver, "button.try-it-btn.mat-flat-button")
    # 
    time.sleep(3)
    # press it
    d3e_trial_button.send_keys(Keys.RETURN)
    # Get CIG_TRL label 
    time.sleep(3)
    driver.maximize_window()
    cig_trial_elem = wait_and_get_elem_by(driver, By.XPATH, "//span[text()='30-Day Free Trial']")
    print(D3E_TRL)
    assert  cig_trial_elem.text == D3E_TRL # overkill!
    time.sleep(3)


# return number of licenses from select_num_lic()
def d3e_standard(driver, chk_billing_method = None):
    print("\n{} -------------------------------------------\n".format(CP_WIN))
    print("\nShow D3E Standard subscriptions page\n")
    open_mgmt_console_subs(driver)

    if chk_billing_method is not None:
        # select monthly billing - billing method to ANNUAL Only - QA--2019-10-09
        set_billing_method(driver, BILL_MONTHLY)
        time.sleep(3)
        # select annual billing
        set_billing_method(driver, BILL_ANNUALLY)
        time.sleep(3)

    driver.maximize_window()
    # check number of licenses
    chk_num_lic = False # set True to turn on
    if chk_num_lic:
        num_lics = select_num_lic(driver)
    else:
        num_lics = 1

    # get button
    d3e_lt_button = wait_and_get_element(driver, "button.buy-it-btn.mat-flat-button")
    time.sleep(3)
    # press it
    d3e_lt_button.send_keys(Keys.RETURN)
    driver.maximize_window()
    # get D3E_STD label
    d3e_lt_lbl = wait_and_get_label(driver, "h2.receipt-title")
    d3e_lt_lbl_txt = d3e_lt_lbl.text
    print("\n D3E Std = {}, Account Information Window Label = {} ".format(D3E_STD, d3e_lt_lbl_txt))
    assert  d3e_lt_lbl_txt == D3E_STD
    #d3e_std_prc = wait_and_get_elem_by(driver, By.XPATH, "//span[text()='$5.83/month']")
    #assert STD_PRC == d3e_std_prc.text #overkill!

    if chk_billing_method is not None:
        verify_prices(driver, BILL_ANNUALLY, num_lics)

    time.sleep(1)
    return(num_lics)



def d3e_premium(driver):
    print("\nShow Contact Us page\n")
    open_mgmt_console_subs(driver)
    # get button
    d3e_premium_button = wait_and_get_element(driver, "a.contact-us-btn.mat-flat-button") # Yoh! Not button ...
    time.sleep(3)
    # press it
    d3e_premium_button.send_keys(Keys.RETURN)
    time.sleep(5)
    # Check next window
    WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
    newWindow = driver.window_handles
    contactUs = newWindow[1]
    driver.switch_to.window(contactUs)
    driver.maximize_window()
    assert D3E_PRM in driver.title
    # get "Contact Us" label
    contact_us_elem = wait_and_get_label(driver, "h1")
    assert  contact_us_elem.text == D3E_PRM
    time.sleep(2)


def d3e_premium_new(driver):
    open_mgmt_console_subs(driver)
    driver.maximize_window()
    cs_str = "Coming Soon"
    print("\n Verify \'{}\' is shown ...\n".format(cs_str))
    cs_elem = wait_and_get_elem_by(driver, By.XPATH, "//div[@class='coming-soon']")
    assert cs_elem.text == cs_str


def enter_trial_code(driver, trial_code):

    print("Enter Trial Code ...")
    trial_code_textbox = wait_and_get_elem_by(driver, By.ID, "mat-input-3")
    trial_code_textbox.send_keys(trial_code)
    time.sleep(2)
    start_bttn = wait_and_get_elem_by(driver, By.CSS_SELECTOR, "button.mat-flat-button.mat-primary.ng-star-inserted")
    print("Press Start button ...")
    start_bttn.send_keys(Keys.RETURN)
    return


# Allow the setting of the number of Licenses.
def chk_download_and_press_link(driver):

    # check thank you message 
    # - enter_card_details_and_submit() did it!
 
    # get download link
    download_link = wait_and_get_elem_by(driver, By.CSS_SELECTOR, "a.download-button.mat-button.mat-flat-button")
    
    # assert download link text
    dwnld_lnk_txt = download_link.text
    print("Download Link Text: \'{}\'".format(dwnld_lnk_txt))
    assert dwnld_lnk_txt == DOWNLOAD_LINK_TEXT
    # click download link
    download_link.click()


# add Number of License for D3E_STD when checking billing method.
def verify_lic_price(driver, plan_type, num_lics = None):

    try:

        if plan_type == D3E_STD:
            price_elem = wait_and_get_elem_by(driver, By.CSS_SELECTOR, "span.unit-price")
            price_str = price_elem.text
            std_price_lst = YR_STD_PRC.split("/")
            std_price_str = std_price_lst[0].strip("$")
            std_price = float(std_price_str) 
            if num_lics is not None:
               std_price *= float(num_lics)
            # convert std_price to 2 decimal places string
            std_price_str = ("{0:.2f}".format(std_price))
            print("\nVerify license price (price_str = \'{}\') has std_price = {} ...\n".format(price_str, std_price_str))
            assert std_price_str in price_str

    except Exception as e:
        raise e


def sign_in_link_and_login(driver):

    # Sign in instead
    sign_in_link = wait_and_get_elem_by(driver, By.PARTIAL_LINK_TEXT, SIGN_IN_INSTEAD)
 
    # press link
    sign_in_link.click()
    time.sleep(3)
   
   
def press_ok_in_YAAE_notice(driver):

    print("Locate \'OK\' button ...")
    ok_bttn = wait_and_get_elem_by(driver, By.XPATH, "//button[@class='mat-stroked-button']")
    time.sleep(5)
    print("Press \'OK\' button ...")
    ok_bttn.click()


def verify_login_screen(driver):

    print("\nVerify the login screen ...")
    print("Search for \'" + SIGN_IN_TO_UR_ACCT + "\' ...")
    sing_in_to_ur_acct = wait_and_get_elem_by(driver, By.XPATH, "//h1[text()=\'" + SIGN_IN_TO_UR_ACCT + "\']")
    print("\nLogin Screen is verified ...")
    # Username and Passwd location can also be added.


def login_and_sign_in(driver, usrname, usrpasswd):

    #usrname entry
    if usrname != "":
        # locate Username entry 
        email_text = wait_and_get_elem_by(driver, By.ID, "mat-input-3")
        time.sleep(1)
        print("enter e-mail ...")
        email_text.send_keys(usrname)
        print("Username or Email: %s\n" % usrname)

    # passwd entry
    passwd_text = wait_and_get_elem_by(driver, By.ID, "mat-input-4")
    time.sleep(1)
    print("enter passwd ...\n")
    passwd_text.send_keys(usrpasswd)
    time.sleep(2)

    # press Sign in
    print("Press Sign In ...\n")
    #sign_in_bttn = wait_and_get_elem_by(driver, By.XPATH, "//button[@class='log-in-btn.mat-flat-button']")
    sign_in_bttn = wait_and_get_elem_by(driver, By.CSS_SELECTOR, "button.log-in-btn.mat-flat-button")
    time.sleep(2)
    sign_in_bttn.click()


def verify_names(driver, email_addr, chk_grp_name = None):

    #Full Name - email address
    full_name = wait_and_get_elem_by(driver, By.CLASS_NAME, "fullname")
    fname = wait_and_get_elem_by(driver, By.XPATH, "//div[text()=\'" + email_addr + "\']")
    assert full_name == fname
    print("\n%s Full Name verified ...\n" % email_addr)
    

    #User Name - email address
    user_name = wait_and_get_elem_by(driver, By.XPATH, "//div[@class='username']")
    print("user_name = \'{}\' email_addr = \'{}\'".format(user_name.text, email_addr))
    assert user_name.text.strip() == email_addr.strip() 
    print("\n%s User Name verified ...\n" % email_addr)

    if chk_grp_name != None:
        #Group Name - email address
        grp_name = wait_and_get_elem_by(driver, By.XPATH, "//a[text()=\'" + email_addr + "\']")
        print("\n%s Group Name verified ...\n" % email_addr)



def verify_dashboard(driver, email_addr = None):
  
    # Dashboard 
    ul_title = wait_and_get_elem_by(driver, By.XPATH, "//span[@class='toolbar-title']")
    assert ul_title.text == DASHBOARD
    print("\n%s Title verified ...\n" % DASHBOARD)

    # Group Assets Summary Header and Titles

    # Header
    grp_assets_summ = wait_and_get_elem_by(driver, By.XPATH, "//h2[@class='devices-overview-h2']")
    assert grp_assets_summ.text == GRP_ASSETS_SUMM
    print("\n%s header verified ...\n" % GRP_ASSETS_SUMM) 

    # Total Assets
    ttl_assets = wait_and_get_elem_by(driver, By.XPATH, "//button[@aria-label='Change sorting for total_assets']")
    ttl_assets_str = "Total Assets"
    assert ttl_assets_str == ttl_assets.text
    print("\n%s column title verified ...\n" % ttl_assets_str) 

    # RS Units
    rs_units = wait_and_get_elem_by(driver, By.XPATH, "//button[@aria-label='Change sorting for rs_online']")
    rs_units_str = "RS Units"
    assert rs_units_str in rs_units.text
    print("\n%s column title verified ...\n" % rs_units_str) 

    # RSE Units
    rse_units = wait_and_get_elem_by(driver, By.XPATH, "//button[@aria-label='Change sorting for E_online']")
    rse_units_str = "RSE Units"
    assert rse_units_str in rse_units.text
    print("\n%s column title verified ...\n" % rse_units_str) 

    # Cyberstack Endpoints
    cyb_ep = wait_and_get_elem_by(driver, By.XPATH, "//button[@aria-label='Change sorting for C_online']")
    cyb_ep_str = "Cyberstack Endpoints"
    assert cyb_ep_str in cyb_ep.text
    print("\n%s column title verified ...\n" % cyb_ep_str) 

    # Cigent Devices
    cig_dv = wait_and_get_elem_by(driver, By.XPATH, "//button[@aria-label='Change sorting for D_online']")
    cig_dv_str = "Cigent Devices"
    assert cig_dv_str in cig_dv.text
    print("\n%s column titles verified ...\n" % cig_dv_str) 

    # Group Assets Summary Header and Titles


def verify_dashboard_img_labels(driver):

    # top labels
    img_labels= ["Total Users", "Online Assets", "Informational", "Warning", "Critical"]
    div_img_labels = wait_and_get_elements_by(driver, By.XPATH, "//div[@class='card-info']")
    ctr = 0
    for img_lbl in div_img_labels:
        img_no = ctr + 1
        #print("\nImage %s -- %s -- to-be-verified ..." % img_no, img_labels[ctr])
        print("\nImage {} -- {} -- to-be-verified ...".format(img_no, img_labels[ctr]))
        assert img_lbl.text == img_labels[ctr]
        print("\n VERIFIED!")
        ctr += 1

    # footer labels
    img_footers = ["View Users", "View Assets", "View Information", "View Warnings", "View Critical"]
    a_img_footers  = wait_and_get_elements_by(driver, By.XPATH, "//a[@class='user-footer-link']")
    ctr = 0
    for img_ftr_lbl in a_img_footers:
        img_no = ctr + 1
        print("\nImage {} footer -- {} = {} ...".format(img_no, img_ftr_lbl.text, img_footers[ctr]))
        assert img_ftr_lbl.text == img_footers[ctr]
        ctr += 1


def verify_licenses_labels(driver):
    
    span_title = wait_and_get_elem_by(driver, By.XPATH, "//span[@class='toolbar-title']")
    win_title = "Manage Licenses"
    assert span_title.text == win_title
    print("Screen Top Title \'{}\' is verified ...".format(win_title)) 

    #manage_ur_lics = wait_and_get_elem_by(driver, By.XPATH, "//h2[@_ngcontent-c25='']")
    #manage_your_licenses = "Manage your Licenses"
    #assert manage_ur_lics.text == manage_your_licenses

    # bold labels
    bold_labels= ["Activate a License", "Subscriptions", "Software Download"]
    h2_bold_labels = wait_and_get_elements_by(driver, By.XPATH, "//h2[@class='table-title-h2']")
    ctr = 0
    for bold_lbl in h2_bold_labels:
        print("\nBold Label \'{}\' to-be-verified ...".format(bold_labels[ctr]))
        assert bold_lbl.text == bold_labels[ctr]
        print("\n VERIFIED!")
        ctr += 1

    # Add Subscription
    #add_subs_elem = wait_and_get_elem_by(driver, By.XPATH, "//span[@class='add-sub-text.ng-tns-c26-13']")
    add_subs_elem = wait_and_get_elem_by(driver, By.CSS_SELECTOR, "span.add-sub-text.ng-tns-c26-13")
    add_subs_str = "Add Subscription"   
    assert add_subs_elem.text == add_subs_str
    print("\nBold Label: \'{}\' VERIFIED ...\n".format(add_subs_str))

    # tbl labels
    bold_labels= ["Activate a License", "Subscriptions", "Software Download"]
    h2_bold_labels = wait_and_get_elements_by(driver, By.XPATH, "//h2[@class='table-title-h2']")
    ctr = 0
    for bold_lbl in h2_bold_labels:
        print("\nBold Label \'{}\' to-be-verified ...".format(bold_labels[ctr]))
        assert bold_lbl.text == bold_labels[ctr]
        print("\n VERIFIED!")
        ctr += 1

    # Add Subscription
    #add_subs_elem = wait_and_get_elem_by(driver, By.XPATH, "//span[@class='add-sub-text.ng-tns-c26-13']")
    add_subs_elem = wait_and_get_elem_by(driver, By.CSS_SELECTOR, "span.add-sub-text.ng-tns-c26-13")
    add_subs_str = "Add Subscription"   


    # Table Headers
    print("\n TABLE COLUMN HEADERS TO BE CHECKED ... ---------------------------- \n")
    tbl_col_str = ["", "Used Licenses", "Available Licenses", "Total Licenses", "Subscription Name", "Owner", "Status", "Type", "Tier", "Renews/Expires", "Recurring Subscription"]
    tbl_col_hdrs = wait_and_get_elements_by(driver, By.XPATH, "//th[@role='columnheader']")
    ctr = 0
    for col_hdr in tbl_col_hdrs:
        print("\nTable Column Header: \'{}\' to-be-verified ...".format(tbl_col_str[ctr]))
        print("\ncol_hdr.text: \'{}\' ...".format(col_hdr.text))
        assert col_hdr.text == tbl_col_str[ctr]
        print("\n VERIFIED!")
        ctr += 1
    print("\n")
    return


def set_billing_method(driver, billing_method):

    try:
        assert billing_method in BILLING_METHODS
  
        if billing_method == BILL_ANNUALLY:
            radio_btn_id = "radio-1"
            oth_rdo_btn = "radio-2"
        if billing_method == BILL_MONTHLY:
            radio_btn_id = "radio-2"
            oth_rdo_btn = "radio-1"
  
        print("\n {} ...".format(billing_method))
        radio_bttn_elem = wait_and_get_elem_by(driver, By.ID, radio_btn_id)
        # select it!
        radio_bttn_elem.click()
        time.sleep(3)
  
        # make sure the other one is not selected
        oth_rdo_btn_elem = wait_and_get_elem_by(driver, By.ID, oth_rdo_btn)
        assert oth_rdo_btn_elem.is_selected is not True
    except Exception as e:
        raise e
    
    return


# Add num_lics param for D3E_STD ...
def verify_prices(driver, billing_method, num_lics = None):

    try:
        assert billing_method in BILLING_METHODS
    
        d3e_unit_price = D3E_UNIT_PRICE
        dup_str = d3e_unit_price.strip("$/monthly")
        unit_price = float(dup_str)
    
        product_total_elem = wait_and_get_elem_by(driver, By.XPATH, "//div[@class='product-total']")
        total_price_elem = wait_and_get_elem_by(driver, By.XPATH, "//span[@class='total-price']")
    
        if num_lics is None:
            num_lics = 1
        if billing_method == BILL_ANNUALLY:
            annual_price = num_lics * unit_price * 12
            annual_price = round(annual_price, 2)
            assert str(annual_price) in product_total_elem.text
            print("\nProduct Price = {0:.2f}, billing method: {1} verified ... ".format(float(annual_price), billing_method))
            assert str(annual_price) in total_price_elem.text
            print("\nTotal Price = {0:.2f}, billing method: {1} verified ...\n".format(float(annual_price), billing_method))
    
        # later ...
        #if billing_method == BILL_MONTHLY: 

    except Exception as e:
        raise e
    
    return


# called after enter_card_details_and_submit() - OC_WIN
def get_subscription_id(driver):
 
    try:
        subs_id_elem = wait_and_get_elem_by(driver, By.XPATH, "//span[@class='order-number-text']")
        subscription_id = subs_id_elem.text
        print("\n \'{}\' subscription_id = {}\n".format(OC_WIN, subscription_id))

    except Exception as e:
        raise e

    return subscription_id
    

# Called when License Window is displayed (LIC_WIN).
# Must call get_subscription_id(driver) to get the subscription_id beforehand.
def verify_subscription_id(driver, subscription_id):

    try:
        #lic_win_subs_id_elem = wait_and_get_elem_by(driver, By.XPATH, "//td[@class='mat-cell.cdk-column-subscription_id.mat-column-subscription_id.ng-tns-c26-13.ng-star-inserted']")
        lic_win_subs_id_elem = wait_and_get_elem_by(driver, By.CSS_SELECTOR, "td.mat-cell.cdk-column-subscription_id.mat-column-subscription_id.ng-tns-c26-13.ng-star-inserted")
        tbl_subs_id = lic_win_subs_id_elem.text
        print("\n \'{}\' subscription_id = {}\n".format(LIC_WIN, tbl_subs_id))
        assert subscription_id == tbl_subs_id

    except Exception as e:
        raise e

    return


# select the number of license/s (CP_WIN)
def select_num_lic(driver, d3e_prem = None):

    try:
        if d3e_prem is None:
             sel_lic_dropdown_elem = wait_and_get_elem_by(driver, By.CSS_SELECTOR, "span.mat-select-value-text.ng-tns-c13-3.ng-star-inserted")
             for i in range(1, 10): # Change stop value to verify diff num_lics.
                                    # Did with num_lics = 6 (DT191015--NUM_LICS_6 in notes).
                 sel_lic_dropdown_elem.click()
                 time.sleep(1)
                 option_id = "mat-option-" + str(i)
                 dropdown_elem = wait_and_get_elem_by(driver, By.ID, option_id)
                 ActionChains(driver).move_to_element(dropdown_elem).perform()
                 print("\nOption: {}".format(dropdown_elem.text))
                 dropdown_elem.click()
                 time.sleep(1)
    except Exception as e:
        raise e

    i += 1 # make it 10!
    return(i)  # returns 10 ... max num lics
        

#---------------------------------- END -------------------------------------

