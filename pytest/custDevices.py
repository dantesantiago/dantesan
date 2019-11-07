

from flask import jsonify
import sys

from logger_module import get_logger

import common
import constants
from common import mdb
from db_connection_cursor import get_db_connection
from db_connection_cursor import get_db_cursor
from common import make_response
from common import create_response

logger = get_logger(__file__)



# Separator = "|"
SEPRTR = "|"
RECON = 1
ENTRS = 2
CYBEP = 3
CIGDV = 4

dvcTypNum = []
#dvcTypNum.append(0)
dvcTypNum.append(RECON)    # rs
dvcTypNum.append(ENTRS)    # ent_rs
dvcTypNum.append(CYBEP)    # cyb_ep
dvcTypNum.append(CIGDV)    # cig_dv


# Customer class ---------------------------------------------------------------------------                            
class Customer: # grpId is custId

    '''Customer or Group class'''

    def __init__(self, adminId = 0, grpId = 0, grpNm = None,
                 rS = [], entRS = [], cybEP = [], cigDV = []):

        methodName = sys._getframe().f_code.co_name

        self.adminId  = adminId
        self.grpId    = grpId
        self.grpNm    = grpNm
        self.rS       = rS
        self.entRS    = entRS
        self.cybEP    = cybEP
        self.cigDV    = cigDV
        self.response = make_response(constants.OK_200, methodName, constants.OK_200)


    def getDevices(self, othOff=None):

        reconTN = "groups%ssentinels%sadmin_group%srs_grp_list" % (SEPRTR, SEPRTR, SEPRTR)                 # Separator = "|"
        entRSTN = "groups%senterprise_rs%sent_rs_admin_grp%sent_rs_grp_list" % (SEPRTR, SEPRTR, SEPRTR)
        cybEPTN = "groups%scyberstack_endpt%scyb_ep_admin_grp%scyb_ep_grp_list" % (SEPRTR, SEPRTR, SEPRTR)
        cigDVTN = "groups%scigent_devices%scig_dv_admin_grp%scig_dv_grp_list" % (SEPRTR, SEPRTR, SEPRTR)

        dvcTblNames = {}
        dvcTblNames = {
            1 : reconTN,
            2 : entRSTN,
            3 : cybEPTN,
            4 : cigDVTN
        }    
                         
        with get_db_connection(database=mdb) as devconn, get_db_cursor(devconn) as cursor:

                for dvcTypNo in dvcTypNum:
                
                    dvcTblNms = dvcTblNames.get(dvcTypNo)
                    #dvcTblNms = reconTN  #CTO - Simulate devices in all types.

                    tableNames = dvcTblNms.split(SEPRTR)

                    #logger.debug("tableNames = ", tableNames[0:2]) #CTO

                    # TABLE ALIASES: G - Group, D - Device, A - Admin-Group, R - Device-Group
                    try: 
                        # Verify that adminId-grpId data is active in Admin-Group table
                        sql = "  SELECT DISTINCT G.id " \
                              "    FROM %s G, %s A " \
                              " INNER JOIN users U ON U.id = A.admin_id " \
                              "   WHERE G.id = A.grp_id AND " \
                              "         A.active = 1    AND " \
                              "         G.id = %s       AND " \
                              "  (A.admin_id = %s OR U.lvl_1_usr_id = %s) " % (tableNames[0], tableNames[2],
                                                                 self.grpId, self.adminId, self.adminId)
                        #logger.debug("G-A_G sql = %s" % sql) #CTO
                        cursor.execute(sql)
                        row = cursor.fetchone()

                        if row: # active adminId-grpId data

                            try:
                                sql = "  SELECT G.grpname, D.id, D.name, D.deviceid, D.userid " \
                                      "    FROM %s G, %s D, %s R " \
                                      "   WHERE G.id = R.grp_id AND " \
                                      "         R.active = 1    AND " \
        	                          "         R.rs_id = D.id  AND " \
                                      "         G.id = %s           " % (tableNames[0], tableNames[1], tableNames[3],
                                                                         self.grpId)
                                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                                #logger.debug("G-D-R_G_L sql = %s" % sql) #CTO
                                cursor.execute(sql)
                                rows = cursor.fetchall()
                                if not rows:
                                    #logger.debug("No rows")) #CTO
                                    continue
                                    
                                for row in rows:
                                    logger.debug("\n\n________ Customer: %s ____________________" % row[0]) #CTO

                                    self.grpNm = row[0]
                                    usrId = row[4]
                                    dvcId = row[1]      # dvcId is the id in the device table
                                    dvcNm = row[2]
                                    deviceId = row[3]   # deviceid in device table

                                    logger.debug("[for row in rows:] usrId = %s, dvcId = %s, dvcNm = %s, deviceId = %s" % (usrId, dvcId, dvcNm, deviceId)) #CTO
                                    device = Device(usrId, dvcId, dvcNm, dvcTypNo, deviceId)
                                    #logger.debug("____________________ device.dvcNm = %s ________________________________________-" % device.dvcNm) #CTO

                                    # GGRP usage fix ...
                                    if othOff == None:
                                        logger.debug("getOthData() will be called ...") #CTO
                                        device.getOthData() 
 
                                    if dvcTypNo == RECON:
                                        self.rS.append(device)
                                        
                                    if dvcTypNo == ENTRS:
                                        self.entRS.append(device)
                                        
                                    if dvcTypNo == CYBEP:
                                        self.cybEP.append(device)
                                        
                                    if dvcTypNo == CIGDV:
                                        self.cigDV.append(device)

                                    if device.response.status != constants.OK_200:
                                        self.response = device.response
                                    else:
                                        self.response = create_response("OK")

                            except Exception as e:
                                logger.debug(e) #CTO
                                self.response = make_response(constants.GET_DEVICES_FAILED,
                                                                  "Customer.getDevices", 
                                                                  constants.BAD_REQUEST_400)
                               
                          
                        else: # active adminId-grpId data
                            continue
                            #self.response = make_response(constants.ADMIN_GROUP_NOT_ACTIVE,
                            #                                  "Customer.getDevices", 
                            #                                  constants.BAD_REQUEST_400)
                       
                                
                    except Exception as e:
                        logger.debug(e) #CTO
                        self.response = make_response(constants.ADMIN_GROUP_CHECK_FAILED,
                                                          "Customer.getDevices", 
                                                          constants.BAD_REQUEST_400)
                       
    #PCD - Print the Customer Devices
    def prnCustDvc(self):
    
        logger.debug("\nCustomer : %s -------------------\n" % self.grpNm)
        logger.debug(" Admin Id = %s Group Id = %s\n" % (self.adminId, self.grpId))
      
        logger.debug("\nxxxxxxxx Recon Sentinel xxxxxxxx")
        rS = self.rS
        for rs in rS:
            logger.debug("usrId: %s, dvcId = %s, deviceId = %s, dvcNm = %s \n" \
                  " lastChkIn = %s, aDCon = %s, alertCnt = %s\n" \
                  " commands = %s\n" \
                  % (rs.usrId, rs.dvcId, rs.deviceId, rs.dvcNm, 
                     rs.lastChkIn, rs.aDCon, rs.alertCnt, rs.commands))
    
        logger.debug("\nxxxxxxxx Enterprise Recon Sentinel xxxxxxxx")
        eR = self.entRS
        for er in eR:
            logger.debug("usrId: %s, dvcId = %s, deviceId = %s, dvcNm = %s \n" \
                  " lastChkIn = %s, aDCon = %s, alertCnt = %s\n" \
                  " commands = %s\n" \
                  % (er.usrId, er.dvcId, rs.deviceId, er.dvcNm, 
                     er.lastChkIn, er.aDCon, er.alertCnt, er.commands))
    
        logger.debug("\nxxxxxxxx CyberStack Endpoint xxxxxxxx")
        eP = self.cybEP
        for ep in eP:
            logger.debug("usrId: %s, dvcId = %s, deviceId = %s, dvcNm = %s \n" \
                  " lastChkIn = %s, aDCon = %s, alertCnt = %s\n" \
                  " commands = %s\n" \
                  % (ep.usrId, ep.dvcId, ep.deviceId, ep.dvcNm, 
                     ep.lastChkIn, ep.aDCon, ep.alertCnt, ep.commands))
    
        logger.debug("\nxxxxxxxx Cigent Devices xxxxxxxx")
        cD = self.cigDV
        for cd in cD:
            logger.debug("usrId: %s, dvcId = %s, deviceId = %s, dvcNm = %s \n" \
                  " lastChkIn = %s, aDCon = %s, alertCnt = %s\n" \
                  " commands = %s\n" \
                  % (cd.usrId, cd.dvcId, cd.deviceId, cd.dvcNm, 
                     cd.lastChkIn, cd.aDCon, cd.alertCnt, cd.commands))
    
    #PCD - Print the Customer Devices
    
    
            
    #CDD - Create Dictionary of Devices
    def crtDevicesDict(self):
    
        logger.debug("\nCustomer : %s -------------------\n" % self.grpNm) #CTO
        logger.debug(" Admin Id = %s Group Id = %s\n" % (self.adminId, self.grpId)) #CTO
      
        devices = []
        logger.debug("\nxxxxxxxx Recon Sentinel xxxxxxxx")    #CTO
        rS = self.rS
        for rs in rS:
            
            user = User(rs.usrId, None)
            user.getUserInfo()
            user_dict = {} 
            user_dict = user.crtUserDict()

            device_dict = {
                "dvc_id"      : rs.dvcId,
                "dvc_name"    : rs.dvcNm,
                "deviceId"    : rs.deviceId,
                "last_chk_in" : rs.lastChkIn,
                "adc_on"      : rs.aDCon,
                "alert_cnt"   : rs.alertCnt,
                "cmd_list"    : rs.commands,
                "dvc_type"    : constants.RECON,
                "user_info"   : user_dict
            }
            devices.append(device_dict)
    
    
        logger.debug("\nxxxxxxxx Enterprise Recon Sentinel xxxxxxxx")    #CTO
        eR = self.entRS
        for er in eR:

            user = User(er.usrId, None)
            user.getUserInfo()
            user_dict = {} 
            user_dict = user.crtUserDict()

            device_dict = {
                "dvc_id"      : er.dvcId,
                "dvc_name"    : er.dvcNm,
                "deviceId"    : er.deviceId,
                "last_chk_in" : er.lastChkIn,
                "adc_on"      : er.aDCon,
                "alert_cnt"   : er.alertCnt,
                "cmd_list"    : er.commands,
                "dvc_type"    : constants.ENTRS,
                "user_info"   : user_dict
            }
            devices.append(device_dict)
    
        logger.debug("\nxxxxxxxx CyberStack Endpoint xxxxxxxx")   #CTO
        eP = self.cybEP
        for ep in eP:

            user = User(ep.usrId, None)
            user.getUserInfo()
            user_dict = {} 
            user_dict = user.crtUserDict()

            device_dict = {
                "dvc_id"      : ep.dvcId,
                "dvc_name"    : ep.dvcNm,
                "deviceId"    : ep.deviceId,
                "last_chk_in" : ep.lastChkIn,
                "adc_on"      : ep.aDCon,
                "alert_cnt"   : ep.alertCnt,
                "cmd_list"    : ep.commands,
                "dvc_type"    : constants.CYBEP,
                "user_info"   : user_dict
            }
            devices.append(device_dict)
    
        logger.debug("\nxxxxxxxx Cigent Devices xxxxxxxx")    #CTO
        cD = self.cigDV
        for cd in cD:

            user = User(cd.usrId, None)
            user.getUserInfo()
            user_dict = {} 
            user_dict = user.crtUserDict()

            device_dict = {
                "dvc_id"      : cd.dvcId,
                "dvc_name"    : cd.dvcNm,
                "deviceId"    : cd.deviceId,
                "last_chk_in" : cd.lastChkIn,
                "adc_on"      : cd.aDCon,
                "alert_cnt"   : cd.alertCnt,
                "cmd_list"    : cd.commands,
                "dvc_type"    : constants.CIGDV,
                "user_info"   : user_dict
            }
            devices.append(device_dict)
    
        return(devices)
    
    #CDD - Create Dictionary of Devices




            
