# 2022 - PANDUIT
#      - Rack Access Control Page Objects
#      - by dantesan-sada--2022-09-14

import time
from datetime import datetime

from selenium.webdriver.common.keys import Keys

from ..utils.selenium_utils import wait_and_get_elem_by
from ..utils.selenium_utils import wait_and_get_elements_by
from ..utils.selenium_utils import enter_text
from ..utils.selenium_utils import click_button
from ..utils.selenium_utils import click_dropdown_item
from ..utils.selenium_utils import click_named_button
from ..utils.selenium_utils import click_a_dropdown_item
from ..utils.selenium_utils import click_aria_label_icon
from ..utils.selenium_utils import verify_element_invisible
from ..utils.selenium_utils import verify_element_visible
from ..utils.selenium_utils import verify_span_label

from ..utils.selenium_utils import ID
from ..utils.selenium_utils import XPATH

from ..utils.automation_utils import write_log
from ..utils.automation_utils import debug_func

#CONSTANTS
ACTIONS = "Actions"
ADD_CARD = "Add Card"
SAVE = "Save"

CARD_ID = "cardid"
USERNAME_ID = "username"
CARD_PIN_ID = "pin"

CARD_ID_SPACES = "    "

FORWARD_TEN = "forward ten" 
BACKWARD_TEN = "back ten" 

MAX_NUM_CARDS_PER_PANEL = 10

CLOSE = "close"

MAX_NUM_FW_10_PRESSED = 19

NO_MORE_CARDS_AFTER_CARD_1 = 2

MAX_FIRST_PAGE_CHECK = 2

# for addind cards
TEXTBOX_ID_NONE = "Card Id textbox is None."
TEXTBOX_USERNM_NONE = "Card User Name textbox is None."
TEXTBOX_PIN_NONE = "Card PIN textbox is None."
RAC_LABEL = "Rack Access Control"

#CONSTANTS


# LOCATORS

ACTIONS_BUTTON_LCTR = "//span[text() = '{0}']".format(ACTIONS)
SAVE_BUTTON_LCTR = "//span[text() = 'Save']"

CARD_ROWS_LCTR = "//tr[@class = 'grommetux-table-row']"

CARD_ID_GIVEN_LCTR = "//td[text() = '{0}']"
#CARD_ID_LCTR = CARD_ROWS_LCTR + CARD_NO_SUB_LCTR

ICONS_SUB_LCTR = "//following-sibling::td[@data-th = 'Actions']"
TRASH_ICON_SUB_LCTR = "//descendant::*[local-name() = 'svg' and @aria-label = 'trash']"
TRASH_ICON_LCTR = CARD_ID_GIVEN_LCTR + ICONS_SUB_LCTR + TRASH_ICON_SUB_LCTR

CARD_ID_LCTR = "//td[@data-th= 'Card Id']"

FORWARD_TEN_LCTR = "//*[local-name()='svg' and @aria-label='{0}']".format(FORWARD_TEN)
BACKWARD_TEN_LCTR = "//*[local-name()='svg' and @aria-label='{0}']".format(BACKWARD_TEN)

NO_CARD_MSG_LCTR = "//div[text()='cards are not available on this page']"

ARIA_CLOSE_LCTR = "//*[local-name()='svg' and @aria-label='close']"

# LOCATORS



now = datetime.now()

curr_date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

class RAC_CLASS:

    MAX_NUM_CARDS = 5 # for now ... 200
    #CARD_NO_PFX = "1"
    USER_NAME_PFX = "user"
    #CARD_PIN_PFX = "1"

    def __init__(self, **kwargs):
        self._card_id = \
            kwargs['card_id'] if 'card_id' in kwargs else "100000"
        self._username = kwargs['username'] if 'username' in kwargs else "user0"
        self._card_pin = kwargs['card_pin'] if 'card_pin' in kwargs else "10000"
        self._start_time = \
        kwargs['start_time'] if 'start_time' in kwargs \
                                 else curr_date_time
        self._expiration_time = \
        kwargs['expiration_time'] if 'expiration_time' in kwargs \
                                 else ""

    def card_id(self, c=None):
        if c:
            self._card_id = c
        return self._card_id

    def username(self, u=None):
        if u:
            self._username = u
        return self._username

    def card_pin(self, p=None):
        if p:
            self._card_pin = p
        return self._card_pin

    def start_time(self, s=None):
        if s:
            self._start_time = s
        return self._start_time

    def expiration_time(self, e=None):
        if e:
            self._expiration_time = e
        return self._expiration_time


def print_rac_obj(o):
    if not isinstance(o, RAC_CLASS):
        raise TypeError('print_rac_obj(): requires RAC_CLASS data.')
    #write_log("{} - {}".format()
    return ('| {}|{}|{}|{}|{} |'.format(o.card_id(), o.username(), o.card_pin(),
            o.start_time(), o.expiration_time()))


