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



if(__name__ == "__main__"):
	##"2011-01-08"
	
	dateString1 = ["2011-01-08", 19, 0]
	dt1 = parser.parse(dateString1[0])
	dt1 = dt1.replace(hour=dateString1[1], minute=dateString1[2])
	
	dateString2 = ["2011-01-08", 22, 30]
	dt2 = parser.parse(dateString2[0])
	dt2 = dt2.replace(hour=dateString2[1], minute=dateString2[2])	
	
	
	
	jd1 = float(jdcal.gcal2jd(dt1.year, dt1.month, dt1.day)[1])+ dayFrac(dt1.hour, dt1.minute)
	jd2 = float(jdcal.gcal2jd(dt2.year, dt2.month, dt2.day)[1])+ dayFrac(dt2.hour, dt2.minute)	
	print jd1, jd2
