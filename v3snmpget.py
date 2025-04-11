#!/usr/bin/python
# dantesan--sada--2024-10-24
# V3 snmpget() 

# for PDU
#snmpget -m PANDUIT-MIB -v 3 -l <sec_lvl> -a <auth> -A <auth_passwd> -x <priv_algorithm> -X <priv_key> -u <user_name> <IP_Address> <Oid>

import sys 
import os

# Only 1 FMPS: 10.137.101.20
#fmps_ip_addr = "10.137.101.20"
#mib_fn = "FMPS-MIB.mib"

#dantesan--sada--2024-12-02 - Add Sunrise PDU
# dantesan-sada-2024-12-05 - opps ... not -UPS-, but -PDU-!
#mibs = ["FMPS-MIB.mib", "PDU-MIB.mib", "UPS-MIB.mib", "PANDUIT-UPS-MIB.mib"]
mibs = ["FMPS-MIB.mib", "PDU-MIB.mib", "UPS-MIB.mib", "PANDUIT-PDU-MIB.mib"]
device_type = ["FMPS", "PDU", "UPS", "SUN"]
#dantesan--sada--2024-10-25 - Security Level Check
sec_level = ["NoAuthNoPriv", "AuthNoPriv", "AuthPriv"]
NA_NP = 0
A_NP = 1
A_P = 2

dev_pos = 0
ipa_pos = 1
oid_pos = 2
num_pos = 3
num_len = 1
mv_pos = 0   #number of positions to move USM and next args ...
usm_pos = 3 # 3 when num is not included!
secl_pos = 4
auth_pos = 5  
authp_pos = 6
priv_pos = 7
privp_pos = 8

if __name__ == "__main__":

    # dantesan--sada--2022-09-19 - check arguments.
    args = sys.argv[1:]
    largs = len(args)
    if largs == 0:
        fullpath = sys.argv[0].split("/")
        fn = fullpath[-1]
        usage_str = "   {0} <DEV_TYPE> <IP_ADDR> <OID> [num] <USM> <sec_level> ".format(fn)
        #dantesan--2024-11-20 - NoAuth? 
        #usage_str = usage_str + "<Auth> <Auth_passwd> [Priv_Algorithm] [Priv_Key]\n"
        usage_str = usage_str + "[Auth] [Auth_passwd] [Priv_Algorithm] [Priv_Key]\n"
        print("\nUsage: \n")
        print(usage_str)
        print("   DEV_TYPE = FMPS or PDU or UPS or SUN (Sunrise PDU)\n")
        print("Security Level <sec_level>= one of the ff:\n")
        print(*sec_level)
        print("\n")
        quit()

    dev_type = args[dev_pos]
    ip_addr = args[ipa_pos]
    oid = args[oid_pos]
    
    num = args[num_pos]      
    if len(num) == num_len: 
        # OID.num - num is specified can be 0, 1, 2,...,9! 
        # ...if > 1 digit, this program fails!                    
        mv_pos = 1       # move the args!
        usm_pos = usm_pos + mv_pos 
        secl_pos = usm_pos + mv_pos
        auth_pos = auth_pos + mv_pos   
        authp_pos = authp_pos + mv_pos
        priv_pos = priv_pos + mv_pos
        privp_pos = privp_pos + mv_pos
    else: #USM follows OID
        # dantesan--sada--DT2411202 - num is not always 0 ...
        #num = "0"
        num = None

    usm = args[usm_pos]
    secl = args[secl_pos]
    secl_idx = sec_level.index(secl)

    if secl_idx > NA_NP:
        auth = args[auth_pos]
        authp = args[authp_pos]
    else:
        auth = None

    if secl_idx == A_P:
        priv = args[priv_pos]
        privp = args[privp_pos]
    else:
        priv = None

    # for PDU
    #snmpget -m PANDUIT-MIB -v 3 -l <sec_lvl> -a <auth> -A <auth_passwd> -x <priv_algorithm> -X <priv_key> -u <user_name> <IP_Address> <Oid>  
    #print("\nOID = {0}, num = {1}".format(oid, num))
    mibs_pos = device_type.index(dev_type)
    #dantesan-sada--2024-12-05 - put full MIB path
    mib_fn = "/usr/share/mibs/netsnmp/{0}".format(mibs[mibs_pos])

    snmpget = "snmpget -m {0} -v 3 -l {1} ".format(mib_fn, secl)
    
    if auth is not None:
        snmpget = snmpget + "-a {0} -A {1} ".format(auth, authp)

    if priv is not None:
        snmpget = snmpget + "-x {0} -X {1} ".format(priv, privp)
     
    # dantesan--sada--DT2411202 - num is not always 0 ...
    #snmpget = snmpget + "-u {0} {1} {2}.{3}".format(usm, ip_addr, oid, num)
    snmpget = snmpget + "-u {0} {1} {2}".format(usm, ip_addr, oid)
    if num is not None:
        snmpget = snmpget + ".{0}".format(num)

    print("\n{0}\n".format(snmpget))
    #os.system(snmpget + " 2>/dev/null")
    os.system(snmpget)
    print("\n")


