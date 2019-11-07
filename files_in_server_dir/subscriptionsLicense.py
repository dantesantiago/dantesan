
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

# Subscriptions Class ---------------------------------------------------------
class Subscriptions:
    ''' Subscriptions class '''

    @classmethod
    def deleteSubscriptions(cls, **kwargs):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn) as cursor:
            try:
                sql = "DELETE FROM subscriptions"
                if len(kwargs) != 0:
                    where = "WHERE"
                    for key, value in kwargs.items():
                        if type(value) == int:
                            condition = (" {field} = {_data} ").format(field = key, _data = value)
                        else:
                            condition = (" {field} = \"{_data}\" ").format(field = key, _data = value)
                        if where == "WHERE":
                            where += (" {cond} ").format(cond = condition)
                        else:
                            where += (" AND {cond} ").format(cond = condition)
                    sql += " "
                    sql += where 

                cursor.execute(sql)
                devconn.commit()

            except Exception as e:
                logger.debug(e)

    

    def __init__(self, _id = None, user_id = None, plan_id = None, 
                       subscription_id = None, group_id = None,
                       status = None, _type = None, count = None,
                       used = None, tier = None, recurring = None):

        self.subscriptions_dict = {
                                      "id"              : _id,
                                      "user_id"         : user_id,
                                      "plan_id"         : plan_id,
                                      "subscription_id" : subscription_id,
                                      "group_id"        : group_id,
                                      "sub_timestamp"   : None,
                                      "exp_timestamp"   : None,
                                      "status"          : status,
                                      "type"            : _type,
                                      "count"           : count,
                                      "used"            : used,
                                      "tier"            : tier,
                                      "recurring"       : recurring
                                  }


    def getSubscriptions(self, **kwargs):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn, dictionary = True) as cursor:
            try:
                sql = "  SELECT id, user_id, plan_id, subscription_id, " \
                      "         group_id, sub_timestamp, exp_timestamp, " \
                      "         status, type, count, used, tier, recurring " \
                      "    FROM subscriptions " 

                if len(kwargs) != 0:
                    where = "WHERE"
                    for key, value in kwargs.items():
                        if type(value) == int:
                            condition = (" {field} = {_data} ").format(field = key, _data = value)
                        else:
                            condition = (" {field} = \"{_data}\" ").format(field = key, _data = value)
                        if where == "WHERE":
                            where += (" {cond} ").format(cond = condition)
                        else:
                            where += (" AND {cond} ").format(cond = condition)
                    sql += " "
                    sql += where 

                cursor.execute(sql)
                subscriptions_data = cursor.fetchall()
                return subscriptions_data

            except Exception as e:
                logger.debug(e)

# Subscriptions Class ---------------------------------------------------------

# Licenses Class --------------------------------------------------------------

class Licenses:

    ''' Licenses class '''

    def __init__(self, _id = None, uuid = None, group_id = None,
                       token = None, system_serial = None, 
                       manufacturer = None, model = None, computer_name = None):

        self.licenses_dict = {
                                 "id"            : _id,
                                 "uuid"          : uuid,
                                 "group_id"      : group_id,
                                 "token"         : token,
                                 "system_serial" : system_serial,
                                 "manufacturer"  : manufacturer,
                                 "model"         : model,
                                 "computer_name" : computer_name
                             }

    @classmethod
    def deleteLicenses(cls):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn) as cursor:
            try:
                sql = "DELETE FROM licenses"
                cursor.execute(sql)
                devconn.commit()

            except Exception as e:
                logger.debug(e)

    def delLicense(self, **kwargs):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn) as cursor:
            try:
                sql = "DELETE FROM licenses"

                if len(kwargs) != 0:
                    where = "WHERE"
                    for key, value in kwargs.items():
                        if type(value) == int:
                            condition = (" {field} = {_data} ").format(field = key, _data = value)
                        else:
                            condition = (" {field} = \"{_data}\" ").format(field = key, _data = value)
                        if where == "WHERE":
                            where += (" {cond} ").format(cond = condition)
                        else:
                            where += (" AND {cond} ").format(cond = condition)
                    sql += " "
                    sql += where 

                cursor.execute(sql)
                devconn.commit()

            except Exception as e:
                logger.debug(e)

    

    def getLicenses(self, **kwargs):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn, dictionary = True) as cursor:
            try:
                sql = "  SELECT id, uuid, group_id, token, " \
                      "         system_serial, manufacturer, model, computer_name " \
                      "    FROM licenses "

                if len(kwargs) != 0:
                    where = "WHERE"
                    for key, value in kwargs.items():
                        if type(value) == int:
                            condition = (" {field} = {_data} ").format(field = key, _data = value)
                        else:
                            condition = (" {field} = \"{_data}\" ").format(field = key, _data = value)
                        if where == "WHERE":
                            where += (" {cond} ").format(cond = condition)
                        else:
                            where += (" AND {cond} ").format(cond = condition)
                    sql += " "
                    sql += where 

                sql += "ORDER BY id "

                cursor.execute(sql)
                licenses_data = cursor.fetchall()
                return licenses_data

            except Exception as e:
                logger.debug(e)