# Add carda data/details. - dantesan--sada--20022-09-19
#
#   Press 'back ten' if the no cards message is shown.
#
# driver  - WebDriver
# num_cards - can be None
#
# Returns : list with True, if there is no error
#           [True/False, "Error Message", None]
#         
#
# dantesan--2022-09-19 -add number of card arguments
def create_card_data(driver, num_cards = None):

    if num_cards is None:
        num_cards = RAC_CLASS.MAX_NUM_CARDS

    write_log("CREATE_CARDS ... {0} - Number of cards = {1}".
        format(create_card_data.__name__, num_cards))
    # make sure no cards message is not showing
    backward_ten(driver)

    page_num = MAX_NUM_CARDS_PER_PANEL
    for c in range(num_cards):
        c =c + 1
        # First card should always exist to avoid connecting handle.
        if c == 1:  
           continue

        card_num = "1{:05d}".format(c)
        user_nm = "{0}{1}".format(RAC_CLASS.USER_NAME_PFX, c)
        card_pinum = "{:05d}".format(c)
        card_data = RAC_CLASS(card_id = card_num,  
                             username = user_nm, 
                            card_pin = card_pinum)
        # verify values
        #rac_obj_values = print_rac_obj(card_data)
        #print(rac_obj_values)
                      
        # press Actions and select Add Card
        named_button = click_named_button(driver, ACTIONS)
        if(named_button is None):
            return [False, "{0} button is missing.".format(ACTIONS), None]

        dropdown_item = click_a_dropdown_item(driver, ADD_CARD)
        if(dropdown_item is None):
            return [False, "{0} dropdown item is missing.".format(ADD_CARD), None]

        textbox_id = enter_value(driver, CARD_ID, card_data.card_id())
        if(textbox_id is None):
            return [False, TEXTBOX_ID_NONE, None]

        textbox_usernm = enter_value(driver, USERNAME_ID, card_data.username())      
        if(textbox_usernm is None):
            return [False, TEXTBOX_USERNM_NONE, None]

        textbox_pin = enter_value(driver, CARD_PIN_ID, card_data.card_pin())
        if(textbox_pin is None):
            return [False, TEXTBOX_PIN_NONE, None]

        # press Save
        named_button = click_named_button(driver, SAVE)
        if(named_button is None):
           return [False, "{0} button is missing.".format(SAVE), None]
        time.sleep(5)

        # do not press Close 
        #icon_button = click_aria_label_icon(driver, CLOSE)
        #if(icon_button is None):
        #   return [False, "{0} icon button is missing.".format(CLOSE), None]
        # use wait instead of sleep, though it works!
        #time.sleep(4)
        verify_notice_closed(driver, ARIA_CLOSE_LCTR)

        write_log("{0} - card_id = {1} added.".
            format(create_card_data.__name__, card_num))
        time.sleep(5)
        # FW_10    
        #if(c > page_num):
        #    page_num = page_num + MAX_NUM_CARDS_PER_PANEL
        #    forward_ten(driver)

    write_log("{1} CARDS CREATED ... {0} ---------------------------------".
        format(create_card_data.__name__, num_cards))

    # cards need to go back to 1st page
    driver.refresh()
    write_log("REFRESH PAGE ... {0} ---------------------------------".
        format(create_card_data.__name__))
    time.sleep(20) # 10 -> 20 ... more time for refresh ...
    # make sure refresh is good!
    rac_label = verify_span_label(driver, RAC_LABEL)
    if(rac_label is not None):
        return [True]
    else:
        return [False, "\'{0}\' label is missing.".format(RAC_LABEL), None] 
    


    

# enter text value in Add Card panel - dantesan--sada--20022-09-14
#
# Enter a text into the textbox given the textbox id.
#
# driver  - WebDriver
# textbox_id - element textbox id
# new_text - the text to write in the textbox 
#
# Returns the textbox webelement. 
#
def enter_value(driver, textbox_id, new_text):
    try:
        textbox = wait_and_get_elem_by(driver, ID, textbox_id)
        textbox.click()
        textbox.send_keys(Keys.HOME)
        textbox.send_keys(new_text)
    except:
        write_log("{0} NoneType Textbox: {1}.".
            format(enter_value.__name__, textbox_id))

    return textbox


# Forward 10. - dantesan--sada--20022-10-03
#
#   Press 'forward ten'. Copied from backward_10
#       and modified.
#
# driver  - WebDriver
#
# Returns : none
#
def forward_ten(driver):
    try:
        #make sure 'forward ten' is shown!
        if(verify_element_visible(driver, XPATH, FORWARD_TEN_LCTR)):
            click_aria_label_icon(driver, FORWARD_TEN)  
            write_log("{0} - FORward 10.".
                format(forward_ten.__name__))
    except:
        write_log("{0} NoneType: FORward 10 is missing.".
            format(forward_ten.__name__))
                
    return


# Backward 10. - dantesan--sada--20022-09-22
#
#   Press 'back ten' if the no cards message is shown.
#
# driver  - WebDriver
#
# Returns : none
#
def backward_ten(driver):
    while(verify_element_visible(driver, XPATH, NO_CARD_MSG_LCTR)):
        try:
            #make sure 'back ten' is shown!
            if(verify_element_visible(driver, XPATH, BACKWARD_TEN_LCTR)):
                click_aria_label_icon(driver, BACKWARD_TEN)  
                write_log("{0} - BACKward 10.".
                    format(backward_ten.__name__))
        except:
            write_log("{0} NoneType: BACKward 10 is missing.".
                format(backward_ten.__name__))

    return


