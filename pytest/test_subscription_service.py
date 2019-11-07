
import pytest
import json
import datetime
import jwt

from flask import jsonify
import sys

from logger_module import get_logger

import common
import ctmc_flask_main as flask_main

from tests.support_tests_module import standard
from tests.support_tests_module import d3e_init

# from common import response
from common import mdb, nonone, create_response
from constants import BAD_REQUEST_400
from constants import CONFLICT_409
from constants import CREATED_201
from constants import FORBIDDEN_403
from constants import PLAN_STANDARD_D3E_TRIAL
from constants import PLAN_STANDARD_D3E_YEARLY
from constants import LICENSE_STATUS_VALID
from constants import LICENSE_TYPE_INVALID
from constants import LICENSE_TIER_STANDARD
from constants import LICENSE_TYPE_TIME_LIMITED
from constants import NOT_AUTHORIZED_401
from constants import NOT_FOUND_404
from constants import OK_200
from constants import PAYMENT_REQ_402
from constants import TOKEN_INV_FAIL
from constants import TOKEN_SIG_FAIL
from constants import USER_EXISTS
from constants import D3E_GROUP_NAME
from constants import D3E_ACTIVATION_KEY
from constants import JWT_DECODE_ALGORITHM

from common import mdb
from db_connection_cursor import get_db_connection
from db_connection_cursor import get_db_cursor
from common import make_response
from common import create_response

from subscriptionsLicense import Subscriptions
from subscriptionsLicense import Licenses
from subscriptionsLicense import ActivationToken
from userGroupRole import dvcUser
from userGroupRole import dvcGroup

from subscriptionsLicense import OthTable
# import rsappapi

from test_flask import login
from test_flask import Headers

from tools.prime_group import create_prime_group

from support_tests_module import d3e_init

# import rsappapi  # /activate


client = flask_main.app.test_client()

# table names
subscriptions = "subscriptions"
licenses = "licenses"

order_number = 9999
plan_id_light = PLAN_STANDARD_D3E_TRIAL
plan_id_full = PLAN_STANDARD_D3E_YEARLY

USR = 0
GRP = 1
SUB = 2

USRNAME = "ilny@cigent.com"
GRPNAME = "ilny@cigent.com"
STRIPE_SUBSCRIPTION_PREFIX = "sub_"
PASSWD = "cigent"

ACTIVATION_TOKEN = ("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
                    "eyJleHAiOjE5NjM0Njk1MDAsInN5cyI6IjMxMzM3aDR4MHIiLCJtYW4iOiJNSUNST1NPRlQs"
                    "IElOQyIsIm1vZCI6IlN1cmZhY2UgQm9vayIsImNtcCI6IjMxMzM3IGg0eDByIn0."
                    "UAasJMr6fubjfsdtAMNnN6wROCEh8eoh_8A81AXtsN4")


@pytest.fixture
def del_all_subscription_info():

    try:

        # commented out for now because of no new token
        # Subscriptions.deleteSubscriptions()
        # Licenses.deleteLicenses()

        _user = dvcUser()
        _user_data_list = _user.getUserInfo(username=USRNAME)
        if len(_user_data_list) != 0:
            _user_data = _user_data_list[0]
            subscription_user_id = _user_data["id"]
            _user.delDvcUser(username=USRNAME)
        else:
            subscription_user_id = 0

        grp = dvcGroup()
        grp_data_list = grp.getGroupInfo(name=GRPNAME)
        if len(grp_data_list) != 0:
            grp.delDvcGroup(name=GRPNAME)

        # delete subscription
        _subscription = OthTable("subscriptions")
        if subscription_user_id != 0:
            _subscription.deleteData(user_id=subscription_user_id)

        grp_data_list = grp.getGroupInfo(name="D3E")
        if len(grp_data_list) != 0:
            grp.delDvcGroup(name="D3E")

        _user_data_list = _user.getUserInfo(username="d3e_master")
        if len(_user_data_list) != 0:
            _user.delDvcUser(username="d3e_master")

        create_prime_group('D3E', 'd3e_master', 'lost')

    except Exception as e:
        raise e

    return


def get_subscription_info():  # need to convert to list

    try:

        information_list = []

        # get user info
        usr = dvcUser()
        usrInfo_list = usr.getUserInfo(username=USRNAME)
        usrInfo = usrInfo_list[0]
        assert(usrInfo["stripe_cust_id"] != None)
        information_list.append(usrInfo)

        # get group info
        grp = dvcGroup()
        grpInfo_list = grp.getGroupInfo(name=GRPNAME)
        grpInfo = grpInfo_list[0]
        information_list.append(grpInfo)

        # check subscription
        subscriptionObj = Subscriptions()
        subscriptions_info_list = subscriptionObj.getSubscriptions(
            user_id=usrInfo["id"])
        subscriptions_info = subscriptions_info_list[0]
        information_list.append(subscriptions_info)

        return information_list

    except Exception as e:
        raise


