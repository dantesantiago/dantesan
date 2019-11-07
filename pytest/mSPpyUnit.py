#!/usr/bin/python

# Copyright 2018-2019 Cigent Technology, Inc.

# delete if not needed
from contextlib import contextmanager
from datetime import date, timedelta
from email.mime.text import MIMEText
from flask import abort, Flask, jsonify, redirect, request, redirect, current_app
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from flask_restful import reqparse
from passlib.hash import bcrypt
import base64
import datetime
import dateparser
import json
import jwt
import mysql.connector as mariadb
import MySQLdb
import os
import random
import requests
import smtplib
import string
import sys
import timestring
import zerorpc

# custom files - rsappapi.py uses these files
import constants
import stripe_process
import custDevices

app = Flask(__name__)
CORS(app)
auth = HTTPBasicAuth()
tokenauth = HTTPTokenAuth("Bearer")
multiauth = MultiAuth(auth, tokenauth)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "rs_auth_key")
# Lines above are copied from the file (from rsappapi.py 
#  for the example below) that has the function to test.

# https://docs.python.org/2/library/unittest.html - for more info
import unittest

# RSAPPAPI_IMPORTS - import function to test.
from rsappapi import list_sentinels
from rsappapi import list_sub_users
from rsappapi import set_sentinel_userid

from rsappapi import create_group
from rsappapi import add_admin_to_group
#from rsappapi import add_device_to_group - IAD
from rsappapi import add_device_to_group

from rsappapi import check_sentinel_authority

from rsappapi import delete_group
from rsappapi import rem_admin_fr_group
#from rsappapi import rem_sentinel_fr_group - IAD
from rsappapi import rem_device_fr_group

from rsappapi import set_user_level_id
from rsappapi import chk_if_group_exists

from rsappapi import get_alerts

from rsappapi import get_master_tech_lvl_devices

from rsappapi import check_sentinel_online
from rsappapi import create_user
from rsappapi import ver_level_1_usr_id_grp_lvl_1


from rsappapi import getCustLevelDvcs
from rsappapi import getDeviceHosts

from rsappapi import update_user
from rsappapi import get_sentinel

from rsappapi import list_admin_devices2
from rsappapi import get_admin_groups

from rsappapi import getAllAdminsInGroup

from rsappapi import getAllAdminsInMSP

# RSAPPAPI_IMPORTS

OK200 = "[200 OK]"
NF404 = "[404 Not Found]"
LK423 = "[423 Locked]"
BR400 = "[400 Bad Request]"

# Double ## so that search #@ (/\#@) will not find this ...
##@unittest.skip(SKIP_COMMENT) - makes TEST_.. flag not OK!
# SKIP_RAFG - skip rem_admin_fr_group() test

NONE = "NONE"
TRUE = "TRUE"