# Customer class ---------------------------------------------------------------------------                            
                           

# Device class -----------------------------------------------------------------------------                            
class Device:

    '''All the devices: Recon Sentinel, Enterprise RS, 
           Cyberstack EndPoint, and Cigent Devices use this class for intantiation.'''

    def __init__(self, usrId = None, dvcId = None, 
                 dvcNm = None, dvcTypNo = None, deviceId = None, custCode = None,
                 lastChkIn = None, aDCon = None, alertCnt = None,
                 commands = [],
                 offlConnHosts = [], onliConnHosts = [],
                 trstConnHosts = [], unkwConnHosts = [],
                 unblConnHosts = [], blckConnHosts = [],
                 alertListDict = []):

        self.usrId     = usrId
        self.dvcId     = dvcId
        self.dvcNm     = dvcNm
        self.dvcTypNo  = dvcTypNo
        self.deviceId  = deviceId
        self.custCode  = custCode
        self.lastChkIn = lastChkIn
        self.aDCon     = aDCon
        self.alertCnt  = alertCnt
        #self.response  = response(status="OK", context=None)

        # Device Level Window
        self.commands  = commands
        self.offlConnHosts = offlConnHosts    # Offline Connected Hosts 
        self.onliConnHosts = onliConnHosts    # Online Connected Hosts       
        self.trstConnHosts = trstConnHosts    # Trusted Connected Hosts       
        self.unkwConnHosts = unkwConnHosts    # Unknowned Connected Hosts       
        self.unblConnHosts = unblConnHosts    # Unblocked Connected Hosts       
        self.blckConnHosts = blckConnHosts    # Blocked Connected Hosts       
        self.alertListDict = alertListDict    # Alert Dictionary List (1 Dict = 1 Rec)      
     
        # Counts
        self.dvcDataCounts = {
                                 "attackAlerts"    : 0,
                                 "messageAlerts"   : 0,
                                 "rougueDvcs"      : 0,
                                 "rougueSvcAlerts" : 0,
                                 "scanAlerts"      : 0,
                                 "onliCH"          : 0,
                                 "offlCH"          : 0,
                                 "trstCH"          : 0,
                                 "unkwCH"          : 0,
                                 "blckCH"          : 0,
                                 "unblCH"          : 0
                              }
        #self.dvcDataCounts = {}
        

        #self.response  = make_response("", "", "")

   
    def getADCstatus(self):
        #logger.debug("\n\nInside getADCstatus()")  #CTO
        
        with get_db_connection(database=self.deviceId) as devconn, get_db_cursor(devconn) as cursor:
            #logger.debug("AFT get_db_connection()")  #CTO

            try:
                #logger.debug("getADCstatus.sql tbf")  #CTO
                sql = "SELECT value " \
                      "  FROM config " \
                      " WHERE option = 'countermeasures'"
                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                #logger.debug("getADCstatus.sql = %s" % sql) #CTO
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    self.aDCon = int(row[0])
                else:
                    self.aDCon = None

                self.response = create_response("OK")

            except Exception as e:
                self.aDCon = constants.GET_ADC_STATUS_FAILED
                self.response = make_response(constants.GET_ADC_STATUS_FAILED, 
                                                       "Device.getADCstatus", 
                                                       constants.BAD_REQUEST_400)



    def getLastChkIn(self):

        with get_db_connection(database=self.deviceId) as devconn, get_db_cursor(devconn) as cursor:
            try:
                sql = "  SELECT status_timestamp " \
                      "    FROM status " \
                      "   WHERE state = 1 " \
                      "ORDER BY status_timestamp DESC"
                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                #logger.debug("getLastChkIn.sql = %s" % sql) #CTO

                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    self.lastChkIn = row[0]
                else:
                    self.lastChkIn = None

                self.response = create_response("OK")

            except Exception as e:
                self.lastChkIn = constants.GET_LAST_CHECK_IN_FAILED
                self.response = make_response(constants.GET_LAST_CHECK_IN_FAILED, 
                                                       "Device.getLastChkIn", 
                                                       constants.BAD_REQUEST_400)
     
    def getAlertCnt(self):

        with get_db_connection(database=self.deviceId) as devconn, get_db_cursor(devconn) as cursor:
            try:
                sql = "SELECT COUNT(*) " \
                      "  FROM alerts " \
                      " WHERE ack = 0"
                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                #logger.debug("getAlertCnt.sql = %s" % sql) #CTO
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    self.alertCnt = int(row[0])
                else:
                    self.alertCnt = None

                self.response = create_response("OK")

            except Exception as e:
                self.alertCnt = constants.ALERT_GET_COUNT_FAILED
                self.response = make_response(constants.ALERT_GET_COUNT_FAILED, 
                                                       "Device.getAlertCnt", 
                                                       constants.BAD_REQUEST_400)



    def getOthData(self):

        self.getADCstatus()

        self.getLastChkIn()

        self.getAlertCnt()

        self.getCommands()



    def setDeviceId(self, deviceid):
        self.deviceId = deviceid

    def getRegInfo(self):
        #logger.debug("\n\nInside getCommands()")  #CTO
        
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn) as cursor:
            #logger.debug("AFT get_db_connection()")  #CTO

            try:
                assetTable = "sentinels"
                sql = "SELECT name, cust_code" \
                      "  FROM %s" \
                      " WHERE deviceid = \"%s\"" % (assetTable, self.deviceId)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    self.dvcNm    = row[0]
                    self.custCode = row[1]
                else:
                    self.dvcNm    = ""
                    self.custCode = ""
                    
            except Exception as e:
                logger.debug(e) #CTO
                self.response = make_response(constants.DEVICE_REGISTRATION_ERROR,
                                                       "Device.getRegInfo", 
                                                       constants.BAD_REQUEST_400)

    # Get Offline Connected Hosts Attributes


    def getCommands(self):
        #logger.debug("\n\nInside getCommands()")  #CTO
        
        with get_db_connection(database=self.deviceId) as devconn, get_db_cursor(devconn) as cursor:
            #logger.debug("AFT get_db_connection()")  #CTO

            try:
                command_list = []
                #logger.debug("getCommands.sql tbf")  #CTO
                sql = "SELECT id, command_timestamp, command, status " \
                      "  FROM command " \
                    "ORDER BY command"
                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                #logger.debug("getCommands.sql = %s" % sql) #CTO
                cursor.execute(sql)
                rows = cursor.fetchall()
                if rows:
                    command = []
                    for row in rows:
                        command = [row[0], row[1], row[2], row[3]]
                        command_list.append(command)

                self.commands = command_list

                self.response = "OK"

            except Exception as e:
                logger.debug(e) #CTO
                self.commands = [constants.GET_COMMANDS_FAILED]
                self.response = make_response(constants.GET_COMMANDS_FAILED, 
                                                       "Device.getCommands", 
                                                       constants.BAD_REQUEST_400)

    # Get Offline Connected Hosts Attributes
    def getOfflineConnHosts(self):
        logger.debug("\n\nnside getOfflineConnHosts()")  #CTO
        
        with get_db_connection(database=self.deviceId) as devconn, get_db_cursor(devconn) as cursor:
            logger.debug("AFT get_db_connection()")  #CTO

            try:
                logger.debug("getOfflineConnHosts.sql tbf")  #CTO
                sql = "    SELECT H.id, H.ip, H.mac, H.os_name, H.os_vendor," \
                      "           H.mac_vendor, H.state, H.hostname " \
                      "      FROM hosts H " \
                      "     WHERE H.state = \'%s\'    AND " \
                      "           H.deviceid = \'%s\'" % (constants.OFFLINE, self.deviceId)

                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                logger.debug("\ngetUnknownConnHosts.sql = %s\n" % sql) #CTO
                cursor.execute(sql)
                rows = cursor.fetchall()
                #logger.debug("\nrows = %s\n" % rows) #CTO
                if rows:
                    offchDict = {}
                    self.offlConnHosts = []
                    for row in rows:
                        offchDict = {
                                    'id'        : row[0],
                                    'deviceid'  : self.deviceId,
                                    'ip'        : row[1],
                                    'mac'       : row[2],
                                    'os_name'   :  row[3],
                                    'os_vendor'  : row[4],
                                    'mac_vendor' : row[5],
                                    'state'      :  row[6],
                                    'hostname'   : row[7] #,
                                    #'devicename' : row[8],
                        }
                        #logger.debug("\noffchDict = %s\n" % offchDict) #CTO
                        self.offlConnHosts.append(offchDict)

                #logger.debug("\nself.offlConnHosts = %s \n" % self.offlConnHosts) #CTO
                self.response = "OK"

            except Exception as e:
                self.offlConnHosts = [constants.GET_OFFLINE_CONN_HOSTS_FAILED]
                self.response = make_response(constants.GET_OFFLINE_CONN_HOSTS_FAILED, 
                                                       "Device.getOfflineConnHosts", 
                                                       constants.BAD_REQUEST_400)
    # Get Online Connected Hosts Attributes
    def getOnlineConnHosts(self):
        logger.debug("\n\nInside getOnlineConnHosts()")  #CTO
        
        with get_db_connection(database=self.deviceId) as devconn, get_db_cursor(devconn) as cursor:
            #logger.debug("AFT get_db_connection()")  #CTO

            try:
                #logger.debug("getOnlineConnHosts.sql tbf")  #CTO
                sql = "    SELECT H.id, H.ip, H.mac, H.os_name, H.os_vendor, " \
                      "           H.mac_vendor, H.state, H.hostname " \
                      "      FROM hosts H " \
                      "     WHERE H.state = \'%s\'    AND " \
                      "           H.deviceid = \'%s\'" % (constants.ONLINE, self.deviceId)

                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                logger.debug("\ngetOnlineConnHosts.sql = %s\n" % sql) #CTO
                cursor.execute(sql)
                rows = cursor.fetchall()
                #logger.debug("\nrows = %s\n" % rows) #CTO
                if rows:
                    onlchDict = {}
                    self.onliConnHosts = []
                    for row in rows:
                        onlchDict = {
                                    'id'        : row[0],
                                    'deviceid'  : self.deviceId,
                                    'ip'        : row[1],
                                    'mac'       : row[2],
                                    'os_name'   :  row[3],
                                    'os_vendor'  : row[4],
                                    'mac_vendor' : row[5],
                                    'state'      :  row[6],
                                    'hostname'   : row[7] #,
                                    #'devicename' : row[8],
                        }
                        self.onliConnHosts.append(onlchDict)

                #self.response = "OK"
                self.response = create_response("OK")

            except Exception as e:
                self.onliConnHosts = [constants.GET_ONLINE_CONN_HOSTS_FAILED]
                self.response = make_response(constants.GET_ONLINE_CONN_HOSTS_FAILED, 
                                                       "Device.getOnlineConnHosts", 
                                                       constants.BAD_REQUEST_400)
    # Return the self.onliConnHosts Dictionary
    def retOnlineConnHosts(self):
        self.getOnlineConnHosts()
        return(self.onliConnHosts)

    # Get Blocked Connected Hosts Attributes
    def getBlockedConnHosts(self):
        logger.debug("\n\nInside getBlockedConnHosts()\n")  #CTO
        
        with get_db_connection(database=self.deviceId) as devconn, get_db_cursor(devconn) as cursor:
            logger.debug("AFT get_db_connection()")  #CTO

            try:
                #logger.debug("getBlockedConnHosts.sql tbf")  #CTO
                sql = "    SELECT H.id, H.ip, H.mac, H.os_name, H.os_vendor, " \
                      "           H.mac_vendor, H.state, H.hostname " \
                      "      FROM hosts H " \
                      "INNER JOIN countermeasures C " \
                      "     WHERE H.ip = C.target_ip AND " \
                      "	          C.active = 1       AND " \
                      "           H.deviceid = \'%s\'" % (self.deviceId)

                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                #logger.debug("getBlockedConnHosts.sql = %s" % sql) #CTO
                cursor.execute(sql)
                rows = cursor.fetchall()
                logger.debug("\nrows = %s\n" % rows) #CTO
                if rows:
                    bchDict = {}
                    self.blckConnHosts = []
                    for row in rows:
                        bchDict = {
                                   'id'        : row[0],
                                   'deviceid'  : self.deviceId,
                                   'ip'        : row[1],
                                   'mac'       : row[2],
                                   'os_name'   :  row[3],
                                   'os_vendor'  : row[4],
                                   'mac_vendor' : row[5],
                                   'state'      :  row[6],
                                   'hostname'   : row[7] #,
                                   #'devicename' : row[8],
                        }
                        self.blckConnHosts.append(bchDict)

                self.response = create_response("OK")

            except Exception as e:
                self.blckConnHosts = [constants.GET_BLOCKED_CONN_HOSTS_FAILED]
                self.response = make_response(constants.GET_BLOCKED_CONN_HOSTS_FAILED, 
                                                       "Device.getBlockedConnHosts", 
                                                       constants.BAD_REQUEST_400)

    # Get Unblocked Connected Hosts Attributes
    def getUnblckdConnHosts(self):
        logger.debug("\n\nInside getUnblckdConnHosts()\n")  #CTO
        
        with get_db_connection(database=self.deviceId) as devconn, get_db_cursor(devconn) as cursor:
            #logger.debug("AFT get_db_connection()")  #CTO

            try:
                #logger.debug("getUnblckdConnHosts.sql tbf")  #CTO
                sql = "    SELECT H.id, H.ip, H.mac, H.os_name, H.os_vendor, " \
                      "           H.mac_vendor, H.state, H.hostname " \
                      "      FROM hosts H " \
                      "INNER JOIN countermeasures C " \
                      "     WHERE H.ip <> C.target_ip AND " \
                      "           H.deviceid = \'%s\'" % (self.deviceId)

                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                #logger.debug("getUnblckdConnHosts.sql = %s" % sql) #CTO
                cursor.execute(sql)
                rows = cursor.fetchall()
                if rows:
                    uchDict = {}
                    self.unblConnHost = []
                    for row in rows:
                        uchDict = {
                                   'id'        : row[0],
                                   'deviceid'  : self.deviceId,
                                   'ip'        : row[1],
                                   'mac'       : row[2],
                                   'os_name'   :  row[3],
                                   'os_vendor'  : row[4],
                                   'mac_vendor' : row[5],
                                   'state'      :  row[6],
                                   'hostname'   : row[7] #,
                                   #'devicename' : row[8],
                        }
                        self.unblConnHosts.append(uchDict)

                self.response = create_response("OK")

            except Exception as e:
                self.unblConnHosts = [constants.GET_UNBLCKD_CONN_HOSTS_FAILED]
                self.response = make_response(constants.GET_UNBLCKD_CONN_HOSTS_FAILED, 
                                                       "Device.getUnblckdConnHosts", 
                                                       constants.BAD_REQUEST_400)

    # Get Unknown Connected Hosts Attributes
    def getUnknownConnHosts(self):
        logger.debug("\n\nInside getUnknownConnHosts()\n")  #CTO
        
        with get_db_connection(database=self.deviceId) as devconn, get_db_cursor(devconn) as cursor:
            #logger.debug("AFT get_db_connection()")  #CTO

            try:
                #logger.debug("getUnknownConnHosts.sql tbf")  #CTO
                sql = "    SELECT H.id, H.ip, H.mac, H.os_name, H.os_vendor, " \
                      "           H.mac_vendor, H.state, H.hostname " \
                      "      FROM hosts H " \
                      "     WHERE H.authorized <> %s  AND " \
                      "           H.deviceid = \'%s\'" % (constants.AUTHORIZED, self.deviceId)

                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                logger.debug("getUnknownConnHosts.sql = %s" % sql) #CTO
                cursor.execute(sql)
                rows = cursor.fetchall()
                if rows:
                    ukchDict = {}
                    self.unkwConnHosts = []
                    for row in rows:
                        ukchDict = {
                                    'id'        : row[0],
                                    'deviceid'  : self.deviceId,
                                    'ip'        : row[1],
                                    'mac'       : row[2],
                                    'os_name'   :  row[3],
                                    'os_vendor'  : row[4],
                                    'mac_vendor' : row[5],
                                    'state'      :  row[6],
                                    'hostname'   : row[7] #, 
                                    #'devicename' : row[8],
                        }
                        self.unkwConnHosts.append(ukchDict)

                self.response = create_response("OK")

            except Exception as e:
                logger.debug(e) #CTO
                self.unkwConnHosts = [constants.GET_UNKNOWN_CONN_HOSTS_FAILED]
                self.response = make_response(constants.GET_UNKNOWN_CONN_HOSTS_FAILED, 
                                                       "Device.getUnknownConnHosts", 
                                                       constants.BAD_REQUEST_400)

    # Get Trusted Connected Hosts Attributes
    def getTrustedConnHosts(self):
        logger.debug("\n\nInside getTrustedConnHosts()\n")  #CTO
        
        with get_db_connection(database=self.deviceId) as devconn, get_db_cursor(devconn) as cursor:
            #logger.debug("AFT get_db_connection()")  #CTO

            try:
                #logger.debug("getTrustedConnHosts.sql tbf")  #CTO
                sql = "    SELECT H.id, H.ip, H.mac, H.os_name, H.os_vendor, " \
                      "           H.mac_vendor, H.state, H.hostname " \
                      "      FROM hosts H " \
                      "     WHERE H.authorized = %s AND " \
                      "           H.deviceid = \'%s\'" % (constants.AUTHORIZED, self.deviceId)

                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                logger.debug("getTrustedConnHosts.sql = %s" % sql) #CTO
                cursor.execute(sql)
                rows = cursor.fetchall()
                if rows:
                    tchDict = {}
                    self.trstConnHosts = []
                    for row in rows:
                        tchDict = {
                                    'id'        : row[0],
                                    'deviceid'  : self.deviceId,
                                    'ip'        : row[1],
                                    'mac'       : row[2],
                                    'os_name'   :  row[3],
                                    'os_vendor'  : row[4],
                                    'mac_vendor' : row[5],
                                    'state'      :  row[6],
                                    'hostname'   : row[7] #,
                                    #'devicename' : row[8],
                        }
                        self.trstConnHosts.append(tchDict)

                self.response = create_response("OK")


            except Exception as e:
                logger.debug(e) #CTO
                self.trstConnHosts = [constants.GET_TRUSTED_CONN_HOSTS_FAILED]
                self.response = make_response(constants.GET_TRUSTED_CONN_HOSTS_FAILED, 
                                                       "Device.getTrustedConnHosts", 
                                                       constants.BAD_REQUEST_400)

    # Get Alert List of Dictionary/ies
    def getAlertListDict(self):
        logger.debug("\n\nInside getAlertListDict()\n")  #CTO
        
        with get_db_connection(database=self.deviceId) as devconn, get_db_cursor(devconn) as cursor:
            #logger.debug("AFT get_db_connection()")  #CTO

            try:
                logger.debug("getAlertListDict.sql tbf")  #CTO
                sql = "SELECT id, deviceid, alert_time, hostname, message, " \
                      "severity, ip, alert_type, notified, ack, mac FROM alerts " \
                      "WHERE deviceid = \"%s\"" \
                      "ORDER BY alert_time DESC" % (self.deviceId)
                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                logger.debug("getAlertListDict.sql = %s" % sql) #CTO

                cursor.execute(sql)
                rows = cursor.fetchall()
                if not rows:
                    return create_response([])

                logger.debug("\nDevice.getAlertListDict(): deviceid = %s, cursor.rowcount = %s -----" % (self.deviceId, cursor.rowcount))
                self.alertListDict = []
                for row in rows:
                    sent_dict = {
                        'id'           : row[0],
                        'deviceid'     : row[1],
                        'mac'          : row[10],
                        'alert_time'   : row[2],
                        'hostname'     : row[3],
                        'message'      : row[4],
                        'severity'     : row[5],
                        'ip'           : row[6],
                        'alert_type'   : row[7],
                        'notified'     : row[8],
                        'acknowledged' : row[9]
                    }
                    self.alertListDict.append(sent_dict)



            except Exception as e:
                logger.debug(e) #CTO
                self.alertListDict = [constants.GET_ALERT_LIST_DICT_FAILED]
                self.response = make_response(constants.GET_ALERT_LIST_DICT_FAILED, 
                                                       "Device.getAlertListDict", 
                                                       constants.BAD_REQUEST_400)

    def getDvcDataCounts(self):

        with get_db_connection(database=self.deviceId) as devconn, get_db_cursor(devconn) as cursor:

            try: #Alerts
                ALRT_ATT = "attack"
                ALRT_MSG = "message"
                ALRT_ROG = "rogue"
                ALRT_RSV = "rogueservice"
                ALRT_SCN = "scan"
                ALRT_OLY = "rogueonly"
                alertTypes = [ALRT_ATT, ALRT_MSG, ALRT_ROG, ALRT_RSV, ALRT_SCN, ALRT_OLY]
                alertCnt = []
                for alert_type in alertTypes:
                    sql = " SELECT COUNT(*) " \
                          "   FROM alerts   " \
                          "  WHERE alert_type = \"%s\" AND ack = 0 " % (alert_type)
                    logger.debug("getDvcDataCounts Alerts sql tbc")  #CTO
                    logger.debug("sql = %s" % sql)  #CTO
                    cursor.execute(sql)
                    row = cursor.fetchone()
                    if row:
                        alertCnt.append(row[0])
                    else:
                        alertCnt.append(0)
 
            except Exception as e:
                self.alertListDict = [constants.GET_ALERT_LIST_DICT_FAILED]
                #self.response = make_response(constants.GET_ALERT_LIST_DICT_FAILED, 
                #                                       "Device.getDvcDataCounts", 
                #                                       constants.BAD_REQUEST_400)
                logger.error(e) 
                return create_response(status=constants.BAD_REQUEST_400)

            
            try: #offlineConnHosts
                logger.debug("getDvcDataCounts offlCH tbf")  #CTO
                sql = "    SELECT COUNT(*) " \
                      "      FROM hosts H  " \
                      "     WHERE H.state = \'%s\'"  % (constants.OFFLINE)

                logger.debug("\ngetDvcDataCounts = %s\n" % sql) #CTO
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    offlCH = row[0]                  
                else:
                    offlCH = 0

            except Exception as e:
                self.offlConnHosts = [constants.GET_OFFLINE_CONN_HOSTS_FAILED]
                #self.response = make_response(constants.GET_OFFLINE_CONN_HOSTS_FAILED, 
                #                                       "Device.getDvcDataCounts", 
                #                                       constants.BAD_REQUEST_400)
                logger.error(e) 
                return create_response(status=constants.BAD_REQUEST_400)

            try: #onlineConnHosts
                logger.debug("getDvcDataCounts onliCH tbf")  #CTO
                sql = "    SELECT COUNT(*) " \
                      "      FROM hosts  H " \
                      "     WHERE H.state = \'%s\'"  % (constants.ONLINE)

                logger.debug("\ngetDvcDataCounts = %s\n" % sql) #CTO
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    onliCH = row[0]                  
                else:
                    onliCH = 0

            except Exception as e:
                self.onliConnHosts = [constants.GET_ONLINE_CONN_HOSTS_FAILED]
                #self.response = make_response(constants.GET_ONLINE_CONN_HOSTS_FAILED, 
                #                                       "Device.getDvcDataCounts", 
                #                                       constants.BAD_REQUEST_400)
                logger.error(e) 
                return create_response(status=constants.BAD_REQUEST_400)

            try: # blckConnHosts
                #logger.debug("getBlockedConnHosts.sql tbf")  #CTO
                sql = "    SELECT COUNT(*) " \
                      "      FROM hosts H " \
                      "INNER JOIN countermeasures C      " \
                      "     WHERE H.ip = C.target_ip AND " \
                      "	          C.active = 1" 

                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    blckCH = row[0]                  
                else:
                    blckCH = 0

            except Exception as e:
                self.blckConnHosts = [constants.GET_BLOCKED_CONN_HOSTS_FAILED]
                #self.response = make_response(constants.GET_BLOCKED_CONN_HOSTS_FAILED, 
                #                                       "Device.getDvcDataCounts",
                #                                       constants.BAD_REQUEST_400)
                logger.error(e) 
                return create_response(status=constants.BAD_REQUEST_400)

            try: # unblConnHosts
                #logger.debug("getUnBlockedConnHosts.sql tbf")  #CTO
                sql = "    SELECT COUNT(*) " \
                      "      FROM hosts H " \
                      "INNER JOIN countermeasures C      " \
                      "     WHERE H.ip = C.target_ip AND " \
                      "	          C.active = 1" 

                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    unblCH = row[0]                  
                else:
                    unblCH = 0

            except Exception as e:
                self.unblConnHosts = [constants.GET_UNBLCKD_CONN_HOSTS_FAILED]
                #self.response = make_response(constants.GET_UNBLCKD_CONN_HOSTS_FAILED, 
                #                                       "Device.getDvcDataCounts",
                #                                       constants.BAD_REQUEST_400)
                logger.error(e) 
                return create_response(status=constants.BAD_REQUEST_400)

            try: #trstConnHosts
                #logger.debug("getTrustedConnHosts.sql tbf")  #CTO
                sql = "    SELECT COUNT(*) " \
                      "      FROM hosts H " \
                      "     WHERE H.authorized = %s " % (constants.AUTHORIZED)

                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                #logger.debug("getTrustedConnHosts.sql = %s" % sql) #CTO
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    trstCH = row[0]                  
                else:
                    trstCH = 0

            except Exception as e:
                self.trstConnHosts = [constants.GET_TRUSTED_CONN_HOSTS_FAILED]
                #self.response = make_response(constants.GET_TRUSTED_CONN_HOSTS_FAILED, 
                #                                       "Device.getDvcDataCounts",
                #                                       constants.BAD_REQUEST_400)
                logger.error(e) 
                return create_response(status=constants.BAD_REQUEST_400)

            try: #unkwConnHosts
                #logger.debug("getTrustedConnHosts.sql tbf")  #CTO
                sql = "    SELECT COUNT(*) " \
                      "      FROM hosts H " \
                      "     WHERE H.authorized <> %s " % (constants.AUTHORIZED)

                #sql = "SELECT grpname FROM sentinels" #CTO - Negative test
                #logger.debug("getTrustedConnHosts.sql = %s" % sql) #CTO
                cursor.execute(sql)
                row = cursor.fetchone()
                if row:
                    unkwCH = row[0]                  
                else:
                    unkwCH = 0

            except Exception as e:
                self.unkwConnHosts = [constants.GET_UNKNOWN_CONN_HOSTS_FAILED]
                #elf.response = make_response(constants.GET_UNKNOWN_CONN_HOSTS_FAILED, 
                #                                      "Device.getDvcDataCounts",
                #                                      constants.BAD_REQUEST_400)
                logger.error(e) 
                return create_response(status=constants.BAD_REQUEST_400)

        # Counts
        self.dvcDataCounts = {
                                 "attackAlerts"    : alertCnt[0],
                                 "messageAlerts"   : alertCnt[1],
                                 "rougueAlerts"    : alertCnt[2],
                                 "rougueSvcAlerts" : alertCnt[3],
                                 "scanAlerts"      : alertCnt[4],
                                 "onliCH"          : onliCH,
                                 "offlCH"          : offlCH,
                                 "trstCH"          : trstCH,
                                 "unkwCH"          : unkwCH,
                                 "blckCH"          : blckCH,
                                 "unblCH"          : unblCH
                              }



    def conHostStatSel(self, status):

        #chStat_offli = CHSTAT_OFFLI
        #chStat_onlin = CHSTAT_ONLIN
        #chStat_unblc = CHSTAT_UNBLC
        #chStat_blckd = CHSTAT_BLCKD
        #chStat_unkwn = CHSTAT_UNKWN
        #chStat_trstd = CHSTAT_TRSTD

        offlCH = self.offlConnHosts
        onliCH = self.onliConnHosts
        trstCH = self.trstConnHosts
        unkwCH = self.unkwConnHosts
        unblCH = self.unblConnHosts
        blckCH = self.blckConnHosts

        switcher = {
             1 : offlCH,
             2 : onliCH,
             3 : trstCH,
             4 : unkwCH,
             5 : unblCH,
             6 : blckCH
        }

        return switcher.get(status)


    # Print the Connected Hosts Given the Status