def test_create_recurring_asset_subscription(d3e_init):
    # def test_create_recurring_asset_subscription(del_all_subscription_info):

    tokenVal = "tok_visa"
    r = client.post('subscribe',
                    headers=Headers.get(),
                    json={
                        'tokenId': tokenVal,
                        'licenseQuantity': 2,
                        'tier': LICENSE_TIER_STANDARD,
                        'email': USRNAME,
                        'password': PASSWD
                    })

    assert(r.status == '201 Created')

    try:

        # get user info
        usr = dvcUser()
        usrInfo_list = usr.getUserInfo(username=USRNAME)
        usrInfo = usrInfo_list[0]
        assert(usrInfo["stripe_cust_id"] != None)

        # get group info
        grp = dvcGroup()
        grpInfo_list = grp.getGroupInfo(name=GRPNAME)
        assert(len(grpInfo_list) != 0)
        grpInfo = grpInfo_list[0]

        # check subscription
        subscriptionObj = Subscriptions()
        subscriptions_info_list = subscriptionObj.getSubscriptions(
            user_id=usrInfo["id"])
        assert(len(subscriptions_info_list) != 0)
        subscriptions_info = subscriptions_info_list[0]

        assert(subscriptions_info["count"] <= 2)
        assert(subscriptions_info["user_id"] == usrInfo["id"])
        assert(subscriptions_info["plan_id"] == plan_id_light)
        #assert(subscriptions_info["subscription_id"] ==  sbscrptn_id)
        assert(subscriptions_info["group_id"] == grpInfo["id"])

        # post json with licenseQuantity >= 5

    except Exception as e:
        raise e

    return


def test_activation_tokens(d3e_init):

    create_prime_group(GRPNAME, USRNAME, PASSWD)
    # clear activation_tokens table
    activation_tokens_obj = OthTable("activation_tokens")
    activation_tokens_obj.deleteData(token=ACTIVATION_TOKEN)

    login(USRNAME, PASSWD)
    r = client.post('activationtokens',
                    headers=Headers.get(),
                    json={
                        'activation_token': ACTIVATION_TOKEN
                    })

    assert(r.status == "201 Created")

    return


def test_activate_license(d3e_init):

    create_prime_group(GRPNAME, USRNAME, PASSWD)
    # delete license data
    license_obj = OthTable("licenses")
    license_obj.deleteTableData()

    # get activation token id
    activation_tokens_obj = OthTable("activation_tokens")
    activation_token_data_lst = activation_tokens_obj.getTableData(
        token=ACTIVATION_TOKEN)
    activation_token_data = activation_token_data_lst[0]
    activation_token_id = activation_token_data["id"]

    # get order number = subscription_id from subscriptions with max(id)
    subsObj = OthTable("subscriptions")
    subscriptions_single_rec_list = subsObj.getTableData(
        statement="ORDER BY id DESC LIMIT 1")
    subs_data = subscriptions_single_rec_list[0]
    # order_number = subscription_id
    order_number = subs_data["subscription_id"]

    login(USRNAME, PASSWD)
    r = client.put('activate',
                   headers=Headers.get(),
                   json={
                       'activationTokenId': activation_token_id,
                       'orderNumber': order_number
                   })

    assert(r.status == '201 Created')  # license data created

    try:

        # get user info
        usr = dvcUser()
        usrInfoLst = usr.getUserInfo(username=USRNAME)
        usrInfo = usrInfoLst[0]
        assert(usrInfo["stripe_cust_id"] != None)

        # get group info
        grp = dvcGroup()
        grpInfoLst = grp.getGroupInfo(name=GRPNAME)
        grpInfo = grpInfoLst[0]

        # check subscriptions table
        subscriptionObj = Subscriptions()
        sbscrptn_id = str(order_number)
        subscriptions_info_list = subscriptionObj.getSubscriptions(
            subscription_id=sbscrptn_id, user_id=usrInfo["id"])
        subscriptions_info = subscriptions_info_list[0]

        assert(subscriptions_info["count"] <= 2)
        assert(subscriptions_info["user_id"] == usrInfo["id"])
        assert(subscriptions_info["plan_id"] == plan_id_light)
        assert(subscriptions_info["subscription_id"] == sbscrptn_id)
        assert(subscriptions_info["group_id"] == grpInfo["id"])
        assert(subscriptions_info["used"] == 1)

        # check activation_token table
        #token_contents = ACTIVATION_TOKEN.split(".")
        #assert(len(token_contents) == 3)
        actvtn_tkn_obj = ActivationToken()
        atInfoLst = actvtn_tkn_obj.getActivationToken(token=ACTIVATION_TOKEN)
        atInfo = atInfoLst[0]
        assert(atInfo["activated"] == 1)

        # get activation info
        payload = jwt.decode(ACTIVATION_TOKEN, D3E_ACTIVATION_KEY, algorithms=JWT_DECODE_ALGORITHM)

        activation_info = {
            "expiration": payload["exp"],
            "system_serial": payload["sys"],
            "manufacturer": payload["man"],
            "model": payload["mod"],
            "computer_name": payload["cmp"]
        }

        # check liceses table
        lic = Licenses()
        licInfoLst = lic.getLicenses(
            group_id=grpInfo["id"], sub_id=subscriptions_info["id"])
        licInfo = licInfoLst[0]

        assert(licInfo["system_serial"] == activation_info["system_serial"])
        assert(licInfo["manufacturer"] == activation_info["manufacturer"])
        assert(licInfo["model"] == activation_info["model"])
        assert(licInfo["computer_name"] == activation_info["computer_name"])

    except Exception as e:
        raise e

    return


