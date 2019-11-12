import re
import sys
import pytz             # $ pip install pytz
import tzlocal          # $ pip install tzlocal
import subprocess
from datetime import datetime

result = subprocess.check_output([sys.executable, "speedtest.py", "--csv", "--no-upload"])
# result = '11643,Hart Telephone Co,"Hartwell, GA",2019-10-04T18:43:18.942285Z,76.19543202040536,49.86,51735109.37702047,38481317.19396705,,170.34.104.9'
# multiplier = 5.2
# multiplier = 6.7
multiplier = 8.6
mylist = re.split(',', result)
host = mylist[1]
ping = round(float(mylist[6]), 1)
downspeed = round((float(mylist[7]) * multiplier) / (1000 * 1000), 1)
downspeed2 = int(round(downspeed, 0))
stamp = mylist[4]
udate = stamp[0:10]
utime = stamp[11:19]
unow = str(udate) + " " + str(utime)
local_timezone = tzlocal.get_localzone() # https://stackoverflow.com/questions/4770297/convert-utc-datetime-string-to-local-datetime
utc_time = datetime.strptime(unow, "%Y-%m-%d %H:%M:%S")
l_time = str(utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone))
nowdate = l_time[0:10]
nowtime = l_time[11:19]
csv = str(nowdate) + "," + str(nowtime) + "," + str(host) + "," + str(ping) + "," + str(downspeed) + "\n"
f=open("results.csv","a+")
f.write(csv)
f.close
print downspeed2