#    def prnConnHostsAttrDict(self, connHostStatus):
#
#        connHostsDictList = conHostStatSel(connHostStatus)
#
#        for connHostsDict in connHostDictList:
#            logger.debug("id  = %s, deviceid = %s, ip = %s, mac = %s, " \
#                  % (connHostsDict['id'], connHostsDict['deviceid'], connHostsDict['ip'], connHostsDict['mac']))
#            logger.debug(" os_name = %s, os_vendor = %s, mac_vendor = %s, state = %s, hostname = %s " \
#                  % (connHostsDict['os_name'], connHostsDict['os_vendor'], connHostsDict['mac_vendor'], \
#                     connHostsDict['state'], (connHostsDict['hostname']))   
#            #logger.debug(" devicename = %s " % (connHostsDict['devicename']))

# Device class -----------------------------------------------------------------------------                            

# User class ----------------------------------------------------------------------------- 
class User:

    '''User info will be added as needed...'''

    def __init__(self, usrId, usrNm = None):

        self.usrId     = usrId
        self.usrNm     = usrNm


    def getUserInfo(self):

        # additional info to be added later as needed ...

        with get_db_connection(database=mdb) as rsuserconn, get_db_cursor(rsuserconn) as cursor:
            try:
                sql = "SELECT username FROM users " \
                      "WHERE id =\"%s\"" % (self.usrId)
                cursor.execute(sql)
                row = cursor.fetchone()
                if not row:
                    return make_response(constants.USER_NOT_FOUND,
                                                  "User.getUserInfo",
                                                  constants.NOT_FOUND_404)

                self.usrNm = row[0]

            except Exception as e:
                return make_response(constants.USER_INFO_FAIL,
                                              "User.getUserInfo",
                                              constants.BAD_REQUEST_400)

    def getUserWithLevelInfo(self, lvl_id):

        with get_db_connection(database=mdb) as rsuserconn, get_db_cursor(rsuserconn) as cursor:
            try:
                sql = "SELECT id, username " \
                      "  FROM users " \
                      " WHERE lvl_id =\"%s\"" % (lvl_id)
                cursor.execute(sql)
                rows = cursor.fetchall()
                if not rows:
                    return make_response(constants.USER_WITH_GIVEN_LEVEL_ID_NOT_FOUND,
                                                  "User.getUserWithLevelInfo",
                                                  constants.NOT_FOUND_404)

                users = []
                for row in rows:
                    self.usrId = row[0]
                    self.usrNm = row[1]
                    users.append(self.crtUserDict())
                   
                return(users)
                    
            except Exception as e:
                return make_response(constants.USER_WITH_GIVEN_LEVEL_ID_INFO_FAIL,
                                     "User.getUserWithLevelInfo",
                                     constants.BAD_REQUEST_400)



    def crtUserDict(self):

        userDict = {}
        userDict = {

           "user_id"  : self.usrId,
           "username" : self.usrNm,

        }

        return(userDict)


    def crtUserListDict(self, users):
        addUser = True
        for user in users:
            if user:
                if user["user_id"] == self["user_id"]:
                    addUser = False
                    break

        if addUser == True:
            self.getUserInfo()
            users.append(self.crtUserDict())

        return (users)



