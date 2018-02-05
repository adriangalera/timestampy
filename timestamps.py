#!/usr/bin/python
import argparse
import datetime
import pytz
from pytz import timezone
import dateutil.parser
import calendar


parser = argparse.ArgumentParser("Script to perform date conversion")
parser.add_argument("value", help='Value to compute')
parser.add_argument("timezone", help='Timezone to use in the computation')
parser.add_argument("-c", "--calculate",
                    help="Calculate timestamp from date", action='store_true')
args = parser.parse_args()
timestamp_val = args.value
timezone_val = args.timezone
calculate = args.calculate

tz_obj = timezone(timezone_val)

if calculate:
    tz_date = tz_obj.localize(dateutil.parser.parse(timestamp_val))
    print calendar.timegm(tz_date.utctimetuple())


else:
    fmt = '%Y-%m-%d %H:%M:%S'

    # get timestamp from value an convert it to date, the timestamps might be comma separated
    values = timestamp_val.split(",")
    output = []
    for value in values:
        gmt_dt = datetime.datetime.utcfromtimestamp(long(value))
        gmt_dt = pytz.utc.localize(gmt_dt)
        output.append(gmt_dt.astimezone(tz_obj).strftime(fmt))

    print ", ".join(output)
