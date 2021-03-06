"""
test_flask


You can auto-discover and run all tests with this command:

    $ pytest

Documentation:

* https://docs.pytest.org/en/latest/
* https://docs.pytest.org/en/latest/fixture.html
* http://flask.pocoo.org/docs/latest/testing/
"""

import pytest
import json

from tests.support_tests_module import standard
from tests.support_tests_module import init_ac_general
from tests.support_tests_module import load_asset_dbs
from tests.support_tests_module import fixture

from tools.prime_group import create_prime_group

from headers import Headers

from ac_module import Ac
from user_module import User

import ctmc_flask_main as flask_main

from custDevices import Device
from userGroupRole import uGR
from userGroupRole import dvcGroup


client = flask_main.app.test_client()


@pytest.fixture
def prime():
    create_prime_group('Foundation', 'fx', 'lost')
    return


def login(username, password, activation_token=None, expecting=200):
    payload = {"username": username, "password": password}
    if activation_token:
        payload['activation_token'] = activation_token

    r = client.put('/user/login',
                   json=payload,
                   headers=Headers.set())
    assert r.status_code == expecting
    if r.status_code == 200:
        Headers.update(authorization='Bearer %s' % r.json)
    return


def test_login(standard, prime):
    login('fx', 'lost')
    return


def test_login_bad_password(standard, prime):
    login('fx', 'not the password', expecting=401)
    return


def test_login_bad_user(standard, prime):
    login('not a user', 'not the password', expecting=401)
    return


def test_get_user_current(standard, prime):
    login('fx', 'lost')
    r = client.options('api/user')
    assert r.status_code == 200
    r = client.get('api/user',
                   headers=Headers.get())
    assert r.status_code == 200
    return


def test_without_login_get_user_current(standard, prime):
    r = client.get('api/user',
                   headers=Headers.set())
    assert r.status_code == 400
    return


def test_generate_2fa(standard, prime):
    login('fx', 'lost')
    r = client.put('user/2fa',
                   headers=Headers.get())
    assert r.status_code == 200
    return


def test_get_user_by_id(standard, init_ac_general):
    login('fx', 'lost')
    print()
    u = User.read(username='grimly')
    r = client.get('api/user/%d' % u.id,
                   headers=Headers.get())
    assert r.status_code == 200
    return


def test_get_user_by_id_bad(standard, init_ac_general):
    Ac.set_user_id()
    u = User.read(username='fx')
    login('grimly', 'lost')
    r = client.get('api/user/%d' % u.id,
                   headers=Headers.get())
    assert r.status_code == 404
    return


# Compare 2 lists
def compareLists(list1, list2):
    result = True
    for i in range(len(list1)):
        if (list1[i] != list2[i]):
            result = False

    return result


def test_get_ugrs_by_id(standard, init_ac_general):
    login('fx', 'lost')
    r = client.get('api/user',
                   headers=Headers.get())
    assert r.status_code == 200
    r = client.get('api/ugrs/user/%d' % r.json['id'],
                   headers=Headers.get())
    assert r.status_code == 200
    print(json.dumps(r.json, indent=3))
    #print(r.json)

    # WP_734
    ugrs_dict = r.json
    UGRS = "ugrs"
    assert(UGRS in ugrs_dict)
    ugrs_dle = ugrs_dict[UGRS]
    ugr_dict_list_elem1 = ugrs_dle[0]
    ugr_dl_elem = {
                      "_access_rights": {
                         "permissions": [
                            "read",
                            "write",
                            "add",
                            "delete"
                         ],
                         "read_only": [],
                         "read_write": [
                            "uuid",
                            "id",
                            "role_tag",
                            "user_id",
                            "group_id"
                         ]
                      },
                      "_group_name": "Foundation",
                      "_obj_type": "user_group_role",
                      "group_id": 1,
                      "id": 1,
                      "role_tag": "admin",
                      "user_id": 1,
                      "uuid": "e11d5af1-0326-4f24-aad0-f3fe437dd990"
                  }
    for ugrs_key in ugr_dl_elem:
       assert(ugrs_key in ugr_dict_list_elem1)

    acc_rights_dict = ugr_dict_list_elem1["_access_rights"]
    assert("permissions" in acc_rights_dict)
    assert("read_only" in acc_rights_dict)
    assert("read_write" in acc_rights_dict)

    arp_list = acc_rights_dict["permissions"]
    perm_list = ["read", "write", "add", "delete"]
    for _elem in perm_list:
        assert(_elem in arp_list)

    arrw_list = acc_rights_dict["read_write"]
    rw_list = ["uuid", "id", "role_tag", "user_id", "group_id"]
    for _elem in rw_list:
        assert(_elem in arrw_list)

    arro_list = acc_rights_dict["read_only"]
    assert(len(arro_list) == 0)

    # WP_734

    return


