#!/usr/bin/python
import sys
from datetime import datetime
from pytz import timezone
import pytz
from optparse import OptionParser
from dateutil import parser
import time
import simplejson as json

def parseTimestampString(timestampString,timezone):
	dateSt="";
	for d in timestampString:
		l = len(d);

		if l==10:
			date = datetime.fromtimestamp(int(d),timezone);
			dateSt += date.strftime('%Y-%m-%d %H:%M:%S %z')+"\t";		

		elif l==13:
			date = datetime.fromtimestamp(int(d)/1e3,timezone);
			dateSt += date.strftime('%Y-%m-%d %H:%M:%S %z')+"\t";

		elif l==8:
			date = datetime.fromtimestamp(int(d)*60,timezone);
			dateSt += date.strftime('%Y-%m-%d %H:%M:%S %z')+"\t";

		elif l==6:
			date = datetime.fromtimestamp(int(d)*3600,timezone);
			dateSt += date.strftime('%Y-%m-%d %H:%M:%S %z')+" \t";

		else:
			print("Timestamp format not correctly detected "+d);
			sys.exit(0);

	return dateSt;

op_parser = OptionParser()
op_parser.add_option("-c", "--calculate-date", dest="date",
                  help="Calculate the timestamp from the date specified");
op_parser.add_option("-j", "--json", dest="json",
                  help="Return the conversed dates from the specified json timestamps");

(options, args) = op_parser.parse_args()

if options.date:
	date = parser.parse(options.date)
	unix_time = int(time.mktime(date.timetuple()))
	print unix_time
	sys.exit(0);

if options.json:
	#Forced GMT+0
	timezone = timezone("GMT+0");
	jsonObj = json.loads(options.json);
	timestampString="";
	try:
		for timestampPair in jsonObj[""]["LIVE"]:
			timestampString+=str(timestampPair[0])+"-";
	except:
		print "No LIVE values";
	
	if timestampString:
		timestampString = timestampString.split("-");
		print "************** LIVE TS ***********************\n"
		print parseTimestampString(timestampString[0:-1],timezone)+"\n";
		print "************** LIVE TS ***********************\n"

	timestampString="";
	try:
		for timestampPair in jsonObj[""]["VOD"]:
			timestampString+=str(timestampPair[0])+"-";
	except:
		print "No VOD values";
	if timestampString:
		timestampString = timestampString.split("-");
		print "************** VOD TS ***********************\n"
		print parseTimestampString(timestampString[0:-1],timezone)+"\n";
		print "************** VOD TS ***********************\n"

	sys.exit(0);

else:
	if len(sys.argv) == 2:
		timestampString = sys.argv[1];
		timestampString = timestampString.split("-");
		
		#Etc/GMT have the reversed symbol, GMT-1 actually is GMT+1
		timezone = timezone("Etc/GMT-1");
	elif len(sys.argv) == 3:
		timestampString = sys.argv[1];
		timestampString = timestampString.split("-");
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

	print parseTimestampString(timestampString,timezone);



