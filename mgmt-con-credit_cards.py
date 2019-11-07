# 2019 - Cigent Technology, Inc.
#      - MSP D3E Subscription: Verify all Stripe credit card numbers.
#      - by dantesan

from selenium import webdriver

from utils.msp_d3e_utils import ent_id_and_passwd
from utils.msp_d3e_utils import enter_card_details_and_submit
from utils.msp_d3e_utils import get_usremail
from utils.msp_d3e_utils import d3e_standard
from utils.msp_d3e_utils import VALID_EXP_DT
from utils.msp_d3e_utils import VALID_CVC
from utils.msp_d3e_utils import USRPASSWD
from utils.msp_d3e_utils import FIRST_CREDIT_CARD_NUM



driver = webdriver.Firefox()
#driver = webdriver.Chrome()

CARD_NUMBERS = [ FIRST_CREDIT_CARD_NUM,
                 "4000056655665556",
                 "5555555555554444",
                 "2223003122003222",
                 "5200828282828210",
                 "5105105105105100",
                 "378282246310005",
                 "371449635398431",
                 "6011111111111117",
                 "6011000990139424",
                 "3566002020360505"] 

NZ_CARD_NUMS = [ "30569309025904",
                 "38520000023237",
                  "6200000000000005"]

if __name__ == "__main__":

    # Use only one user email for now ...
    usremail = get_usremail()
    for card_num in CARD_NUMBERS:
        d3e_standard(driver)
        ent_id_and_passwd(driver, usremail, USRPASSWD)
        enter_card_details_and_submit(driver, card_num, VALID_EXP_DT, VALID_CVC, True)

    for card_num in NZ_CARD_NUMS:
        d3e_standard(driver)
        ent_id_and_passwd(driver, usremail, USRPASSWD)
        enter_card_details_and_submit(driver, card_num, VALID_EXP_DT, VALID_CVC, False)

    driver.close()


