#!/usr/bin/python
import sys
from datetime import datetime
from pytz import timezone
import pytz

if len(sys.argv) == 2:
	timestampString = sys.argv[1];
	#Etc/GMT have the reversed symbol, GMT-1 actually is GMT+1
	timezone = timezone("Etc/GMT-1");
elif len(sys.argv) == 3:
	timestampString = sys.argv[1];
	tzString = sys.argv[2];
	timeZoneString ="Etc/GMT";
	#Etc/GMT have the reversed symbol, GMT-1 actually is GMT+1
	if tzString[3]=="-":
		timeZoneString+="+";
	else:
		timeZoneString+="-";
	timeZoneString+= tzString[4:]
	# ************************************************************
	timezone = timezone(timeZoneString);
else:
	print("Wrong number of parameters");
	sys.exit(0);


l = len(timestampString);
	


if l==10:
	date = datetime.fromtimestamp(int(timestampString),timezone);
	print date.strftime('%Y-%m-%d %H:%M:%S %z');


elif l==13:
	date = datetime.fromtimestamp(int(timestampString)/1e3,timezone);
	print date.strftime('%Y-%m-%d %H:%M:%S %z');

elif l==8:
	date = datetime.fromtimestamp(int(timestampString)*60,timezone);
	print date.strftime('%Y-%m-%d %H:%M:%S %z');

elif l==6:
	date = datetime.fromtimestamp(int(timestampString)*3600,timezone);
	print date.strftime('%Y-%m-%d %H:%M:%S %z');	

else:
	print("Timestamp format not correctly detected");
	sys.exit(0);