# WP_773
# Verify keys and values of only one user for a group.
def verify_users(user_first_dict, test_user_list):

    try: # for debugging
        # verify keys in the user dictionary
        user_dict = {
                        "_access_rights": {
                           "permissions": [
                              "add",
                              "delete",
                              "read",
                              "write"
                           ],
                           "read_only": [
                              "last_login",
                              "join_date"
                           ],
                           "read_write": [
                              "email",
                              "billing_phone",
                              "logins",
                              "permissions",
                              "active",
                              "criticalMail",
                              "fname",
                              "billing_zip_code",
                              "uuid",
                              "lname",
                              "group_id",
                              "billing_city",
                              "billing_srt1",
                              "account_id",
                              "email_verified",
                              "messageMail",
                              "lvl_1_usr_id",
                              "password",
                              "warnMail",
                              "messageMobile",
                              "vericode",
                              "stripe_cust_id",
                              "username",
                              "warnMobile",
                              "serviceMobile",
                              "infoMobile",
                              "infoShow",
                              "company",
                              "id",
                              "billing_state",
                              "lvl_id",
                              "criticalMobile",
                              "second_factor",
                              "infoMail",
                              "serviceMail",
                              "billing_srt2"
                           ]
                        },
                        "_obj_type": "user",
                        "account_id": 0,
                        "account_owner": 0,
                        "active": 1,
                        "billing_city": "",
                        "billing_phone": "",
                        "billing_srt1": "",
                        "billing_srt2": "",
                        "billing_state": "",
                        "billing_zip_code": "",
                        "company": "",
                        "criticalMail": 1,
                        "criticalMobile": 1,
                        "email": "",
                        "email_verified": 0,
                        "fname": "",
                        "group_id": 5,
                        "id": 3,
                        "infoMail": 0,
                        "infoMobile": 0,
                        "infoShow": 0,
                        "join_date": "Thu, 30 May 2019 12:22:51 GMT",
                        "last_login": "Thu, 30 May 2019 12:22:51 GMT",
                        "lname": "",
                        "logins": 0,
                        "lvl_1_usr_id": 0,
                        "lvl_2_usr_id": "",
                        "lvl_id": 0,
                        "messageMail": 1,
                        "messageMobile": 1,
                        "password": "$2y$12$yjvNJSyyYMHUoTkHPvQKLe8dm7k5zBNG1Ai7jY9Fbod1ud3lPTDFW",
                        "permissions": 0,
                        "second_factor": "",
                        "serviceMail": 1,
                        "serviceMobile": 1,
                        "stripe_cust_id": "",
                        "username": "brad",
                        "uuid": "e0dbd51c-1f8e-494b-9f32-3392c0829af7",
                        "vericode": "",
                        "warnMail": 1,
                        "warnMobile": 1
                     }
        # verify keys exist
        for key in user_dict:
            assert(key in user_first_dict)

        # verify user data
        usr_id = user_first_dict["id"]
        usr_fname = user_first_dict["fname"]
        group_id = user_first_dict["group_id"]
        usr_lname = user_first_dict["lname"]
        usrname = user_first_dict["username"]
        usr_uuid = user_first_dict["uuid"]
        user_found = False
        for usr_dl in test_user_list:
            if usr_dl["username"] == usrname:
                assert(usr_fname == usr_dl["fname"])
                assert(group_id == usr_dl["group_id"])
                assert(usr_lname == usr_dl["lname"])
                assert(usrname == usr_dl["username"])
                assert(usr_uuid == usr_dl["uuid"])
                user_found = True
                break
        assert(user_found)

    except Exception as e:
        raise e

# verify_user() - end

