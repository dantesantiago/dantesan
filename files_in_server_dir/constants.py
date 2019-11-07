# Success Codes
OK_200 = "200 OK"
NO_CONTENT_204 = "204 No Content"
CREATED_201 = "201 Created"
ACCEPTED_202 = "202 Accepted"

# Error Status Codes
BAD_REQUEST_400 = "400 Bad Request"
NOT_AUTHORIZED_401 = "401 Not Authorized"
PAYMENT_REQ_402 = "402 Payment Required"
FORBIDDEN_403 = "403 Forbidden"
NOT_FOUND_404 = "404 Not Found"
NOT_ACCEPTABLE_406 = "406 Not Acceptable"
REQUEST_TIMEOUT_408 = "408 Request Timeout"
CONFLICT_409 = "409 Conflict"
LOCKED_423 = "423 Locked"

# Expiration Values
SUB_GOOD = 1
SUB_30_DAY = 2
SUB_EXPIRE = 3

# Health Fields
CRITICAL = 1
WARNING = 2
GOOD = 3
UNKNOWN = 4

# State Fields
NOT_RESPONDING = 0
IDLE = 1
OFFLINE = 2
REBOOTING = 3
REGISTERING = 5
FACTORY_RESET = 6
SONAR = 7
TRUST_ALL = 8
UNTRUST_ALL = 9
PENDING = 99

# Login Error Messages
LOGIN_VERIFY_FAIL = "LOGIN_VERIFY_FAIL"
TOKEN_SIG_FAIL = "TOKEN_SIG_FAIL"
TOKEN_INV_FAIL = "TOKEN_INV_FAIL"

# Sentinel Error Messages
DEVICE_NOT_RESPONDING = "DEVICE_NOT_RESPONDING"
SENTINEL_ONLINE_STATUS = "SENTINEL_ONLINE_STATUS"
DEVICE_NOT_FOUND = "DEVICE_NOT_FOUND"
UNAUTHORIZE_FAIL = "UNAUTHORIZE_FAIL"
SENTINELS_FAIL = "SENTINELS_FAIL"
REGISTER_FAIL = "REGISTER_FAIL"
SENTINEL_FAIL = "SENTINEL_FAIL"
EXPIRE_FAIL = "EXPIRE_FAIL"
NOT_AUTHORIZED = "NOT_AUTHORIZED"
DEVICE_REGISTERED = "DEVICE_REGISTERED"
EMPTY_SENTINELS = "EMPTY_SENTINELS"
CHECK_SENTINEL_FAIL = "CHECK_SENTINEL_FAIL"
FAIL_SENTINEL_EXPDATE = "FAIL_SENTINEL_EXPDATE"
GET_NAME_FAIL = "GET_NAME_FAIL"
NAME_FAIL = "NAME_FAIL"
FAIL_UPDATE_EXPDATE = "FAIL_UPDATE_EXPDATE"

# Alerts Error Messages
ALERTS_FAIL = "ALERTS_FAIL"
EMPTY_ALERTS = "EMPTY_ALERTS"
ALERT_ACK_FAIL = "ALERT_ACK_FAIL"
ALERT_UPDATE_FAIL = "ALERT_UPDATE_FAIL"
ALERT_CREATE_FAIL = "ALERT_CREATE_FAIL"
ALERT_DELETE_ALL_FAIL = "ALERT_DELETE_ALL_FAIL"
ALERT_DELETE_FAIL = "ALERT_DELETE_FAIL"
ALERT_UNACK_FAIL = "ALERT_UNACK_FAIL"
NO_ALERT_TYPE = "NO_ALERT_TYPE"
ALERT_CONFIG_FAIL = "ALERT_CONFIG_FAIL"