#  Get the card web elements. - dantesan--sada--20022-09-21
#    DND - Do Not Delete
#
# get_card_wes
#
# driver  - WebDriver
#
# Returns : the card web elements and None if does/do not exist/s.
#
def get_card_wes(driver):
    try:
        if(verify_element_visible(driver, XPATH, CARD_ID_LCTR)):
            card_id_we = wait_and_get_elements_by(driver, XPATH, CARD_ID_LCTR)
        return card_id_we

    except:
        write_log("{0} - NoneType: Card ID web elements.".
           format(get_card_wes.__name__))

    return None


#  Wait till notice closes. - dantesan--sada--20022-10-05
#    
#
# get_card_wes
#
# driver  - WebDriver
# close_xpath - 
#
# Returns : True if notice is not visible. anymore.
#
def verify_notice_closed(driver, close_xpath):
    while(verify_element_invisible(driver, XPATH, close_xpath) is not True):
        continue
    return True


#  Forward ten or back ten. - dantesan--sada--20022-09-16
#
# check_cards()
#
# driver  - WebDriver
#
# Returns : none
# 
def check_cards(driver):

    no_cards = True
    fw_pressed = 0
    while(no_cards):    
        forward_ten(driver)
        time.sleep(5)
        card_id_wes = get_card_wes(driver)
        if(card_id_wes is not None):
            break
        fw_pressed = fw_pressed + 1
        if(fw_pressed >= MAX_NUM_FW_10_PRESSED):
            break
        write_log("{0} - fw_pressed = {1}, MAX = {2}.".
            format(check_cards.__name__, fw_pressed, MAX_NUM_FW_10_PRESSED))
        if(verify_element_visible(driver, XPATH, NO_CARD_MSG_LCTR)):
            write_log("{0} - NO_CARD_MSG_REACHED.".
                format(check_cards.__name__))
            backward_ten(driver) 
            card_id_wes = get_card_wes(driver)
            break
    
    return card_id_wes


#  Delete Cards with DND list - dantesan--sada--20022-09-16
#    DND - Do Not Delete
#
# delete_cards_with_dnd_list()
#
# driver  - WebDriver
# do_not_delete_list - list of cards not to delete
#
#
# Returns : true
# 
def delete_cards_with_dnd_list(driver, dont_delete_list):

    INDEX_START = 0
    card_id_wes = get_card_wes(driver)
    if(card_id_wes is None):
        return True
    num_cards = len(card_id_wes)
    n = INDEX_START
    # var indicator if 1st page is passed
    first_page_checked = 0

    write_log("DELETE_CARDS ------------------------------------------".
        format(delete_cards_with_dnd_list.__name__))
    while(num_cards > 0):
        card_id = card_id_wes[n].text
        
        # no card id - check if
        if card_id == "":
            card_id_wes = check_cards(driver)
            if(card_id_wes is None):
                return True
            num_cards = len(card_id_wes)
            n = INDEX_START
            continue

        #do not delete =- 1st card now!
        if(card_id in dont_delete_list and first_page_checked == 0):
            first_page_checked = first_page_checked + 1
            n = n + 1
            continue
        elif(card_id in dont_delete_list and 
                num_cards <= NO_MORE_CARDS_AFTER_CARD_1):
            if(first_page_checked == MAX_FIRST_PAGE_CHECK - 1):
                first_page_checked = first_page_checked + 1
                n = n + 1
                continue
            else:    
              break
        elif(card_id in dont_delete_list):
            n = n + 1
            continue

        trash_icon_xpath = CARD_ID_GIVEN_LCTR.format(card_id) + ICONS_SUB_LCTR + TRASH_ICON_SUB_LCTR
        trash_icon = wait_and_get_elem_by(driver, XPATH, trash_icon_xpath)  
        trash_icon.click()
        #driver.refresh()
        # avoid StaleElementReferenceException 
        time.sleep(5)

        # do not press arla-label = 'close' or X mark in notice
        #click_aria_label_icon(driver, CLOSE)
        verify_notice_closed(driver, ARIA_CLOSE_LCTR)

        write_log("{0} - card_id = {1} DELETED.".
            format(delete_cards_with_dnd_list.__name__, card_id))
        # add sleep for the webpage to be able to update.
        time.sleep(5)
        card_id_wes = get_card_wes(driver)
        if(card_id_wes is None):
           return True
        if(card_id_wes is None): # check later if still needed!
            while(True):
                backward_ten(driver)
                card_id_wes = get_card_wes(driver)
                card_id = card_id_wes[0].text
                if(card_id in dont_delete_list):
                    first_page_checked = True
                    break
        num_cards = len(card_id_wes)
        n = INDEX_START
    
    write_log("DELETE_CARDS ... either checked or deleted ------------".
        format(delete_cards_with_dnd_list.__name__))
    return True


# --------------------------------------- END --------------------------------
