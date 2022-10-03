# 2022 - PANDUIT
#      - Automation Utilities File
#      - by dantesan-sada--2022-09-28

import os
from datetime import datetime
from datetime import timedelta
import shutil
from pathlib import Path


CONTINUE_MSG = "User is already logged in. Do you really want to continue?"

# LOCATORS

MONITORED_LCTR = "//h3/span[contains(text(), 'Monitored & Switched Per Outlet PDU')]"
USERNAME_ID_LCTR = "username"
PASSWORD_ID_LCTR = "password"
LOGIN_BTTN_LCTR = "//button[@type = 'submit']"

CONTINUE_MSG_LCTR = "//p/span[contains(text(), '{0}')]".format(CONTINUE_MSG)
CONTINUE_MSG_OK_LCTR = "//button/span[contains(text(), 'OK')]"

LOG_DIR = "{0}/log".format(Path.cwd())
LOG_FN = "pdu_automation_log.txt"
LOG_FULLPATH = "{0}/{1}".format(LOG_DIR, LOG_FN)
# LOCATORS

# #FROM_COMPLIANCE_PROJECT -VM114:$CYGD/C/TFC/analyze_color_CCfE.py 

# dantesan--2022-07-06 - so that other log files can be used ... logFn=None
def write_log(msg, logFn=None):
    if logFn is None:
        if(not os.path.exists(LOG_DIR)):
           os.mkdir(LOG_DIR, mode = 0o777)
        logFn = LOG_FULLPATH
        

    # dantesan--sada--2022-07-08 - check if log file exists!
    if os.path.exists(logFn):
        check_and_truncate_log_file(logFn)
    now = datetime.now()

    # dantesan-sada--2022-06-13 - save the run log. 
    if "SAVE_RUN_LOG" in msg:
        # dantesan--sada--2022-06-15 - first PROD run, failed!
        #dttm_str = now.strftime("%Y-%m-%d %H:%M") 
        save_run(datetime.now(), logFn)
        return

    if os.path.exists(logFn):
        log_out = open(logFn, 'at')
    else:
        log_out = open(logFn, 'wt')

    msgLn = "{}: {}\n".format(now, msg)
    if "START" in msg:
        msgLn = "\n\n" + msgLn    
    if "END" in msg:
        msgLn = msgLn + "\n\n" 
    

    log_out.writelines(msgLn)
    log_out.close()
    return


# dantesan-sada--2022-06-13 - save the run log - works if processing is done in < 1 minute!
# dantesan--sada--2022-06-15 - Did not last in PROD or did not run correctly at 1st time!
#                            - Runtime was divided between 1230 and 1231!
#                            - Get previous minute for now!
def save_run(dttm_now, logFn):
    dttm_str = dttm_now.strftime("%Y-%m-%d %H:%M")
    prev_min = dttm_now + timedelta(minutes=-1)
    prev_dttm_str = prev_min.strftime("%Y-%m-%d %H:%M")
    run_log_dttm = dttm_str.replace(' ', '_')
    run_log_fn = ("log/{}.txt".format(run_log_dttm))
    dttm_str_list = [prev_dttm_str,
                     dttm_str
                    ]

    for dttm_in_log in dttm_str_list:
        os.system("grep -n \"{0}\" {1} >> {2}".format(dttm_in_log, logFn, run_log_fn))

    write_log("{0} - Run log is saved in {1}.".format(save_run.__name__, run_log_fn))
    return


# dantesan--sada--2022-06-15 - debug function ... Cygwin debug has to be learned in VS Code.
def debug_func(msg, var):
    print("\n {0} : |{1}|\n".format(msg, var))
    return


def check_and_truncate_log_file(logFn):
    MAX_LINES = 5000
    MIN_LINES = 1000
    logTmp = "log/logtmp.txt"
    os.system("numlines=`wc -l < {0}`; if [ $numlines -gt {1} ]; then tail -{2} {0} > {3}; fi".format(logFn, MAX_LINES, MIN_LINES, logTmp))
    if os.path.exists(logTmp):
        if os.path.exists(logFn):
            os.remove(logFn)
        shutil.move(logTmp, logFn)
    return


# #FROM_COMPLIANCE_PROJECT -VM114:$CYGD/C/TFC/analyze_color_CCfE.py 
