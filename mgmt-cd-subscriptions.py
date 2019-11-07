# 2019 - Cigent Technology, Inc.
#      - MSP D3E Subscription: Verify subscription plan buttons.
#      - by dantesan

from selenium import webdriver

from utils.msp_d3e_utils import d3e_trial
from utils.msp_d3e_utils import d3e_standard
from utils.msp_d3e_utils import d3e_premium

driver = webdriver.Firefox()
#driver = webdriver.Chrome()



if __name__ == "__main__":

    d3e_trial(driver)

    d3e_standard(driver)

    d3e_premium(driver)

    driver.quit()

