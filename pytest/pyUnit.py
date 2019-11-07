#!/usr/bin/python

# Copyright 2018 Cigent Technology, Inc.

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

auth = HTTPBasicAuth()
tokenauth = HTTPTokenAuth("Bearer")
multiauth = MultiAuth(auth, tokenauth)
app = Flask(__name__)
CORS(app)
# Lines above are copied from the file (from rsappapi.py 
#  for the example below) that has the function to test.

# https://docs.python.org/2/library/unittest.html - for more info
import unittest

# RSAPPAPI_IMPORTS - import function to test.
from rsappapiFunc import get_scan_alerts
# RSAPPAPI_IMPORTS

OK200 = "[200 OK]"
NF404 = "[404 Not Found]"
LK423 = "[423 Locked]"
BR400 = "[400 Bad Request]"

with app.app_context():
    with current_app.test_request_context():

        class TestRSRA_Functions(unittest.TestCase): #Test_Test_Name( ...

                def test_get_scan_alerts(self): # 'test' should start name 
                    scanAlerts = str(get_scan_alerts("bY9KZyE8jmHv")) 
                    okResp = scanAlerts.find(OK200)
                    self.assertTrue(okResp != -1)
                
                    scanAlerts = str(get_scan_alerts("aDuxNQ8DL38r")) 
                    okResp = scanAlerts.find(LK423)
                    self.assertTrue(okResp != -1)
                
                    scanAlerts = str(get_scan_alerts("initial")) 
                    okResp = scanAlerts.find(LK423)
                    self.assertFalse(okResp == -1)

                    self.assertEqual(str(get_scan_alerts("rsDNEiDBnFND")), '<Response 76 bytes [404 Not Found]>')
                    scanAlerts = str(get_scan_alerts("rsDNEiDBnFND")) 
                    okResp = scanAlerts.find(NF404)
                    self.assertFalse(okResp == -1)
                    self.assertTrue(okResp != -1)

                #   add more test functions here ...

# MAIN
        if __name__ == '__main__':
            unittest.main()
                
        
    