# Verify keys and values of only one asset for a group.
def verify_asset(asset_first_dict, test_asset_list):

    try: # for debugging
        # verify keys in the asset dictionary
        asset_dict = {
                         "_access_rights": {
                            "permissions": [
                               "read",
                               "write"
                            ],
                            "read_only": [],
                            "read_write": [
                               "registered",
                               "authorized",
                               "name",
                               "int_ip",
                               "sub_start",
                               "id",
                               "deviceid",
                               "offline_notified",
                               "uuid",
                               "online",
                               "group_id",
                               "ext_ip",
                               "userid",
                               "cust_code",
                               "sub_expire"
                            ]
                         },
                         "_alerts": [],
                         "_asset_config_options": {
                            "countermeasures": 0,
                            "firmware_version": "1.21.125",
                            "lcd_status": 1
                         },
                         "_asset_status": {
                            "_obj_type": "asset_status",
                            "id": 13011,
                            "state": 1,
                            "status": "OK",
                            "status_timestamp": "Thu, 07 Mar 2019 15:59:59 GMT"
                         },
                         "_obj_type": "asset",
                         "agent_type": "",
                         "authorized": 1,
                         "cust_code": "",
                         "deviceid": "C4wjiHHMu0gJ",
                         "ext_ip": "10.200.50.151",
                         "group_id": 1,
                         "id": 18,
                         "int_ip": "192.168.1.109",
                         "name": "minion",
                         "offline_notified": 0,
                         "online": 1,
                         "password": "$2a$12$Fr2eKLmV6XV0k19S1dKM6uN1Lkr7xLC2YQyRegW6yWT6fSMhTnc.u",
                         "register_timestamp": "Thu, 30 May 2019 12:22:51 GMT",
                         "registered": 0,
                         "sharedsecret": "BGoHbhGlQOQW",
                         "sub_expire": "",
                         "sub_start": "",
                         "userid": 0,
                         "uuid": "93ca00f0-1203-4bb0-bee8-3f3fb4736092"
                    }

        # verify keys exist
        for key in asset_dict:
            if key == "_alerts":
                continue
            assert(key in asset_first_dict)

        # verify user data
        asset_id = asset_first_dict["id"]
        assetid = asset_first_dict["deviceid"]
        assetname = asset_first_dict["name"]
        group_id = asset_first_dict["group_id"]
        asset_uuid = asset_first_dict["uuid"]
        asset_found = False
        for asset_dl in test_asset_list:
            if asset_dl["deviceid"] == assetid:
                assert(asset_id == asset_dl["id"])
                assert(assetname == asset_dl["name"])
                assert(group_id == asset_dl["group_id"])
                assert(asset_uuid == asset_dl["uuid"])
                asset_found = True
                break
        assert(asset_found)

    except Exception as e:
        raise e

# verify_asset() - end

def verify_alert(asset_alert_dict):

    try:
        alert_dict = {
                         "_obj_type": "alert",
                         "ack": 1,
                         "alert_time": "Wed, 26 Sep 2018 21:20:29 GMT",
                         "alert_type": "rogue",
                         "deviceid": "ZQ5jmN2elTkB",
                         "hostname": "None",
                         "id": 1,
                         "ip": "192.168.1.148",
                         "mac": "DC:CF:96:97:8D:D9",
                         "message": "Rogue Device Detected!!! IP: 192.168.1.148",
                         "notified": 1,
                         "severity": 1
                     }
    
        for key in alert_dict:
            assert(key in asset_alert_dict)
    
    except Exception as e:
        raise e