# Licenses Class --------------------------------------------------------------

# ActivationToken Class --------------------------------------------------------------

class ActivationToken:

    ''' ActivationToken class '''

    def __init__(self, _id = None, signature = None, 
                       expiration_timestamp = None, activated = None):

        self. activation_token_dict = {
                                          "id"                  : _id,
                                          "signature"           : signature,
                                          "expiration_timestamp": expiration_timestamp,
                                          "activated"           : activated,
                                      }

    @classmethod
    def deleteActivationTokens(cls):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn) as cursor:
            try:
                sql = "DELETE FROM activation_tokens"
                cursor.execute(sql)
                devconn.commit()

            except Exception as e:
                logger.debug(e)

    def deleteActivationTokens(self, **kwargs):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn) as cursor:
            try:
                sql = "DELETE FROM activation_tokens"
                if len(kwargs) != 0:
                    where = "WHERE"
                    for key, value in kwargs.items():
                        if type(value) == int:
                            condition = (" {field} = {_data} ").format(field = key, _data = value)
                        else:
                            condition = (" {field} = \"{_data}\" ").format(field = key, _data = value)
                        if where == "WHERE":
                            where += (" {cond} ").format(cond = condition)
                        else:
                            where += (" AND {cond} ").format(cond = condition)
                    sql += " "
                    sql += where 

                cursor.execute(sql)
                devconn.commit()

            except Exception as e:
                logger.debug(e)

    


    def getActivationToken(self, **kwargs):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn, dictionary = True) as cursor:
            try:
                sql = "  SELECT * " \
                      "    FROM activation_tokens "

                if len(kwargs) != 0:
                    where = "WHERE"
                    for key, value in kwargs.items():
                        if type(value) == int:
                            condition = (" {field} = {_data} ").format(field = key, _data = value)
                        else:
                            condition = (" {field} = \"{_data}\" ").format(field = key, _data = value)
                        if where == "WHERE":
                            where += (" {cond} ").format(cond = condition)
                        else:
                            where += (" AND {cond} ").format(cond = condition)
                    sql += " "
                    sql += where 

                cursor.execute(sql)
                actvtn_tkn = cursor.fetchall()
                return actvtn_tkn

            except Exception as e:
                logger.debug(e)

# ActivationToken Class --------------------------------------------------------------

# OthTable Class --------------------------------------------------------------

class OthTable:

    ''' OthTable class '''

    def __init__(self,  tableName):

        self.tableName = tableName

    def deleteTableData(self):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn) as cursor:
            try:
                sql = "DELETE FROM %s " % (self.tableName)
                cursor.execute(sql)
                devconn.commit()

            except Exception as e:
                logger.debug(e)

    def deleteData(self, **kwargs):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn) as cursor:
            try:
                sql = "DELETE FROM %s" % (self.tableName)
                if len(kwargs) != 0:
                    where = "WHERE"
                    for key, value in kwargs.items():
                        if type(value) == int:
                            condition = (" {field} = {_data} ").format(field = key, _data = value)
                        else:
                            condition = (" {field} = \"{_data}\" ").format(field = key, _data = value)
                        if where == "WHERE":
                            where += (" {cond} ").format(cond = condition)
                        else:
                            where += (" AND {cond} ").format(cond = condition)
                    sql += " "
                    sql += where 

                cursor.execute(sql)
                devconn.commit()

            except Exception as e:
                logger.debug(e)

    


    def getTableData(self, **kwargs):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn, dictionary = True) as cursor:
            try:
                col_sql = "SELECT COLUMN_NAME FROM information_schema.columns " \
                          " WHERE table_schema = \"%s\" AND " \
                          "       table_name = \"%s\" " % (common.mdb, self.tableName)
                cursor.execute(col_sql)
                field_names = cursor.fetchall()
                # field_names is a list of dicts with keys 'COLUMN_NAME' and field names as values.
                # convert to field names list
                field_names_list = []
                for field_dict in field_names:
                        field_names_list.append(list(field_dict.values()))
                          
                sql = "  SELECT * " \
                      "    FROM %s" % (self.tableName)

                if len(kwargs) != 0:
                    where = "WHERE"
                    stmt_line = ""
                    for key, value in kwargs.items():
                        for list_item in field_names_list:
                            if key in list_item:
                                if type(value) == int:
                                    condition = (" {field} = {_data} ").format(field = key, _data = value)
                                else:
                                    condition = (" {field} = \"{_data}\" ").format(field = key, _data = value)
                                if where == "WHERE":
                                    where += (" {cond} ").format(cond = condition)
                                else:
                                    where += (" AND {cond} ").format(cond = condition)
                        if key == "statement": # statements after WHERE should follow correct SQL style
                            stmt_line += " " 
                            stmt_line += value
                    sql += " "
                    if where != "WHERE":
                        sql += where 
                    sql += stmt_line

                cursor.execute(sql)
                tbl_dat = cursor.fetchall()
                return tbl_dat

            except Exception as e:
                logger.debug(e)

# OthTable Class --------------------------------------------------------------