def test_get_license(d3e_init):

    try:
        create_prime_group(GRPNAME, USRNAME, PASSWD)
        # get subs_id
        subsObj = OthTable("subscriptions")
        subscriptions_single_rec_list = subsObj.getTableData(
            statement="ORDER BY id DESC LIMIT 1")
        subs_data = subscriptions_single_rec_list[0]

        # get license token
        lic = Licenses()
        licInfoLst = lic.getLicenses(sub_id=subs_data["id"])
        licInfo = licInfoLst[0]
        lic_tkn = licInfo["token"]

        login(USRNAME, PASSWD)
        Headers.update(authorization='Bearer %s' % lic_tkn)
        r = client.get('license',
                       headers=Headers.get())

        assert(r.status == "200 OK")

        # get subscription info
        subscription_info = get_subscription_info()
        subscription = subscription_info[SUB]

        assert(r.json["status"] == subscription["status"])
        assert(r.json["type"] == subscription["type"])
        expiration_seconds = (
            subscription["exp_timestamp"] - datetime.datetime(1970, 1, 1)).total_seconds()
        assert(r.json["expiration"] == expiration_seconds)
        assert(r.json["count"] == subscription["count"])
        assert(r.json["used"] == subscription["used"])
        assert(r.json["tier"] == subscription["tier"])
        assert(r.json["recurring"] == subscription["recurring"])

    except Exception as e:
        raise e

    return


def test_validate_d3e_token(d3e_init):

    try:
        create_prime_group(GRPNAME, USRNAME, PASSWD)
        login(USRNAME, PASSWD)
        activation_token = ACTIVATION_TOKEN
        Headers.update(authorization='Bearer %s' % activation_token)
        r = client.get('validate',
                       headers=Headers.get())

        assert(r.status == "200 OK")

        actvtn_tkn_obj = ActivationToken()
        atInfoLst = actvtn_tkn_obj.getActivationToken(token=ACTIVATION_TOKEN)
        atInfo = atInfoLst[0]
        license_uuid = atInfo["license_uuid"]

        # get licenses data
        lic_obj = Licenses()
        licInfoLst = lic_obj.getLicenses(uuid=license_uuid)
        licInfo = licInfoLst[0]

        assert(r.json["license"] == licInfo["token"])

    except Exception as e:
        raise e

    return


def test_get_software_versions(d3e_init):

    try:
        create_prime_group(GRPNAME, USRNAME, PASSWD)
        login(USRNAME, PASSWD)
        r = client.get('update',
                       headers=Headers.get())

        assert(r.status == "200 OK")

        softVerObj = OthTable("software_versions")

        software_version_rec_list = softVerObj.getTableData(
            statement="ORDER BY id DESC LIMIT 1")

        software_version_rec = software_version_rec_list[0]

        assert(r.json["minor"] == int(software_version_rec["minor"]))
        assert(r.json["major"] == int(software_version_rec["major"]))
        assert(r.json["revision"] == int(software_version_rec["revision"]))
        assert(r.json["path"] == software_version_rec["path"])

    except Exception as e:
        raise e

    return


def test_deactivate_license(d3e_init):

    try:
        create_prime_group(GRPNAME, USRNAME, PASSWD)
        # get subs_id
        subsObj = OthTable("subscriptions")
        subscriptions_single_rec_list = subsObj.getTableData(
            statement="ORDER BY id DESC LIMIT 1")
        subs_data = subscriptions_single_rec_list[0]
        start_subs_info = subs_data["used"]

        # get license token
        lic = Licenses()
        licInfoLst = lic.getLicenses(sub_id=subs_data["id"])
        licInfo = licInfoLst[0]
        lic_tkn = licInfo["token"]

        login(USRNAME, PASSWD)
        Headers.update(authorization='Bearer %s' % lic_tkn)
        r = client.put('deactivate',
                       headers=Headers.get())
        assert(r.status == "200 OK")

        # check subscription
        end_subs_info_lst = subsObj.getTableData(
            statement="ORDER BY id DESC LIMIT 1")

        end_subs_info = end_subs_info_lst[0]
        assert(end_subs_info["used"] == start_subs_info - 1)

    except Exception as e:
        raise e

    return


# ------------ END ------------