# Hosts Error Messages
EMPTY_HOSTS = "EMPTY_HOSTS"
HOSTS_FAIL = "HOSTS_FAIL"
HOST_FAIL = "HOST_FAIL"
HOST_ADC_ENABLE_FAIL = "HOST_ADC_ENABLE_FAIL"
HOST_UPDATE_FAIL = "HOST_UPDATE_FAIL"
HOST_ADC_ENABLE_CM_FAIL = "HOST_ADC_ENABLE_CM_FAIL"
HOST_ADC_DISABLE_CM_FAIL = "HOST_ADC_DISABLE_CM_FAIL"
HOST_CREATE_FAIL = "HOST_CREATE_FAIL"
HOST_DELETE_FAIL = "HOST_DELETE_FAIL"
HOST_TRUST_FAIL = "HOST_TRUST_FAIL"
HOST_UNTRUST_FAIL = "HOST_UNTRUST_FAIL"
HOST_ALERT_FAIL = "HOST_ALERT_FAIL"
HOST_TRUST_CM_FAIL = "HOST_TRUST_CM_FAIL"
HOST_UNTRUST_CM_FAIL = "HOST_UNTRUST_CM_FAIL"
HOST_CM_FAIL = "HOST_CM_FAIL"

# Traps Error Messages
EMPTY_TRAPS = "EMPTY_TRAPS"
TRAPS_FAIL = "TRAPS_FAIL"
TRAP_CREATE_FAIL = "TRAP_CREATE_FAIL"
TRAP_DISABLE_FAIL = "TRAP_DISABLE_FAIL"
TRAP_DISABLE_CM_FAIL = "TRAP_DISABLE_CM_FAIL"
TRAP_ENABLE_FAIL = "TRAP_ENABLE_FAIL"
TRAP_UPDATE_FAIL = "TRAP_UPDATE_FAIL"
TRAP_ENABLE_CM_FAIL = "TRAP_ENABLE_CM_FAIL"

# Command Error Messages
SET_CMD_FAIL = "SET_CMD_FAIL"
SHUTDOWN_FAIL = "SHUTDOWN_FAIL"
REBOOT_FAIL = "REBOOT_FAIL"
REBOOT_STATUS_FAIL = "REBOOT_STATUS_FAIL"
FACTORY_RESET_FAIL = "FACTORY_RESET_FAIL"
HOST_CMD_FAIL = "HOST_CMD_FAIL"
HOSTS_CM_1_FAIL = "HOSTS_CM_1_FAIL"
HOSTS_CM_0_FAIL = "HOSTS_CM_0_FAIL"
START_SONAR_FAIL = "START_SONAR_FAIL"
STOP_SONAR_FAIL = "STOP_SONAR_FAIL"
LCD_OFF_FAIL = "LCD_OFF_FAIL"
LCD_ON_FAIL = "LCD_ON_FAIL"

# User Error Messages
USER_NOT_FOUND = "USER_NOT_FOUND"
USER_EXISTS = "USER_EXISTS"
USER_ID_MISMATCH = "USER_ID_MISMATCH"
USER_FAIL = "USER_FAIL"
USER_CREATE_FAIL = "USER_CREATE_FAIL"
USER_UPDATE_FAIL = "USER_UPDATE_FAIL"
USER_LOOKUP_FAIL = "USER_LOOKUP_FAIL"
PASS_VERIFY_FAIL = "PASS_VERIFY_FAIL"
PASS_UPDATE_FAIL = "PASS_UPDATE_FAIL"
LOGIN_UPDATE_FAIL = "LOGIN_UPDATE_FAIL"
EMAIL_USER_NOT_SET = "EMAIL_USER_NOT_SET"
EMAIL_FIND_FAIL = "EMAIL_FIND_FAIL"
EMAIL_IN_USE = "EMAIL_IN_USE"
USER_INFO_FAIL = "USER_INFO_FAIL"
USER_SENTINEL_REMOVE = "USER_SENTINEL_REMOVE"

USER_LEVEL_LOOKUP_FAIL = "USER_LEVEL_LOOKUP_FAIL"
# Verification Code Error Messages
CODE_SAVE_FAIL = "CODE_SAVE_FAIL"
CODE_EXPIRED = "CODE_EXPIRED"
CODE_NOT_FOUND = "CODE_NOT_FOUND"
CODE_FIND_FAIL = "CODE_FIND_FAIL"
CODE_REMOVE_FAIL = "CODE_REMOVE_FAIL"

