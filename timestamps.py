#!/usr/bin/python
import sys
from datetime import datetime
from pytz import timezone
import pytz
from optparse import OptionParser
from dateutil import parser
import time
import simplejson as json

def parseTimestampString(timestampString,timezone,labels=[]):
	dateSt="";

	for d in range(len(timestampString)):

		l = len(timestampString[d]);
		if l==10:
			date = datetime.fromtimestamp(int(timestampString[d]),timezone);		
		elif l==13:
			date = datetime.fromtimestamp(int(timestampString[d])/1e3,timezone);
		elif l==8:
			date = datetime.fromtimestamp(int(timestampString[d])*60,timezone);
		elif l==6:
			date = datetime.fromtimestamp(int(timestampString[d])*3600,timezone);
		elif timestampString[d]=="0":
			date="";#ignore it but don't go to sys.exit
		else:
			print("Timestamp format not correctly detected "+d);
			sys.exit(0);
		if date:
			if not labels:
				dateSt += date.strftime('%Y-%m-%d %H:%M:%S %z')+"\t";		
			else:
				dateSt += labels[d]+" "+date.strftime('%Y-%m-%d %H:%M:%S %z')+"\t";

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
	nolive=False;
	novod=False;
	try:
		for timestampPair in jsonObj[""]["LIVE"]:
			timestampString+=str(timestampPair[0])+"-";
	except:
		nolive=True;
		#print "No LIVE values";
	
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
		novod=True;
		#print "No VOD values";
	if timestampString:
		timestampString = timestampString.split("-");
		print "************** VOD TS ***********************\n"
		print parseTimestampString(timestampString[0:-1],timezone)+"\n";
		print "************** VOD TS ***********************\n"

	#try json key-value format:
	timestampLabels="";
	if nolive==True and novod==True:
		for t in jsonObj.items():
			timestampString+=str(t[1])+"-";
			timestampLabels+=str(t[0])+"-";
		timestampString = timestampString.split("-");
		labels = timestampLabels.split("-");
		print parseTimestampString(timestampString[0:-1],timezone,labels[0:-1])+"\n";


	sys.exit(0);

else:
	if len(sys.argv) == 2:
		timestampString = sys.argv[1];
		timestampString = timestampString.split("-");
		
		#Etc/GMT have the reversed symbol, GMT-1 actually is GMT+1, but default is GMT+0
		timezone = timezone("Etc/GMT+0");
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



