#!/usr/bin/env python2

#  pip install -U pyzk

from zk import ZK, const
from datetime import datetime

import sys
import time

host = sys.argv[len(sys.argv)-2]
timeZoneOffSet = sys.argv[len(sys.argv)-1]

conn = None

zk = ZK(host, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
try:
        newtime = datetime.today() + timeZoneOffSet

        conn = zk.connect()

        conn.set_time(newtime)

        conn.enable_device()

        sys.exit(0)
except Exception as e:
        print ("Process terminate : {}".format(e))
        sys.exit(1)
finally:
        if conn:
                conn.disconnect()
