    
@app.route('/sentinels/<deviceid>/alerts', methods=['GET'])
@tokenauth.verify_token
def get_alerts(deviceid, alert_type=None):
    username = get_user_from_authheader()
    if username.status != constants.OK_200:
        return username

    user = extract_username(username)
    userid = get_user_id(user)
    if userid.status != constants.OK_200:
        return userid
    
    user_id = json.loads(userid.get_data())
    check_devid_auth = check_sentinel_authority(deviceid, user_id)
    if check_devid_auth.status != constants.OK_200:
        return check_devid_auth

    alerts = []
    with get_db_connection(database=deviceid) as devconn, get_db_cursor(devconn) as cursor:
        try:
            if alert_type == None:
                alert_type = ""

            sql = "SELECT id, deviceid, alert_time, hostname, message, " \
                  "severity, ip, alert_type, notified, ack, mac FROM alerts " \
                  "WHERE deviceid = \"%s\"" \
                  "AND ack = 0 " \
                  "%s " \
                  "ORDER BY alert_time DESC" % (deviceid, alert_type)
            cursor.execute(sql)
            rows = cursor.fetchall()
            if not rows:
                return jsonify([])
                
            for row in rows:
                sent_dict = {
                    'id' : row[0],
                    'deviceid'  :  row[1],
                    'mac' : row[10],
                    'alert_time'  :  row[2],
                    'hostname'  :  row[3],
                    'message'  :  row[4],
                    'severity'  : row[5],
                    'ip'  :  row[6],
                    'alert_type'  :  row[7],
                    'notified'  : row[8],
                    'acknowledged'  :  row[9]
                }
                alerts.append(sent_dict)
            return jsonify(alerts)
        except Exception as e:
            return make_response(constants.ALERTS_FAIL, 
                                 "get_alerts", 
                                 constants.BAD_REQUEST_400)
            
@app.route('/sentinels/<deviceid>/alerts/attack', methods=['GET'])
@tokenauth.verify_token
def get_attack_alerts(deviceid):
    alert_type = "AND alert_type = 'attack'"
    return get_alerts(deviceid, alert_type)
            
@app.route('/sentinels/<deviceid>/alerts/scan', methods=['GET'])
@tokenauth.verify_token
def get_scan_alerts(deviceid):
    alert_type = "AND alert_type = 'scan'"
    return get_alerts(deviceid, alert_type)
            
