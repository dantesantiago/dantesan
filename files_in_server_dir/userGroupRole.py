
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


# dvcUser class ---------------------------------------------------------------------------
class dvcUser:
    
    ''' Device User class '''
    def __init__(self, _id = None, group_id = None, 
                       username = None, uuid = None):

        methodName = sys._getframe().f_code.co_name 

        self._id = _id
        self.group_id = group_id
        self.username = username
        self.uuid = uuid

    def getUserInfo(self, **kwargs):

        methodName = sys._getframe().f_code.co_name 
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn, dictionary = True) as cursor:
            try:
                sql = "SELECT id, group_id, username, uuid, stripe_cust_id " \
                      "  FROM users " 

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
                userInfo = cursor.fetchall()

                return(userInfo)

            except Exception as e:
                logger.debug(e) 
                self.response = make_response(constants.USER_INFO_FAIL,
                                                       methodName,
                                                       constants.BAD_REQUEST_400)


        
    def delDvcUser(self, **kwargs):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn, dictionary = True) as cursor:
            try:
                sql = "DELETE FROM users "

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



# dvcUser class ---------------------------------------------------------------------------


# Ugr class ---------------------------------------------------------------------------
class uGR:

    ''' UserGroupRole class '''

    def __init__(self, username = None, user_id = None, user_uuid = None, group_id = None, 
                       groupname = None, parent_id = None,
                       ugr_id = None, role_tag = None, ugr_uuid = None):

        methodName = sys._getframe().f_code.co_name 

        self.username  = username
        self.user_id   = user_id
        self.user_uuid = user_uuid
        self.group_id  = group_id
        self.groupname = groupname
        self.parent_id = parent_id
        self.ugr_id    = ugr_id
        self.role_tag  = role_tag
        self.ugr_uuid  = ugr_uuid

    def getUgrInfo(self):

        methodName = sys._getframe().f_code.co_name 
        #logger.debug("\n\n Inside %s" % methodName)  #CTO
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn) as cursor:
            #logger.debug("AFT get_db_connection()")  #CTO
            try:
                sql = "SELECT UGR.id, UGR.group_id, UGR.role_tag, " \
                      "       UGR.uuid, G.name, G.parent_id, U.id, U.uuid " \
                      "  FROM groups G, user_group_roles UGR, users U" \
                      " WHERE UGR.user_id = U.id " \
                      "   AND G.id = UGR.group_id " \
                      "   AND U.username = \"%s\" " \
                   " ORDER BY UGR.id " % (self.username)
                cursor.execute(sql)
                rows = cursor.fetchall()
                ugrInfo = []
                for row in rows:
                    self.user_id   = row[6]
                    self.user_uuid = row[7]
                    self.group_id  = row[1]
                    self.groupname = row[4]
                    self.parent_id = row[5]
                    self.ugr_id    = row[0]
                    self.role_tag  = row[2]
                    self.ugr_uuid  = row[3]

                    ugrTmp = {}
                    ugrTmp = {
                                 "user_id"    : self.user_id,
                                 "user_uuid"  : self.user_uuid,
                                 "username"   : self.username,
                                 "group_id"   : self.group_id,
                                 "groupname"  : self.groupname,
                                 "parent_id"  : self.parent_id,
                                 "ugr_id"     : self.ugr_id,
                                 "role_tag"   : self.role_tag,
                                 "ugr_uuid"   : self.ugr_uuid
                             }
                    ugrInfo.append(ugrTmp)

                return(ugrInfo)

            except Exception as e:
                logger.debug(e) 


        

# Ugr class ---------------------------------------------------------------------------


# dvcGroup class ---------------------------------------------------------------------------
class dvcGroup:

    ''' Device Group class '''

    def __init__(self, group_id = None, group_name = None, 
                       parent_id = None, group_uuid = None, grplvl = None):

        self.dvc_grp_dict = {
                                 "id"        : group_id,
                                 "name"      : group_name,
                                 "parent_id" : parent_id,
                                 "uuid"      : group_uuid,
                                 "grplvl"    : grplvl
                            }

    def getGroupInfo(self, **kwargs):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn, dictionary = True) as cursor:
            try:
                sql = "  SELECT id, name, parent_id, uuid, grplvl " \
                      "    FROM groups " 

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
                groups_data = cursor.fetchall() #cursor.fetchone()
                return groups_data

            except Exception as e:
                logger.debug(e) 

    def getUsersInGroup(self):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn, dictionary = True) as cursor:
            try:
                sql = ("    SELECT U.id, U.fname, U.group_id, U.lname, U.username, U.uuid  " 
                       "      FROM users U  " 
                       "INNER JOIN groups G  " 
                       "     WHERE G.id = {grp_id} " 
                       "       AND G.id = U.group_id " 
                       "  ORDER BY U.id").format(grp_id = self.dvc_grp_dict["id"])
                cursor.execute(sql)
                user_dict_list = cursor.fetchall()
                return user_dict_list

            except Exception as e:
                logger.debug(e) 

    def getAssetsInGroup(self):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn, dictionary = True) as cursor:
            try:
                sql = ("    SELECT S.id, S.deviceid, S.name, S.group_id, S.uuid  " 
                       "      FROM sentinels S  " 
                       "INNER JOIN groups    G  " 
                       "     WHERE G.id = {grp_id} " 
                       "       AND G.id = S.group_id " 
                       "  ORDER BY S.id").format(grp_id = self.dvc_grp_dict["id"])
                cursor.execute(sql)
                asset_dict_list = cursor.fetchall()
                return asset_dict_list

            except Exception as e:
                logger.debug(e) 


    def delDvcGroup(self, **kwargs):
        with get_db_connection(database=common.mdb) as devconn, get_db_cursor(devconn, dictionary = True) as cursor:
            try:
                sql = "DELETE FROM groups "

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

# dvcGroup class ---------------------------------------------------------------------------
