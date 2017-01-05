## MJD.py ######################################################################
## handle date & time strings to get us a MJD value ############################
## or more accurately, just a JD value #########################################
################################################################################
from dateutil import parser

try:
	import jdcal
	def jdcalAvailable():
		return True
except ImportError:
	def jdcalAvailable():
		return False
	
def dayFrac(hour, minute):
	minutes = 60*hour + minute
	return float(minutes/1440.0)

def getMJDForDate(dateString, Hour=0, Minute=0):
	dt = parser.parse(dateString)
	dt = dt.replace(hour=Hour, minute=Minute)
	mjd = float(jdcal.gcal2jd(dt.year, dt.month, dt.day)[1])+ dayFrac(dt.hour, dt.minute)
	return mjd


if(__name__ == "__main__"):
	##"2011-01-08"
	
	date1 = "2011-01-08", 19, 0
	jd1 = getMJDForDate(*date1)
	
	date2 = ["2011-01-08", 22, 30]
	jd2 = getMJDForDate(*date2)
	print jd1, jd2
