#!/usr/bin/python
# dantesan--sada--2024-10-23 - python version
# V1/V2 snmpget() 


import sys 
import os

# Only 1 FMPS: 10.137.101.20
#fmps_ip_addr = "10.137.101.20"
#mib_fn = "FMPS-MIB.mib"

 #dantesan--sada--2024-12-02 - Add Sunrise PDU
#mibs = ["FMPS-MIB.mib", "PDU-MIB.mib", "UPS-MIB.mib"]
# dantesan-sada-2024-12-05 - opps ... not -UPS-, but -PDU-!
#mibs = ["FMPS-MIB.mib", "PDU-MIB.mib", "UPS-MIB.mib", "PANDUIT-UPS-MIB.mib"]
mibs = ["FMPS-MIB.mib", "PDU-MIB.mib", "UPS-MIB.mib", "PANDUIT-PDU-MIB.mib"]
#device_type = ["FMPS", "PDU", "UPS"]
device_type = ["FMPS", "PDU", "UPS", "SUN"]

dev_pos = 0
ipa_pos = 1
oid_pos = 2
num_pos = 3
#dantesan--sada--DT2411202 - num is not always 0 ...
#def_num = "0"
def_num = None

if __name__ == "__main__":


    # dantesan--sada--2022-09-19 - check arguments.
    args = sys.argv[1:]
    largs = len(args)
    if largs == 0:
        fullpath = sys.argv[0].split("/")
        fn = fullpath[-1]
        print("\nUsage: \n")
        print("   {0} <DEV_TYPE> <IP_ADDR> <OID> [num]\n".format(fn))
        print("   DEV_TYPE = FMPS or PDU or UPS or SUN (Sunrise PDU)\n")
        quit()

    dev_type = args[dev_pos]
    ip_addr = args[ipa_pos]
    oid = args[oid_pos]
    if largs == num_pos + 1:
       num = args[num_pos]
    else:
       num = def_num 

    #print("\nOID = {0}, num = {1}".format(oid, num))
    mibs_pos = device_type.index(dev_type)
    #dantesan-sada--2024-12-05 - put full MIB path
    mib_fn = "/usr/share/mibs/netsnmp/{0}".format(mibs[mibs_pos])
    #mib_fn = mibs[mibs_pos]

    snmpget = "snmpget -m {0} -v 2c -c public ".format(mib_fn)

    # dantesan--sada--DT2411202 - num is not always 0 ...
    snmpget = snmpget + "{0} {1}".format(ip_addr, oid)
    if num is not None:
        snmpget = snmpget + ".{0}".format(num)

    print("\n{0}\n".format(snmpget))
    os.system(snmpget + " 2>/dev/null")
    #os.system(snmpget)
    print("\n")