# Verify group list of dictionaries using recursion instead of just one list element.
def verify_groups(group_list, group_dict_list):
    if len(group_list) == 1:

        try:
            # for debugging ...
            # verify group dict keys
            grp_dict = {
                           "_access_rights": {
                              "permissions": [
                                 "delete",
                                 "read",
                                 "write",
                                 "add"
                              ],
                              "read_only": [
                                 "_assets",
                                 "_users"
                              ],
                              "read_write": [
                                 "uuid",
                                 "grplvl",
                                 "grpname",
                                 "name",
                                 "id",
                                 "end_dttm",
                                 "parent_id",
                                 "active",
                                 "start_dttm"
                              ]
                           },
                           "_assets": [],
                           "_obj_type": "group",
                           "_users": [],
                           "active": "",
                           "end_dttm": "",
                           "grplvl": 2,
                           "grpname": "",
                           "id": 4,
                           "name": "Atlas",
                           "parent_id": 1,
                           "start_dttm": "",
                           "uuid": "81ba6e64-3e7f-41d8-b9d2-2c6781a79eb5"
                       }

            group_list_elem = group_list[0]
            for key in grp_dict:
                assert(key in group_list_elem)

            # verify group data
            grp_id = group_list_elem["id"]
            grp_name = group_list_elem["name"]
            parent_id = group_list_elem["parent_id"]
            grp_uuid = group_list_elem["uuid"]
            grplvl = group_list_elem["grplvl"]
            group_found = False
            for grp_dl in group_dict_list:
                if grp_dl["id"] == grp_id:
                    assert(grp_name == grp_dl["name"])
                    assert(parent_id == grp_dl["parent_id"])
                    assert(grp_uuid == grp_dl["uuid"])
                    assert(grplvl == grp_dl["grplvl"])
                    group_found = True
                    break
            assert(group_found)

            # get user and check
            #verify_user() 
            user_list_of_dicts = group_list_elem["_users"]
            testGrpObj = dvcGroup(grp_id)
            test_user_list = testGrpObj.getUsersInGroup()
            if len(user_list_of_dicts) != 0:
                user_first_dict = user_list_of_dicts[0]
                if len(user_first_dict) != 0:
                    verify_users(user_first_dict, test_user_list)

            # get all assets in the group
            test_asset_list = testGrpObj.getAssetsInGroup()
            # get asset and check
            # verify_assets()
            assets_list = group_list_elem["_assets"]
            if len(assets_list) != 0:
                 for asset_dict in assets_list:
                     if len(asset_dict) != 0:
                         if "_alerts" in asset_dict:
                             list_of_alerts = asset_dict["_alerts"]
                             if len(list_of_alerts) != 0:
                                 for alert_dict in list_of_alerts:
                                     if len(alert_dict) != 0:
                                         verify_alert(alert_dict)
                         verify_asset(asset_dict, test_asset_list)

        except Exception as e:
            raise e

    else:
        mid = len(group_list) // 2
        fst_half = group_list[:mid]
        snd_half = group_list[mid:]
        verify_groups(fst_half, group_dict_list)
        verify_groups(snd_half, group_dict_list)


# WP_773

def test_get_groups(standard, init_ac_general):
    print()

    login('fx', 'lost')
    r = client.get('api/groups/summary',
                   headers=Headers.get())
    assert r.status_code == 200
    print(json.dumps(r.json, indent=3))
    # TODO: verify data

    r = client.get('api/groups/standard',
                   headers=Headers.get())
    assert r.status_code == 200
    print(json.dumps(r.json, indent=3))
    # TODO: verify data
    return


def test_get_asset(standard, init_ac_general, load_asset_dbs):
    print()
    login('fx', 'lost')
    r = client.get('api/asset/H5V2JiWiwCi0',
                   headers=Headers.get())
    assert r.status_code == 200
    print(json.dumps(r.json, indent=3))

    # WP_721
    asset_dict = r.json
    asset_prop_dict = {}
    asset_prop_dict = {
                        "sub_start"        : "",
                        "sub_expire"       : "",
                        "userid"           : "",
                        "_rogueDevCnt"     : 0,
                        "_attackCnt"       : 0,
                        "_portScanCnt"     : 0,
                        "_rogueServiceCnt" : 0,
                        "_authDevCnt"      : 0,
                        "_messageCnt"      : 0,
                        "_onlineDev"       : 0,
                        "_offlineDev"      : 0,
                        "_blockedCnt"      : 0,
                        "_health"          : 0,     # Enum - check range
                        "_asset_config_options": {
                           "countermeasures": 0,
                           "firmware_version": "1.21.125",
                           "lcd_status": 1
                        },
                    }
    asset_prop_keys = asset_prop_dict.keys()
    for _key in asset_prop_keys:
        print( "key = <%s>" % _key)
        assert(_key in asset_dict)

    assert(asset_dict.get("_asset_config_options").get("countermeasures") != None)
    assert(asset_dict.get("_asset_config_options").get("firmware_version") != None)
    assert(asset_dict.get("_asset_config_options").get("lcd_status") != None)
    # WP_721

    # WP_726 - Verify Counts
    # get expected Counts ...
    dvc = Device()
    dvc.setDeviceId("H5V2JiWiwCi0")
    dvc.getDvcDataCounts()

    # Alert Counts
    assert(asset_dict["_attackCnt"] == dvc.dvcDataCounts["attackAlerts"])

    #assert(asset_dict["_messageCnt"]) == 0
    assert(asset_dict["_attackCnt"] == dvc.dvcDataCounts["messageAlerts"])

    #assert(asset_dict["_rogueDevCnt"]) == 0
    assert(asset_dict["_rogueDevCnt"] == dvc.dvcDataCounts["rougueAlerts"])

    #assert(asset_dict["_rogueServiceCnt"]) == 0
    assert(asset_dict["_rogueServiceCnt"] == dvc.dvcDataCounts["rougueSvcAlerts"])

    #assert(asset_dict["_portScanCnt"]) == 1
    assert(asset_dict["_portScanCnt"] == dvc.dvcDataCounts["scanAlerts"])
    # Alert Counts

    # Conn Hosts
    #assert(asset_dict["_authDevCnt"]) == 4
    assert(asset_dict["_authDevCnt"] == dvc.dvcDataCounts["trstCH"])

    #assert(asset_dict["_blockedCnt"]) == 0
    assert(asset_dict["_blockedCnt"] == dvc.dvcDataCounts["blckCH"])

    assert(asset_dict["_offlineDev"] == dvc.dvcDataCounts["offlCH"])
    assert(asset_dict["_onlineDev"] == dvc.dvcDataCounts["onliCH"])

    # Conn Hosts

    # WP_726 - Verify Counts

    return