# User class -----------------------------------------------------------------------------    

# Group class ----------------------------------------------------------------------------- 
class Group:

    '''Group info will include a list of Administrators, if there are!'''

    def __init__(self, grpId, grpLvl = None, startDttm = None, grpNm = None, adminILst = []):

        methodName = sys._getframe().f_code.co_name

        self.grpId     = grpId
        self.grpLvl    = grpLvl
        self.startDttm = startDttm
        self.grpNm     = grpNm
        self.adminILst = adminILst
        self.response = make_response(constants.OK_200, methodName, constants.OK_200)


    def getGroupInfo(self):

        # additional info to be added later as needed ...

        with get_db_connection(database=mdb) as rsuserconn, get_db_cursor(rsuserconn) as cursor:
            try:
                sql = "SELECT G.id, G.grplvl, G.start_dttm, G.grpname, " \
                      "       A.admin_id, A.start_dttm, U.username " \
                      "  FROM groups G, admin_group A, users U " \
                      " WHERE G.id = %s         AND " \
                      "       A.grp_id = G.id   AND " \
                      "       A.admin_id = U.id AND " \
                      "       A.active = %s         " % (self.grpId, constants.ACTIVE_STATUS)
                cursor.execute(sql)
                rows = cursor.fetchall()
                if not rows:
                    self.response = make_response(constants.GROUP_OR_ADMINS_NOT_FOUND,
                                                           "Group.getGroupInfo",
                                                           constants.NOT_FOUND_404)


                adminILst = []
                for row in rows:
                    if self.startDttm == None:
                        self.grpId     = row[0]
                        self.grpLvl    = row[1]
                        self.startDttm = row[2]
                        self.grpNm     = row[3]
                    adminDict = {}
                    adminDict = {
                        "adminId"   : row[4],
                        "startDttm" : row[5],
                        "adminNm"   : row[6]
                    }
                    self.adminILst.append(adminDict)                   

            except Exception as e:
                self.response = make_response(constants.GROUP_INFO_FAIL,
                                                       "Group.getGroupInfo",
                                                       constants.BAD_REQUEST_400)

    def crtGroupDict(self):

        grpDict = {
             "grpId"     : self.grpId,
             "grpLvl"    : self.grpLvl,
             "startDttm" : self.startDttm,
             "grpNm"     : self.grpNm,
             "adminILst" : self.adminILst
        }

        return(grpDict)


# Group class ----------------------------------------------------------------------------- 
