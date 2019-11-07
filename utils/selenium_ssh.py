#!/usr/bin/python

# Copyright 2018-2019 Cigent Technology, Inc.

# delete if not needed

from sys import argv


# custom files - rsappapi.py uses these files
import constants
import custDevices
import db_connection_cursor
import subscriptionsLicense
import userGroupRole

import unittest


OK200 = "[200 OK]"
NF404 = "[404 Not Found]"
LK423 = "[423 Locked]"
BR400 = "[400 Bad Request]"

# Double ## so that search #@ (/\#@) will not find this ...
##@unittest.skip(SKIP_COMMENT) - makes TEST_.. flag not OK!
# SKIP_RAFG - skip rem_admin_fr_group() test

NONE = "NONE"
TRUE = "TRUE"

def get_user_id(usernm):
    user_tbl = subscriptionsLicense.OthTable("users")
    user_info_lst = user_tbl.getTableData(username=usernm)
    user_info =  user_info_lst[0]
    user_id = user_info["id"]
    return(user_id)
    


def get_verification_code(usernm):
    usr_id = get_user_id(usernm)
    verification_tbl = subscriptionsLicense.OthTable("verification_codes")
    verification_code_lst = verification_tbl.getTableData(user_id=usr_id)
    vc_len = len(verification_code_lst)
    verification_code_elem = verification_code_lst[vc_len - 1]
    verification_code = verification_code_elem["code"]
    return(verification_code)

# MAIN
if __name__ == '__main__':

   if argv[1] == "1":
       verification_code = get_verification_code(argv[2])
       print(verification_code)
        