def test_get_assets(standard, init_ac_general):
    print()
    login('brad', 'lost')
    r = client.get('api/assets',
                   headers=Headers.get())
    assert r.status_code == 200
    print(json.dumps(r.json, indent=3))
    return


def test_get_alerts(standard, init_ac_general):
    print()
    login('fx', 'lost')
    r = client.get('api/asset/H5V2JiWiwCi0/alerts',
                   headers=Headers.get())
    assert r.status_code == 200
    print(json.dumps(r.json, indent=3))
    return


def test_get_hosts(standard, init_ac_general):
    print()
    login('fx', 'lost')
    r = client.get('api/asset/H5V2JiWiwCi0/hosts',
                   headers=Headers.get())
    assert r.status_code == 200
    print(json.dumps(r.json, indent=3))


    # WP_720
    hostS_dict = r.json
    assert("hosts" in hostS_dict)
    assert(len(hostS_dict) != 0)

    #MariaDB [H5V2JiWiwCi0]> SELECT COUNT(*) FROM hosts;
    #+----------+
    #| COUNT(*) |
    #+----------+
    #|        4 |
    #+----------+
    #1 row in set (0.00 sec)
    #
    #MariaDB [H5V2JiWiwCi0]>
    NUM_HOSTS = 4
    last_hosts = hostS_dict["hosts"][NUM_HOSTS - 1]
    assert(last_hosts != None)

    host1 = hostS_dict["hosts"][0]
    #assert(host1["_countermeasures"] != None)
    #assert(host1["_obj_type"] != None)
    #assert(host1["_ports"]  != None)
    host_data_dict = {
                         "_countermeasures": [],
                         "_obj_type": "asset_host",
                         "_ports": [],
                         "authorized": 1,
                         "deviceid": "H5V2JiWiwCi0",
                         "devicename": "\r",
                         "hostname": "None",
                         "id": 4,
                         "ip": "192.168.1.102",
                         "last_update": "Mon, 04 Mar 2019 21:50:08 GMT",
                         "mac": "FC:25:3F:D4:53:59",
                         "mac_vendor": "Apple",
                         "os_accuracy": "",
                         "os_family": "",
                         "os_gen": "",
                         "os_name": "",
                         "os_vendor": "",
                         "protocol": "ipv4",
                         "state": "up",
                         "status": ""
                     }
    for host_key in host_data_dict:
        assert((host_key in host1) == True)

    port1 = host1["_ports"]
    assert(len(port1) != None)

    port1_host1 = port1[0]
    assert(port1_host1 != None)

    if len(port1_host1) != 0:
        port_dict = {
                        "_obj_type": "asset_host_port",
                        "deviceid": "H5V2JiWiwCi0",
                        "id": 1,
                        "info": "",
                        "ip": "192.168.1.1",
                        "mac": "08:00:27:4B:58:FB",
                        "name": "www-http",
                        "port": 80,
                        "protocol": "tcp",
                        "service": "World Wide Web HTTP",
                        "state": "open",
                        "status": ""
                     }

        for port_key in port_dict:
            assert((port_key in port1_host1) == True)

    # WP_720

    return


def test_get_commands(standard, init_ac_general):
    print()
    login('fx', 'lost')
    r = client.get('api/asset/H5V2JiWiwCi0/commands',
                   headers=Headers.get())
    assert r.status_code == 200
    print(json.dumps(r.json, indent=3))
    return


