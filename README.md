timestampy
==========

Python code to work with timestamps, currently works with timestamps

The way to use it is:
```
timestamps.py timestamp timezone
```
, for instance:
```
timestamps.py 23038544 GMT+2
```

or to calculate timestamp from date:
```
timestamps.py -c "date string" timezone
```

This program makes use of python pytz and python dateutils, which may not be installed in your system, in order to install it:
```
pip install pytz
pip install python-dateutil
```