# Misc
ADC_ENABLE_FAIL = "ADC_ENABLE_FAIL"
ADC_DISABLE_FAIL = "ADC_DISABLE_FAIL"
ADC_GET_STATUS_FAILED = "ADC_GET_STATUS_FAILED"
IP_DELETE_CM_FAIL = "IP_DELETE_CM_FAIL"
EMAIL_FAIL = "EMAIL_FAIL"
NEWSLETTER_FAIL = "NEWSLETTER_FAIL"
FAIL_PAYMENT_SAVE = "FAIL_PAYMENT_SAVE"
STATUS_TRUNC_FAIL = "STATUS_TRUNC_FAIL"
PORT_DELETE_FAIL = "PORT_DELETE_FAIL"
DEVICE_TOKEN_FAIL = "DEVICE_TOKEN_FAIL"
REMOVE_TOKEN_FAIL = "REMOVE_TOKEN_FAIL"
STRIPE_SUB_FAIL = "Failed to insert Stripe subscription"
SUPPORT_TICKET_FAIL = "SUPPORT_TICKET_FAIL"

#MSP - Managed Service Provider

LEVEL_ID_01 = 1
LEVEL_ID_02 = 2
LEVEL_ID_03 = 3
SET_USER_ID_FAIL = "Failed to change the assigned user id to sentinel."

GROUP_EXISTS = "GROUP_EXISTS"
GROUP_CREATE_FAIL = "GROUP_CREATE_FAIL"
GROUP_LOOKUP_FAIL = "GROUP_LOOKUP_FAIL"
GROUP_DOES_NOT_EXIST = "GROUP_DOES_NOT_EXIST"

ACTIVE_ADMIN_GROUP_EXISTS = "ACTIVE_ADMIN_GROUP_EXISTS"
ACTIVE_ADMIN_GROUP_DOES_NOT_EXIST = "ACTIVE_ADMIN_GROUP_DOES_NOT_EXIST"
ADMIN_GROUP_CREATE_FAIL = "ADMIN_GROUP_CREATE_FAIL"
ADMIN_GROUP_UPDATE_FAIL = "ADMIN_GROUP_UPDATE_FAIL"
ADMIN_GROUP_LOOKUP_FAIL = "ADMIN_GROUP_LOOKUP_FAIL"

ACTIVE_DEVICE_GROUP_EXISTS = "ACTIVE_DEVICE_GROUP_EXISTS"
ACTIVE_DEVICE_GROUP_DOES_NOT_EXIST = "ACTIVE_DEVICE_GROUP_DOES_NOT_EXIST"
DEVICE_GROUP_CREATE_FAIL = "DEVICE_GROUP_CREATE_FAIL"
DEVICE_GROUP_UPDATE_FAIL = "DEVICE_GROUP_UPDATE_FAIL"
DEVICE_GROUP_LOOKUP_FAIL = "DEVICE_GROUP_LOOKUP_FAIL"

WRONG_LEVEL_ID = "WRONG_LEVEL_ID"
USERNM_WRONG_LEVEL_ID = "USERNM_WRONG_LEVEL_ID"
SENTINEL_EXP_DATE = "SENTINEL_EXP_DATE"

ACTIVE_STATUS = 1
NOT_ACTIVE_STATUS = 0

STR_NOT_FOUND = -1

# MSP - MTLD
FIND_RS_DEVICES_FAILED = "FIND_RS_DEVICES_FAILED" # Recon Sentinel (RS)
FIND_ER_DEVICES_FAILED = "FIND_ER_DEVICES_FAILED" # Enterprise RS       - DEV_ERS
FIND_CE_DEVICES_FAILED = "FIND_CE_DEVICES_FAILED" # Cyberstack Endpoint - DEV_CEP
FIND_CD_DEVICES_FAILED = "FIND_CD_DEVICES_FAILED" # Cigent Device       - DEV_CDV
DEV_FND = 1    # device found
DEV_NTF = 0    # device NOT found
DEV_ERS = 1  
DEV_CEP = 2
DEV_CDV = 3

# VL1GL1
GRP_LVL_1 = 1
GRP_LVL_2 = 2
ACTIVE_LVL_1_USER_GROUP_DOES_NOT_EXIST = "ACTIVE_LVL_1_USER_GROUP_DOES_NOT_EXIST"


# MSP - Customer Level 
# Customer Class
GET_DEVICES_FAILED = "GET_DEVICES_FAILED"
ADMIN_HAS_NO_DEVICES = "ADMIN_HAS_NO_DEVICES"