def test_post_user(standard, init_ac_general):
    print()
    login('fx', 'lost')
    r = client.post('api/user',
                    headers=Headers.get(),
                    json={
                        'username': 'ortiz',
                        'group_id': 2,
                        'password': 'lost'
                    })
    assert r.status_code == 200
    print(json.dumps(r.json, indent=3))
    return

def test_put_user(standard, init_ac_general):
    print()
    login('fx', 'lost')
    u = User.read(username='bill')
    r = client.get('api/user/%d' % u.id,
                   headers=Headers.get())
    assert r.status_code == 200
    u.fname = 'Big'
    u.lname = 'Bird'
    r = client.put('api/user',
                   headers=Headers.get(),
                   json=u.get_dict())
    assert r.status_code == 200
    return


def test_get_users_known(standard, init_ac_general):
    print()
    login('fx', 'lost')
    r = client.get('api/users',
                   headers=Headers.get())
    assert r.status_code == 200
    assert users_in_response(r) == ['fx', 'bill', 'brad', 'george', 'grimly']

    login('bill', 'lost')
    r = client.get('api/users',
                   headers=Headers.get())
    assert r.status_code == 200
    assert users_in_response(r) == ['bill', 'brad', 'george', 'grimly']

    login('grimly', 'lost')
    r = client.get('api/users',
                   headers=Headers.get())
    assert r.status_code == 200
    assert users_in_response(r) == []

    return


def users_in_response(r):
    users = r.json['users']
    usernames = [user['username'] for user in users]
    return usernames


def verify_ugr_keys(rjson):

    try:
        access_keys = {
                          "_access_rights": {
                             "permissions": [
                                "write",
                                "add",
                                "read",
                                "delete"
                             ],
                             "read_only": [
                                "join_date",
                                "last_login"
                             ],
                             "read_write": [
                                "uuid",
                                "company",
                                "logins",
                                "infoMobile",
                                "criticalMail",
                                "billing_srt2",
                                "vericode",
                                "lvl_1_usr_id",
                                "active",
                                "criticalMobile",
                                "username",
                                "billing_zip_code",
                                "group_id",
                                "stripe_cust_id",
                                "serviceMail",
                                "second_factor",
                                "warnMobile",
                                "warnMail",
                                "fname",
                                "lname",
                                "password",
                                "account_id",
                                "permissions",
                                "email",
                                "billing_city",
                                "billing_srt1",
                                "serviceMobile",
                                "infoMail",
                                "messageMobile",
                                "infoShow",
                                "email_verified",
                                "messageMail",
                                "billing_phone",
                                "billing_state",
                                "id",
                                "lvl_id"
                             ]
                          }
                      }

        _ar = "_access_rights"
        _pl = "permissions"
        _ol = "read_only"
        _wl = "read_write"
        acc_rights_dict = access_keys[_ar]
        perm_lst        = acc_rights_dict[_pl]
        _ro_lst         = acc_rights_dict[_ol]
        _rw_lst         = acc_rights_dict[_wl]

        user_dict_elem = rjson["users"]
        user_dict = user_dict_elem[0]

        assert(_ar in user_dict)
        ud_acc_rights = user_dict[_ar]
        assert(_pl in ud_acc_rights)
        ud_perm_lst   = ud_acc_rights[_pl]
        assert(_ol in ud_acc_rights)
        ud_ro_lst     = ud_acc_rights[_ol]
        assert(_wl in ud_acc_rights)
        ud_rw_lst     = ud_acc_rights[_wl]

        # check permissions
        for pl in perm_lst:
           assert(pl in ud_perm_lst)

        # check read_only
        for _ro in _ro_lst:
           assert(_ro in ud_ro_lst)

        # check read_write
        for _rw in _rw_lst:
           assert(_rw in ud_rw_lst)

        assert("_obj_type" in user_dict)
        ugrs = "_ugrs"
        assert(ugrs in user_dict)


        ud_ugr_list = user_dict[ugrs]
        ud_ugr_dict = ud_ugr_list[0]

        ugr_dict = {
                    "_access_rights": {
                       "permissions": [
                          "write",
                          "add",
                          "read",
                          "delete"
                       ],
                       "read_only": [],
                       "read_write": [
                          "uuid",
                          "role_tag",
                          "id",
                          "group_id",
                          "user_id"
                       ]
                    },
                    "_group_name": "",
                    "_obj_type": "",
                    "group_id": 1,
                    "id": 1,
                    "role_tag": "",
                    "user_id": 1,
                    "uuid": ""
                 }

        ac_str = "_access_rights"
        pm_str = "permissions"
        ro_str = "read_only"
        rw_str = "read_write"
        ac_d = ugr_dict[ac_str]
        pm_l = ac_d[pm_str]
        ro_l = ac_d[ro_str]
        rw_l = ac_d[rw_str]

        for _ugr_key in ugr_dict:
            assert(_ugr_key in ud_ugr_dict)

        ud_ac_d = ud_ugr_dict[ac_str]
        assert(pm_str in ud_ac_d)
        ud_pm_l = ud_ac_d[pm_str]
        for pm_elem in pm_l:
            assert(pm_elem in ud_pm_l)
        assert(ro_str in ud_ac_d)
        ud_ro_l = ud_ac_d[ro_str]
        assert(len(ud_ro_l) == 0)
        assert(rw_str in ud_ac_d)
        ud_rw_l = ud_ac_d[rw_str]
        for rw_elem in rw_l:
            assert(rw_elem in ud_rw_l)


        user_info_dict = {
                             "account_id": 0,
                             "account_owner": 0,
                             "active": 1,
                             "billing_city": "",
                             "billing_phone": "",
                             "billing_srt1": "",
                             "billing_srt2": "",
                             "billing_state": "",
                             "billing_zip_code": "",
                             "company": "",
                             "criticalMail": 1,
                             "criticalMobile": 1,
                             "email": "",
                             "email_verified": 0,
                             "fname": "",
                             "group_id": 1,
                             "id": 1,
                             "infoMail": 0,
                             "infoMobile": 0,
                             "infoShow": 0,
                             "join_date": "Thu, 16 May 2019 13:00:16 GMT",
                             "last_login": "Thu, 16 May 2019 20:02:53 GMT",
                             "lname": "",
                             "logins": 1,
                             "lvl_1_usr_id": 0,
                             "lvl_2_usr_id": "",
                             "lvl_id": 0,
                             "messageMail": 1,
                             "messageMobile": 1,
                             "password": "$2y$12$n/lNrwqW8LUrl/Irx3FEzuUFdJ8EWXu4MTuQnW77H1WxG0gtBAggW",
                             "permissions": 0,
                             "second_factor": "",
                             "serviceMail": 1,
                             "serviceMobile": 1,
                             "stripe_cust_id": "",
                             "username": "fx",
                             "uuid": "c4b61fe7-d627-4397-9344-850e02c72b9c",
                             "vericode": "",
                             "warnMail": 1,
                             "warnMobile": 1
                         }

        ud_user_list = rjson["users"]
        ud_user_info = ud_user_list[0]

        for user_ie in user_info_dict:
            assert(user_ie in ud_user_info)

    except Exception as e:
        raise e

    return


