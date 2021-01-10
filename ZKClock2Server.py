#!/usr/bin/env python3

#  pip install -U pyzk
#  pip install -U requests

from zk import ZK, const
from datetime import datetime

import sys
import time
import requests

host = sys.argv[len(sys.argv)-2]
url = sys.argv[len(sys.argv)-1]

#print host
#print url

conn = None

zk = ZK(host, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
try:
        timeToday = datetime.today()

        conn = zk.connect()
        conn.disable_device()
        serial = conn.get_serialnumber();
        timeOffset = time.mktime(conn.get_time().timetuple()) - time.mktime(timeToday.timetuple())        
        timeZoneOffset = -time.timezone        
        users = conn.get_users()
        records = conn.get_attendance()
        conn.set_time(timeToday)
        conn.enable_device()
        conn.disconnect()
        conn = None


#       print serial
#       print timeStamp

        device = {'id': serial, 'timeOffset': timeOffset, 'timeZoneOffset': timeZoneOffset}

#       print device

        x = requests.post(url, json = {'device': device})

#       print x.text


        for user in users:
                _user = {'id': str(user.uid), 'privilege': str(user.privilege), 'name': str(user.name), 'password': str(user.password), 'idCustom': str(user.user_id), 'idGroup': str(user.group_id)}
#                print _user
                x = requests.post(url, json = {'device': device, 'user': _user})
#                print x.text

        for record in records:
                _user = {'id': str(record.uid), 'idCustom': str(record.user_id)}
#                print _user
                _record = {'time': str(time.mktime(record.timestamp.timetuple())), 'status': str(record.status), 'punch': str(record.punch)}
#                print _record
                x = requests.post(url, json = {'device': device, 'user': _user, 'record': _record})
#                print x.text


        sys.exit(0)
except Exception as e:
        print ("Process terminate : {}".format(e))
        sys.exit(1)
finally:
        if conn:
                conn.disconnect()
