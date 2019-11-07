
"""
common.py -
The purpose of this module is to provide shared common methods etc.
"""

import sys
import os
import inspect

import json

from flask import jsonify

import env
from passlib.hash import bcrypt

from logger_module import get_logger

logger = get_logger(__file__)

PROJECT_ROOT = '%s/..' % os.path.dirname(__file__)
SEND_EMAIL = env.SEND_EMAIL
ADMINS = ['david.glass@cigent.com']
mdbhost = env.mdbhost
mailserver = env.mailserver
webaccess = env.webaccess

mailuser = "no-reply@reconsentinel.com"
mailpass = "Tp8zbEyy8ALWFHo957Q5A"

mdbuser = "rsadmin"
mdbpass = "uUCZ5DNi4tpf5Rxgi42Wk"
mdb = "rsusersdb"
mdbport = "3306"


def create_response(message=None, status=None):
    if message is None:
        message = ''
    caller_frame = inspect.stack()[1]
    context = caller_frame[3]
    logger.debug("<%s> [%s] ..." % (context, status))
    r = jsonify(message)
    if status:
        r.status = status
    logger.debug("<%s> [%s] %s" % (context, r.status, r.data))
    return r


def make_response(message, func, status):
    # note: func is obsolete but remains due the the large number of references that call 3 arguments
    r = create_response(message, status)
    return r


def nonone(d):
    """nonone dictionary - returns a dictionary with all None value elements removed"""
    nonone_dict = {}
    for k in d:
        v = d[k]
        if v is not None:
            nonone_dict[k] = v
    return nonone_dict


def is_python3():
    return sys.version_info[0] == 3


def encrypt(password):
    return bcrypt.using(ident="2y").hash(password)


class BadDataException(Exception):
    pass


class StripeException(Exception):
    pass