# Device class
GET_ADC_STATUS_FAILED = "GET_ADC_STATUS_FAILED"
GET_LAST_CHECK_IN_FAILED = "GET_LAST_CHECK_IN_FAILED"
ALERT_GET_COUNT_FAILED = "ALERT_GET_COUNT_FAILED"
ADMIN_GROUP_NOT_ACTIVE = "ADMIN_GROUP_NOT_ACTIVE"
ADMIN_GROUP_CHECK_FAILED = "ADMIN_GROUP_CHECK_FAILED"


RECON = "RECON"
ENTRS = "ENTRS"
CYBEP = "CYBEP"
CIGDV = "CIGDV"

# MSP - Device Level

GET_COMMANDS_FAILED = "GET_COMMANDS_FAILED"
GET_OFFLINE_CONN_HOSTS_FAILED = "GET_OFFLINE_CONN_HOSTS_FAILED"
GET_ONLINE_CONN_HOSTS_FAILED = "GET_ONLINE_CONN_HOSTS_FAILED"
GET_BLOCKED_CONN_HOSTS_FAILED = "GET_BLOCKED_CONN_HOSTS_FAILED"
GET_UNBLCKD_CONN_HOSTS_FAILED = "GET_UNBLCKD_CONN_HOSTS_FAILED"
GET_UNKNOWN_CONN_HOSTS_FAILED = "GET_UNKNOWN_CONN_HOSTS_FAILED"
GET_TRUSTED_CONN_HOSTS_FAILED = "GET_TRUSTED_CONN_HOSTS_FAILED"

OFFLINE = "down"
ONLINE  = "up"

TRUSTED = 1
AUTHORIZED = 1

CHSTAT_OFFLI = 1
CHSTAT_ONLIN = 2
CHSTAT_UNBLC = 3
CHSTAT_BLCKD = 4
CHSTAT_UNKWN = 5
CHSTAT_TRSTD = 6


SEPRTR = "|" 
RECON = 1 
ENTRS = 2 
CYBEP = 3 
CIGDV = 4 
ALLDV = 5    #GGR

# Customer class - Table name lists
RECONTN = "groups%ssentinels%sadmin_group%srs_grp_list" % (SEPRTR, SEPRTR, SEPRTR)                 # Separator = "|"
ENTRSTN = "groups%senterprise_rs%sent_rs_admin_grp%sent_rs_grp_list" % (SEPRTR, SEPRTR, SEPRTR)
CYBEPTN = "groups%scyberstack_endpt%scyb_ep_admin_grp%scyb_ep_grp_list" % (SEPRTR, SEPRTR, SEPRTR)
CIGDVTN = "groups%scigent_devices%scig_dv_admin_grp%scig_dv_grp_list" % (SEPRTR, SEPRTR, SEPRTR)

# IAD
DEVICES_FAIL = "DEVICES_FAIL"

SUB_USERS_LOOKUP_FAIL = "SUB_USERS_LOOKUP_FAIL"

#SULI_IAD - errors
USERNAME_NOT_FOUND = "USERNAME_NOT_FOUND"
LVL2_USER_NOT_FOUND = "LVL2_USER_NOT_FOUND"
LVL2_WRONG_LEVEL_ID = "LVL2_WRONG_LEVEL_ID"

#Not defined! Found out during test of new update_user().
UNAUTHORIZED_USER_PASS = "UNAUTHORIZED_USER_PASS"

# Alert List of Dictionaries
GET_ALERT_LIST_DICT_FAILED = "GET_ALERT_LIST_DICT_FAILED"

# Group class
GROUP_OR_ADMINS_NOT_FOUND = "GROUP_OR_ADMINS_NOT_FOUND"
GROUP_INFO_FAIL = "GROUP_INFO_FAIL"

# User.getUserWithLevelInfo()
USER_WITH_GIVEN_LEVEL_ID_NOT_FOUND = "USER_WITH_GIVEN_LEVEL_ID_NOT_FOUND"
USER_WITH_GIVEN_LEVEL_ID_INFO_FAIL = "USER_WITH_GIVEN_LEVEL_ID_INFO_FAIL"