def verify_ugr_data(rjson, logged_user):

    assert(("users" in rjson) == True)
    ugrs_list = rjson["users"]
    usr_fnd = False

    # verify keys
    verify_ugr_keys(rjson)

    try:
        for userd in ugrs_list:
            user_name = userd["username"]
            if user_name == logged_user:
                usr_fnd = True
                uGRobj = uGR(user_name)
                assert(uGRobj.username == user_name)
                uGRdictList = []
                uGRdictList = uGRobj.getUgrInfo()

                ugr_num = 0
                not_chkd = True
                rjson_ugr = []
                rjson_ugr = userd["_ugrs"]

                for uGRdl in uGRdictList:

                    if not_chkd:
                        assert(uGRdl["user_id"] == userd["id"])
                        assert(uGRdl["user_uuid"] == userd["uuid"])
                        not_chkd = False

                    ugr_d = rjson_ugr[ugr_num]
                    assert(uGRdl["ugr_id"] == ugr_d["id"])
                    assert(uGRdl["group_id"] == ugr_d["group_id"])
                    assert(uGRdl["groupname"] == ugr_d["_group_name"])
                    assert(uGRdl["role_tag"] == ugr_d["role_tag"])
                    assert(uGRdl["ugr_uuid"] == ugr_d["uuid"])
                    ugr_num = ugr_num + 1

                break

    except Exception as e:
        # TODO: fix this
        print(e)

    print("user found = %s" % usr_fnd)
    assert(usr_fnd == True)
    return

# WP_732

