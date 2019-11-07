# 2019 - Cigent Technology, Inc.
#      - MSP D3E Subscription: Verify invalid values in Stripe.
#      - by dantesan

from selenium import webdriver

from utils.msp_d3e_utils import ent_id_and_passwd
from utils.msp_d3e_utils import enter_card_details_and_submit
from utils.msp_d3e_utils import get_usremail
from utils.msp_d3e_utils import d3e_standard

driver = webdriver.Firefox()
#driver = webdriver.Chrome()

USRPASSWD = "Cigent0813"

INVALID_EXP_DT = "MM/YY"  
INVALID_CVC    = "SWQ"
VALID_ZIP      = "33901"
FIRST_CREDIT_CARD_NUM = "4242424242424242"


if __name__ == "__main__":

    d3e_standard(driver)
    usremail = get_usremail()
    ent_id_and_passwd(driver, usremail, USRPASSWD)
    card_num = FIRST_CREDIT_CARD_NUM
    enter_card_details_and_submit(driver, card_num, True, INVALID_EXP_DT, INVALID_CVC)

    driver.close()