with app.app_context():
    #print current_app.name;
    with current_app.test_request_context():

        class TestRSRA_Functions(unittest.TestCase): #Test_Test_Name( ...

                @unittest.skip("Do not do TEST_LS")
                def test_list_sentinels(self): # 'test' should start name 

                    #self.assertEqual(str(list_sentinels()), "<Response 3 bytes [200 OK]>" ); # usr = "Benkieshome" #MSP (usr_id = 18) - lvl_1_usr_id
                    #self.assertEqual(str(list_sentinels()), "<Response 612 bytes [200 OK]>" ); # usr = "test" #MSP (usr_id = 55) - lvl_2_usr_id
                    #self.assertEqual(str(list_sentinels()), "<Response 617 bytes [200 OK]>" ); # usr = "dantesan" #MSP (usr_id = 56) - lvl_3_usr_id
                    scanAlerts = str(list_sentinels()) 
                    okResp = scanAlerts.find(OK200)
                    self.assertTrue(okResp != -1)
            
                @unittest.skip("Do not do TEST_LU")
                def test_list_sub_users(self): # 'test' should start name 

                    scanAlerts = str(list_sub_users()) 
                    okResp = scanAlerts.find(OK200)
                    self.assertTrue(okResp != -1)
                    #self.assertEqual(str(list_sub_users()), "<Response 3 bytes [200 OK]>" ); # usr = "Benkieshome" #MSP (usr_id = 18) - lvl_1_usr_id
                    #self.assertEqual(str(list_sub_users()), "<Response 612 bytes [200 OK]>" ); # usr = "test" #MSP (usr_id = 55) - lvl_2_usr_id
                    #self.assertEqual(str(list_sub_users()), "<Response 617 bytes [200 OK]>" ); # usr = "dantesan" #MSP (usr_id = 56) - lvl_3_usr_id
            
                @unittest.skip("Do not do TEST_SU")
                def test_set_sentinel_userid(self): # 'test' should start name 
    
                    self.assertEqual(str(set_sentinel_userid("ZQ5jmN2elTkB")), "<Response 3 bytes [200 OK]>" );
                    scanAlerts = str(set_sentinel_userid("ZQ5jmN2elTkB")) 
                    okResp = scanAlerts.find(OK200)
                    self.assertTrue(okResp != -1)
    
                @unittest.skip("Do not do TEST_AATG")
                def test_add_admin_to_group(self): # 'test' should start name 
    
                    # VL1GL1 test - comment out
                                                                  # user_id = 1
                    #self.assertEqual(str(add_admin_to_group(1, "admin")), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(add_admin_to_group(14, "cprtools")), "<Response 5 bytes [200 OK]>" );
                    #                                              # user_id = 18
                    #self.assertEqual(str(add_admin_to_group(2, "Benkieshome")), "<Response 5 bytes [200 OK]>" );
                    #                                              # user_id = 8
                    #self.assertEqual(str(add_admin_to_group(1, "devadmin")), "<Response 5 bytes [200 OK]>" );
                    #                                           # user_id = 3
                    #self.assertEqual(str(add_admin_to_group(1, "gscasny")), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(add_admin_to_group(2, "gscasny")), "<Response 5 bytes [200 OK]>" );

                    #self.assertNotEqual(str(add_admin_to_group(1, "dantesan")), "<Response 5 bytes [200 OK]>" );
                    # VL1GL1 test - comment out

                    # IAD test
                    #scanAlerts = str(add_admin_to_group(1, "dantesan", constants.CYBEP)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added

                    #MSPRSAPPAPI_PYUNIT - ASTG_IAD tested here, too!
                    #scanAlerts = str(add_admin_to_group(1, "recondev", constants.ENTRS)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added


                    #AATG_IAD__ASTG_IAD__GETDEVICES_ADMIN_ID__TEST 
                    # When no admin_id for a group_id in device-group table list, VL1GL1 needs to be disabled!
                    #scanAlerts = str(add_admin_to_group(13, "dantesan", constants.RECON)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added

                    #scanAlerts = str(add_admin_to_group(13, "dantesan", constants.ENTRS)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added

                    #scanAlerts = str(add_admin_to_group(13, "dantesan", constants.CYBEP)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added

                    #scanAlerts = str(add_admin_to_group(13, "dantesan", constants.CIGDV)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added

                    # allowGL2 = True - bypass VL1GL1
                    #scanAlerts = str(add_admin_to_group(8, "dantesan", constants.CIGDV, True)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added

                    #BRUCE_REQUEST
                    #scanAlerts = str(add_admin_to_group(18, "bruce", 18, constants.RECON, True)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added

                    #BOINK_IF_NO_DEVICE
                    #scanAlerts = str(add_admin_to_group(18, "bruce", 18, constants.CYBEP, True)) # LEVEL_1_USR_ID
                    # def add_admin_to_group(groupid, usernm, group_id_1,  dvc_typ, allowGL2):
                    scanAlerts = str(add_admin_to_group(1, "donaldduck", NONE, NONE, TRUE)) # LEVEL_1_USR_ID
                    okResp = scanAlerts.find(OK200) 
                    self.assertTrue(okResp != -1) # added


                @unittest.skip("SKIP_RAFG")
                def test_rem_admin_fr_group(self): # 'test' should start name 
                                                                  # user_id = 18
                    #self.assertEqual(str(rem_admin_fr_group(1, "Benkieshome")), "<Response 5 bytes [200 OK]>" );
                                                               # user_id = 3
                    # VL1GL1 test - comment out
                    #self.assertEqual(str(rem_admin_fr_group(1, "devadmin")), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(rem_admin_fr_group(1, "gscasny")), "<Response 5 bytes [200 OK]>" );
                    # VL1GL1 test - comment out

                    # RAFG-IAD test
                    #self.assertEqual(str(rem_admin_fr_group(1, "dantesan", constants.CYBEP)), "<Response 5 bytes [200 OK]>" );
                    #scanAlerts = str(rem_admin_fr_group(1,"Benkieshome")) # LEVEL_1_USR_ID
                    #print "scanAlerts = <%s>" % scanAlerts
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) #removed

                    #scanAlerts = str(rem_admin_fr_group(1,"test")) # LEVEL_2_USR_ID
                    #okResp = scanAlerts.find(OK200)
                    #self.assertTrue(okResp == -1)

                    #MSPRSAPPAPI_PYUNIT - RSFG_IAD tested here, too!
                    #scanAlerts = str(rem_admin_fr_group(1,"recondev", constants.ENTRS)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added

                    #BOINK_IF_NO_DEVICE
                    #scanAlerts = str(rem_admin_fr_group(18, "bruce", 18, constants.CYBEP, True)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added

                    #BOINK_IF_NO_DEVICE
                    #def rem_admin_fr_group(groupid, usernm, group_id_1,  dvc_typ, allowGL2):
                    #scanAlerts = str(rem_admin_fr_group(84, "dantesan", NONE, NONE, True)) 
                    scanAlerts = str(rem_admin_fr_group(1, "donaldduck", NONE, NONE, True)) 
                    okResp = scanAlerts.find(OK200) 
                    self.assertTrue(okResp != -1) # added


                @unittest.skip("SKIP_ASTG")
                def test_add_device_to_group(self): # 'test' should start name 
                    #"CFISFPrg3Vlo" - LEVEL 2 - rs_id = 86
                    #self.assertEqual(str(add_device_to_group( "CFISFPrg3Vlo", 1)), "<Response 5 bytes [200 OK]>" );
                    #"aTCYdN4L95gE" - LEVEL 1 - rs_id = 74
                    #self.assertEqual(str(add_device_to_group( "aTCYdN4L95gE", 1)), "<Response 5 bytes [200 OK]>" );
                    #LVL_1_USR_ID - mSPTest:usr = BenkiesHome, LVL_2_USR_ID - mSPTest:usr = test
                    #"ZQ5jmN2elTkB" - LEVEL 3 - rs_id = 89
                    #self.assertEqual(str(add_device_to_group( "ZQ5jmN2elTkB", 1)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(add_device_to_group( "ZQ5jmN2elTkB", 2)), "<Response 5 bytes [200 OK]>" );
                    #"OPgBjYjvR2J1" - LEVEL 1 = rs_id = 70

                    # VL1GL1 test 
                    #self.assertEqual(str(add_device_to_group( "OPgBjYjvR2J1", 1)), "<Response 5 bytes [200 OK]>" );
                    #scanAlerts = str(add_device_to_group( "ZQ5jmN2elTkB", 13)) # Fort Myers Office Of The Mayor
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added
    
                    # USR_STRY_526_ALLOWGL2, ASTG_ALLOWGL2_NEEDED
                    # [u'aTCYdN4L95gE', u'Z7uz8jMt7q7v', u'ZQ5jmN2elTkB']
                    # admin-group record exists
                    #scanAlerts = str(add_device_to_group( "ZQ5jmN2elTkB", 8, "dantesan", constants.CIGDV)) 
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added
    
                    #scanAlerts = str(add_device_to_group( "aTCYdN4L95gE", 8, "dantesan", constants.CIGDV)) 
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added
    
                    #scanAlerts = str(add_device_to_group( "Z7uz8jMt7q7v", 8, "dantesan", constants.CIGDV)) 
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added
    
                    # Real Test of USR_STRY_526_ALLOWGL2, ASTG_ALLOWGL2_NEEDED
                    # admin-group record DNE
                    #scanAlerts = str(add_device_to_group( "ZQ5jmN2elTkB", 2, "dantesan", constants.CIGDV, True)) 
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added
    
                    #scanAlerts = str(add_device_to_group( "aTCYdN4L95gE", 2, "dantesan", constants.CIGDV, True)) 
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added
    
                    #scanAlerts = str(add_device_to_group( "Z7uz8jMt7q7v", 2, "dantesan", constants.CIGDV, True))
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added
    
                    #scanAlerts = str(add_device_to_group( "Z7uz8jMt7q7v", 1, "dantesan", constants.CIGDV, True)) 
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp == -1) # added

                    ##username = None
                    #scanAlerts = str(add_device_to_group( "Z7uz8jMt7q7v", 1, None, constants.CIGDV, True)) 
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # Originally, == and thought to error out, but True was not deleted! "Z7uz8jMt7q7v" added!

                    # Test when allowGL2 != True
                    scanAlerts = str(add_device_to_group( "ZQ5jmN2elTkB", 1, None, constants.CIGDV)) 
                    okResp = scanAlerts.find(OK200) 
                    self.assertTrue(okResp == -1) # added

    

            
    
                @unittest.skip("SKIP_RSFG")
                def test_rem_sentinel_fr_group(self): # 'test' should start name 
                    #"aTCYdN4L95gE" - LEVEL 1
                    #self.assertEqual(str(rem_sentinel_fr_group( "aTCYdN4L95gE", 1)), "<Response 5 bytes [200 OK]>" );
                    #"CFISFPrg3Vlo" - LEVEL 2
                    #self.assertEqual(str(rem_sentinel_fr_group( "CFISFPrg3Vlo", 1)), "<Response 5 bytes [200 OK]>" );
                    #"ZQ5jmN2elTkB" - LEVEL 3
                    #self.assertEqual(str(rem_sentinel_fr_group( "ZQ5jmN2elTkB", 1)), "<Response 5 bytes [200 OK]>" );

                    # VL1GL1 test
                    #scanAlerts = str(rem_sentinel_fr_group( "ZQ5jmN2elTkB", 2)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # removed

                    #MSPRSAPPAPI_PYUNIT
                    #scanAlerts = str(rem_device_fr_group("ZQ5jmN2elTkB", 1, None, constants.CIGDV)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added

                    #scanAlerts = str(rem_device_fr_group("ZQ5jmN2elTkB", 1, "dantesan", constants.CIGDV)) # LEVEL_1_USR_ID
                    #okResp = scanAlerts.find(OK200) 
                    #self.assertTrue(okResp != -1) # added

    
                    #WRONG_LVL_ID
                    scanAlerts = str(rem_device_fr_group("CFISFPrg3Vlo", 1, "PyUnitUser", constants.CIGDV)) # LEVEL_1_USR_ID
                    okResp = scanAlerts.find(OK200) 
                    self.assertTrue(okResp == -1) # added

                @unittest.skip("SKIP_CSA")
                def test_check_sentinel_authority(self): # 'test' should start name 
                    # SET 1 ------------
                    #LVL_1_USR_ID
                    self.assertEqual(str(check_sentinel_authority( "ZQ5jmN2elTkB", 3)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(check_sentinel_authority( "aTCYdN4L95gE", 18)), "<Response 5 bytes [200 OK]>" );
                    #LVL_2_USR_ID
                    self.assertEqual(str(check_sentinel_authority( "ZQ5jmN2elTkB", 55)), "<Response 5 bytes [200 OK]>" );
                    #USER_ID
                    self.assertEqual(str(check_sentinel_authority( "ZQ5jmN2elTkB", 56)), "<Response 45 bytes [200 OK]>" );
                    #devadmin id = 8, gscasny id = 3
                    self.assertEqual(str(check_sentinel_authority( "ZQ5jmN2elTkB", 8)), "<Response 76 bytes [423 Locked]>" );
                    # SET 1 ------------

                    # SET 2 ------------
                    # userid = 3 (LVL_1_USR_ID)
                    self.assertEqual(str(check_sentinel_authority( "2jseTSGTC2ND", 3)), "<Response 5 bytes [200 OK]>" );
                    # userid = 17 (LVL_2_USR_ID)
                    self.assertEqual(str(check_sentinel_authority( "KkN4UGT3plDI", 17)), "<Response 5 bytes [200 OK]>" );
                    # userid = 8 (LVL_1_USR_ID)
                    self.assertEqual(str(check_sentinel_authority( "KkN4UGT3plDI", 8)), "<Response 5 bytes [200 OK]>" );
                    #LVL_2_USR_ID not for the userid = 17
                    self.assertEqual(str(check_sentinel_authority( "KkN4UGT3plDI", 55)), "<Response 76 bytes [423 Locked]>" );
                    # SET 2 ------------
    
                    # SET 3 ------------
                    # LVL_1_USR_ID = 18
                    self.assertEqual(str(check_sentinel_authority( "aDuxNQ8DL38r", 18)), "<Response 5 bytes [200 OK]>" );
                    # LVL_2_USR_ID = 55
                    self.assertEqual(str(check_sentinel_authority( "aDuxNQ8DL38r", 55)), "<Response 5 bytes [200 OK]>" );
                    # USRID = 9
                    self.assertEqual(str(check_sentinel_authority( "aDuxNQ8DL38r", 9)), "<Response 5 bytes [200 OK]>" );
                    # LVL_3_USR_ID not userid
                    self.assertEqual(str(check_sentinel_authority( "aDuxNQ8DL38r", 56)), "<Response 76 bytes [423 Locked]>" );
                    # SET 3 ------------
    
                @unittest.skip("Do not do TEST_CGRP")
                def test_create_group(self): # 'test' should start name 
                    #self.assertEqual(str(create_group("NONE", "NONE")), "<Response 5 bytes [200 OK]>" );
                    self.assertEqual(str(create_group("dantesan", "NONE")), "<Response 5 bytes [200 OK]>" ); #no GUFA call,
                                                                                                             # PYUNIT = False ok!
    
                @unittest.skip("SKIP_DG")
                def test_delete_group(self): # 'test' should start name 
                    self.assertEqual(str(delete_group()), "<Response 5 bytes [200 OK]>" );
    

                @unittest.skip("SKIP_SULI")
                def test_set_user_level_id(self): # 'test' should start name 
                    # user_id =  3 - LVL_1_USR_ID
                    # user_id = 18 - LVL_1_USR_ID
                    # user_id = 55 - LVL_2_USR_ID
                    # user_id = 56 - LVL_3_USR_ID
                    #self.assertEqual(str(set_user_level_id("gscasny2", constants.LEVEL_ID_01)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("brettlanglinais", constants.LEVEL_ID_02)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("recondev", constants.LEVEL_ID_03)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("carlrecon", constants.LEVEL_ID_03, "test")), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("rayrecon", constants.LEVEL_ID_02)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("cprtools", constants.LEVEL_ID_02)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("cprtools", constants.LEVEL_ID_01)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("odstest", constants.LEVEL_ID_03, "rayrecon")), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("carlrecon", constants.LEVEL_ID_03, "test")), "<Response 5 bytes [200 OK]>" );

                    # re-running these lines will send: ACTIVE_DEVICE_GROUP_EXISTS
                    #self.assertEqual(str(set_user_level_id("cprtools", constants.LEVEL_ID_01, 15, None)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("brettlanglinais", constants.LEVEL_ID_02, 16, None)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("odstest", constants.LEVEL_ID_03, 16, "rayrecon")), "<Response 5 bytes [200 OK]>" );

                    #self.assertEqual(str(set_user_level_id("recondev", constants.LEVEL_ID_01, 14)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("Benkieshome", constants.LEVEL_ID_01, 1, None)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("bchmtn", constants.LEVEL_ID_03, 16, "rayrecon")), "<Response 5 bytes [200 OK]>" );

                    #SULI_IAD - NO_ERROR
                    #self.assertEqual(str(set_user_level_id("recondev", constants.LEVEL_ID_01, 13, constants.RECON)), "<Response 5 bytes [200 OK]>" );
                    #self.assertEqual(str(set_user_level_id("recondev", constants.LEVEL_ID_01, 13, constants.CYBEP)), "<Response 5 bytes [200 OK]>" );
                    # UNF_WLI_ERR - set curr_username in GUFA - use above tests ...

                    # username - UNF
                    #self.assertEqual(str(set_user_level_id("unf", constants.LEVEL_ID_01, 13, constants.CYBEP)), "<Response 5 bytes [200 OK]>" );

                    # lvl_2_usr_id - LVL2_USER_NOT_FOUND
                    #self.assertEqual(str(set_user_level_id("cprtools", constants.LEVEL_ID_02, 13, constants.CYBEP, "unf")), "<Response 5 bytes [200 OK]>" );
                    # lvl_2_usr_id - WLI ... not LVL_2_USR_ID
                    #self.assertEqual(str(set_user_level_id("cprtools", constants.LEVEL_ID_02, 13, constants.CYBEP, "carlrecon")), "<Response 5 bytes [200 OK]>" );
                    # Dave Test
                    #self.assertEqual(str(set_user_level_id("cprtools", constants.LEVEL_ID_02, 13, constants.CYBEP, "carlrecon")), "<Response 5 bytes [200 OK]>" );
                    #https://rsappapi-dev.reconsentinel.com/user/register/lvl_id/davetest2/2/1/None/None/None
                    #def set_user_level_id(username, new_lvl_id, group_id, dvc_typ=None, lvl_2_username=None, grp_id_1=None):

                    #https://rsappapi-dev.reconsentinel.com/user/register/lvl_id/davetest2/2/13/None/None/None
                    #scanAlerts = str(set_user_level_id("davetest2", constants.LEVEL_ID_02, 2, 13, None, None, None)) 

                    #https://rsappapi-dev.reconsentinel.com/user/register/lvl_id/davetest2/1/1/None/None/None
                    #print "Run davetest"
                    #scanAlerts = str(set_user_level_id("davetest2", constants.LEVEL_ID_01, 1, None, None, None)) 
                    #okResp = scanAlerts.find(OK200)
                    #self.assertTrue(okResp != -1) 


                    #https://rsappapi-dev.reconsentinel.com/user/register/lvl_id/davetest3/2/1/None/None/None
                    #scanAlerts = str(set_user_level_id("davetest3", constants.LEVEL_ID_02, 1, None, None, None)) 
                    #scanAlerts = str(set_user_level_id("davetest3", constants.LEVEL_ID_02, 1, "", "davetest3", "")) 

                    #5393 def set_user_level_id(username, new_lvl_id, group_id, dvc_typ, lvl_2_username, grp_id_1):
                    # LVL_2
                    #scanAlerts = str(set_user_level_id("PyUnitUser", constants.LEVEL_ID_02, 1, "NONE", "PyUnitUser", "NONE")) 
                    # LVL_1
                    #scanAlerts = str(set_user_level_id("PyUnitUser", constants.LEVEL_ID_01, 1, "NONE", "NONE", "NONE")) 
                    # LVL_3
                    scanAlerts = str(set_user_level_id("PyUnitUser", constants.LEVEL_ID_03, 1, "NONE", "mark", "NONE")) 
                    okResp = scanAlerts.find(OK200)
                    self.assertTrue(okResp != -1) 

                @unittest.skip("SKIP_CIGE")
                def test_chk_if_group_exists(self): # 'test' should start name 
                    #print "TEST: %s " % self
                    self.assertEqual(str(chk_if_group_exists(1)), "<Response 5 bytes [200 OK]>" );
                    self.assertEqual(str(chk_if_group_exists(2)), "<Response 5 bytes [200 OK]>" );
                    self.assertEqual(str(chk_if_group_exists(8)), "<Response 5 bytes [200 OK]>" );
                    self.assertEqual(str(chk_if_group_exists(13)), "<Response 5 bytes [200 OK]>" );

                    self.assertNotEqual(str(chk_if_group_exists(3)), "<Response 5 bytes [200 OK]>" );
                    self.assertNotEqual(str(chk_if_group_exists(4)), "<Response 5 bytes [200 OK]>" );
    
                @unittest.skip("SKIP_GTAL") 
                def test_get_alerts(self): # 'test' should start name 
                    #print "TEST: %s " % self
                    self.assertEqual(str(get_alerts("H8rJ07zX9MAj")), "<Response 5 bytes [200 OK]>" );

                @unittest.skip("SKIP_MTLD") 
                def test_get_master_tech_lvl_devices(self): # 'test' should start name 
                    #print "TEST: %s " % self
                    #self.assertEqual(str(get_master_tech_lvl_devices()), "<Response 5 bytes [200 OK]>" );
                    scanAlerts = str(get_master_tech_lvl_devices()) 
                    okResp = scanAlerts.find(OK200)
                    self.assertTrue(okResp != constants.STR_NOT_FOUND)

                @unittest.skip("SKIP_CSO") 
                def test_check_sentinel_online(self): # 'test' should start name 
                    #print "TEST: %s " % self
                    self.assertEqual(str(check_sentinel_online("ZQ5jmN2elTkB")), "<Response 5 bytes [200 OK]>" );

                @unittest.skip("SKIP_CU")
                def test_create_user(self): # 'test' should start name 
                    self.assertEqual(str(create_user()), "<Response 5 bytes [200 OK]>" );
    
                @unittest.skip("SKIP_VL1GL1")
                def test_ver_level_1_usr_id_grp_lvl_1(self): # 'test' should start name 
                    self.assertEqual(str(ver_level_1_usr_id_grp_lvl_1(8, 1, "admin_group")), "<Response 5 bytes [200 OK]>" );
                    self.assertEqual(str(ver_level_1_usr_id_grp_lvl_1(3, 1, "admin_group")), "<Response 5 bytes [200 OK]>" );
                    self.assertEqual(str(ver_level_1_usr_id_grp_lvl_1(56, 1, "admin_group")), "ACTIVE_LVL_1_USER_GROUP_DOES_NOT_EXIST" );
                    #scanAlerts = str(ver_level_1_usr_id_grp_lvl_1("ZQ5jmN2elTkB")) 
                    #okResp = scanAlerts.find(OK200)
                    #self.assertTrue(okResp != -1)
    
                @unittest.skip("SKIP_GCL") 
                def test_getCustLevelDvcs(self): # 'test' should start name 
                    #print "TEST: %s " % self
                    #self.assertEqual(str(getCustLevelDvcs(1, 56)), "<Response 5 bytes [200 OK]>" ); 
                    #scanAlerts = str(getCustLevelDvcs(1, 56))
                    #okResp = scanAlerts.find(OK200)
                    #self.assertTrue(okResp != constants.STR_NOT_FOUND)

                    #GETDEVICE_ADMIN_ID	
                    #scanAlerts = str(getCustLevelDvcs(13, 56))
                    #okResp = scanAlerts.find(OK200)
                    #self.assertTrue(okResp != constants.STR_NOT_FOUND)

                    # USR_STRY_557
                    #scanAlerts = str(getCustLevelDvcs(13, 9))
                    #scanAlerts = str(getCustLevelDvcs(44, 56))
                    scanAlerts = str(getCustLevelDvcs(43, 56))
                    #scanAlerts = str(getCustLevelDvcs(13, 9))
                    okResp = scanAlerts.find(OK200)
                    self.assertTrue(okResp != constants.STR_NOT_FOUND)

                @unittest.skip("SKIP_GDH") 
                def test_getDeviceHosts(self): # 'test' should start name 
                    #print "TEST: %s " % self
                    self.assertEqual(str(getDeviceHosts("ZQ5jmN2elTkB").response), "<Response 5 bytes [200 OK]>" );
                    #scanAlerts = str(getDeviceHosts("ZQ5jmN2elTkB").response)
                    #okResp = scanAlerts.find(OK200)
                    #self.assertTrue(okResp != constants.STR_NOT_FOUND)


                @unittest.skip("SKIP_UU")  # USR_STRY_547 - Now assigned to Damian ...
                def test_update_user(self): # 'test' should start name 
                    self.assertEqual(str(update_user("PyUnitUser")), "<Response 5 bytes [200 OK]>" );
    
                @unittest.skip("SKIP_GS")  # USR_STRY_560
                def test_get_sentinel(self): # 
                    #self.assertEqual(str(get_sentinel("ZQ5jmN2elTkB")), "<Response 5 bytes [200 OK]>" ); # <Response 580 bytes [200 OK]>
                    scanAlerts = str(get_sentinel("ZQ5jmN2elTkB")) 
                    okResp = scanAlerts.find(OK200)
                    self.assertTrue(okResp != -1)
    
                @unittest.skip("SKIP_LAD2")  # USR_STRY_571
                def test_list_admin_devices2(self): # 
                    #self.assertEqual(str(list_admin_devices2("dantesan", "sentinels")), "<Response 5 bytes [200 OK]>" ); # <Response 580 bytes [200 OK]>
                    #scanAlerts = str(list_admin_devices2("dantesan", "sentinels")) 
                    #scanAlerts = str(list_admin_devices2("recondev", "sentinels")) 
                    scanAlerts = str(list_admin_devices2("glass", "sentinels")) 
                    okResp = scanAlerts.find(OK200)
                    self.assertTrue(okResp != -1)
    
                #@unittest.skip("SKIP_GGRP")  # USR_STRY_552
                def test_get_admin_groups(self): # 
                    #self.assertEqual(str(get_admin_groups("dantesan")), "<Response 5 bytes [200 OK]>" ); # <Response 580 bytes [200 OK]>
                    #scanAlerts = str(get_admin_groups("dantesan", constants.RECON)) 
                    #scanAlerts = str(get_admin_groups(None, None)) 
                    scanAlerts = str(get_admin_groups("recondev", "NONE")) 
                    #scanAlerts = str(get_admin_groups("glass", "NONE")) 
                    okResp = scanAlerts.find(OK200)
                    self.assertTrue(okResp != -1)
    

                @unittest.skip("SKIP_GGA")  # USR_STRY_638
                def test_getAllAdminsInGroup(self): # 
                    scanAlerts = str(getAllAdminsInGroup(1)) 
                    nOkResp = scanAlerts.find("GROUP")
                    self.assertTrue(nOkResp == -1)
    
                @unittest.skip("SKIP_GAM")  # USR_STRY_640
                def test_getAllAdminsInGroup(self): # 
                    scanAlerts = str(getAllAdminsInMSP()) 
                    nOkResp = scanAlerts.find("GROUP")
                    self.assertTrue(nOkResp == -1)
    
    

# MAIN
        if __name__ == '__main__':
            unittest.main()
                
        