def test_get_users_with_roles(standard, init_ac_general):
    print()
    login('fx', 'lost')
    r = client.get('api/users/roles',
                   headers=Headers.get())
    assert r.status_code == 200
    #print(r.json)
    #print(json.dumps(r.json, indent=3))
    # WP_732
    verify_ugr_data(r.json, 'fx')

    login('bill', 'lost')
    r = client.get('api/users/roles',
                   headers=Headers.get())
    assert r.status_code == 200
    #print(r.json)
    print(json.dumps(r.json, indent=3))
    verify_ugr_data(r.json, 'bill')

    login('grimly', 'lost')
    r = client.get('api/users/roles',
                   headers=Headers.get())
    assert r.status_code == 200
    #print(r.json)
    print(json.dumps(r.json, indent=3))
    #verify_ugr_data(r.json, 'grimly')
    return


def test_register_asset(standard, init_ac_general, load_asset_dbs):
    print()
    login('fx', 'lost')

    r = client.put('api/asset/C4wjiHHMu0gJ/register',
                   headers=Headers.get(),
                   json={'name': 'purple haze',
                         'vendor': 'ACME'})
    assert r.status_code == 200
    #print(r.json)
    dvc = Device()
    dvc.setDeviceId("C4wjiHHMu0gJ")
    dvc.getRegInfo()

    # check sentinels/asset data
    assert(dvc.dvcNm == 'purple haze')
    assert(dvc.custCode == 'ACME')

    # check command list
    dvc.getCommands()
    cmds = ["initscan", "register"]
    list_num = 0
    for cmd in cmds:
        cmd_list = dvc.commands[list_num]
        assert(cmd_list[2] == cmd)
        list_num = list_num + 1

    return


def test_init_asset(standard, init_ac_general, load_asset_dbs):
    print()
    login('fx', 'lost')

    r = client.put('api/asset/C4wjiHHMu0gJ/init',
                   headers=Headers.get(),
                   )
    assert r.status_code == 200
    print(r.json)
    return


def test_reboot_asset(standard, init_ac_general, load_asset_dbs):
    print()
    login('fx', 'lost')

    r = client.put('api/asset/C4wjiHHMu0gJ/reboot',
                   headers=Headers.get(),
                   )
    assert r.status_code == 200
    print(r.json)
    return


def test_shutdown_asset(standard, init_ac_general, load_asset_dbs):
    print()
    login('fx', 'lost')

    r = client.put('api/asset/C4wjiHHMu0gJ/shutdown',
                   headers=Headers.get(),
                   )
    assert r.status_code == 200
    print(r.json)
    return


def drive_asset_switches(prepath, *switches):
    for switch in switches:
        r = client.put('%s/%s' % (prepath, switch),
                       headers=Headers.get(),
                       )
        assert r.status_code == 200
        print(r.json)
    r = client.delete('%s/%s' % (prepath, switch),
                   headers=Headers.get(),
                   )
    assert r.status_code == 200
    print(r.json)
    r = client.put('%s/%s' % (prepath, switch),
                   headers=Headers.get(),
                   )
    assert r.status_code == 200
    print(r.json)
    return


def test_asset_switches(standard, init_ac_general, load_asset_dbs):
    print()
    login('fx', 'lost')
    drive_asset_switches('/api/asset/C4wjiHHMu0gJ', 'lcd', 'adc')
    return


def api_put(path):
    print('%s =>' % path)
    r = client.put('%s' % path,
                   headers=Headers.get(),
                   )
    assert r.status_code == 200
    print(r.json)
    return


def test_alert_apis(standard, init_ac_general):
    print()
    login('fx', 'lost')
    api_put('/api/asset/H5V2JiWiwCi0/alert/6512/acknowledge')
    return


def test_ack_alerts(standard, fixture):
    print()
    login('fx', 'lost')
    r = client.patch('/api/asset/H5V2JiWiwCi0/alerts/acknowledge',
                   headers=Headers.get(),
                   )
    assert r.status_code == 200
    print(r.json)
    return


def test_rename_host(standard, fixture):
    print()
    login('fx', 'lost')
    r = client.patch('/api/asset/H5V2JiWiwCi0/host/3',
                     headers=Headers.get(),
                     json={'name': 'The Third Host'}
                     )
    assert r.status_code == 200
    print(r.json)
    return


def test_delete_command(standard, fixture):
    print()
    login('fx', 'lost')

    # reboot will create a command
    r = client.put('api/asset/C4wjiHHMu0gJ/reboot',
                   headers=Headers.get(),
                   )
    assert r.status_code == 200
    print(r.json)

    # delete the reboot command
    r = client.delete('/api/asset/C4wjiHHMu0gJ/command/1',
                      headers=Headers.get(),
                      )
    assert r.status_code == 200
    print(r.json)

    return
