## graphtools.py ###############################################################
## graphing functions used by the analysis script(s) ###########################
################################################################################
import numpy as np

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


from scipy import stats

from scipy.optimize import curve_fit
from scipy import asarray as ar,exp

import math

import pylab
import distStats
from distStats import *

import pandas as pd
import seaborn as sns

import os


def plotScatterLabelled(data, x_param, y_param, huey, output_path, output_directory, output_filename):
	sns.lmplot(x_param, y_param, data, hue=huey, fit_reg=False);
	output_ = "%s/%s/%s" % (output_path, output_directory, output_filename)
	try:
		plt.savefig(output_)
	except IOError:
		os.makedirs('%s/%s/' % (output_path, output_directory))
		plt.savefig(output_)	
	plt.close()

def plotScatterMatrix(data, output_path, output_directory, output_filename):
	pd.tools.plotting.scatter_matrix(data, diagonal="kde")
	plt.tight_layout()
	
	output_ = "%s/%s/%s" % (output_path, output_directory, output_filename)
	try:
		plt.savefig(output_)
	except IOError:
		os.makedirs('%s/%s/' % (output_path, output_directory))
		plt.savefig(output_)		
	plt.close()
	
	
def seabornHeatmap(data, output_path, output_directory, output_filename):
	corrmat = data.corr()
	
	##ax = plt.subplots(figsize=(800,550))
	##ax = plt.subplots()
	ax = sns.heatmap(corrmat, vmax=1., square=False)
	ax.xaxis.tick_top()
	##ax.figure(figsize=(800,550))
	
	output_ = "%s/%s/%s" % (output_path, output_directory, output_filename)
	_output = "%s/%s/corrs.csv" % (output_path, output_directory)	
	
	try:

		corrmat.to_csv(_output)
	except IOError:
		print "Oh Well"
	
	plt.xticks(rotation=20)
	plt.yticks(rotation=20)		
	try:
		plt.savefig(output_)
	except IOError:
		os.makedirs('%s/%s/' % (output_path, output_directory))
		plt.savefig(output_)		
	plt.tight_layout()
	plt.close()


def snapToNearestTen(value):
	output = int(value)
	
	def farthestFromZero(thisValue, otherValue):
		diffThis = abs(thisValue)
		diffOther = abs(otherValue)
		if(diffThis >= diffOther):
			return True
		else:
			return False	
	
	
	
	if(output == 0):
		## if our max rounded down to zero, we'll take it up or down to
		## the nearest ten
		if(value < 0):
			output = -10.0
		else:
			output = 10.0
	elif( (output%10.0) != 0.0):
		## if the output wasnt gonna be zero, but it still wasnt a
		## multiple of 10, we need to adjust it
		nearest = float(int(output/10.0))*10
		if(value > 0):
			nearestPlus = float(int(output/10.0) + 1)*10
		else:
			nearestPlus = float(int(output/10.0) - 1)*10			
		##print nearest, '   ', nearestPlus, 'farthestFrom zero ', farthestFromZero(nearest, nearestPlus)
			
				
		if(farthestFromZero(nearest, nearestPlus)):
			
			output = nearest
		else:
			output = nearestPlus
	else:
		if(abs(output) < abs(value)):
			if(output < 0):
				output -= 10.0
			else:
				output += 10.0
	
	return output

##if(__name__ == "__main__"):
##	import random
##	
##	for i in range(0, 50):
##		val = random.random()*100.0
##		print "Value %f, rounded to nearest ten, %f" % (val, snapToNearestTen(val)), '\n'
##	for i in range(0, 50):
##		val = random.random()*-100.0
##		print "Value %f, rounded to nearest ten, %f" % (val, snapToNearestTen(val)), '\n'	
	
##	print "Value %f, rounded to nearest ten, %f" % (89.99, snapToNearestTen(89.99)), '\n'		
	
		

def generateHistogram(xlabel, ylabel, title, values, output_path, output_directory, output_filename, subplot_col, subplot_row, subplot_no, minShow='foo', maxShow='bar', binCount=39):
	
	nVal = len(values)
	
	plotMax = 60.0
	
	if(minShow == 'foo'):
		## if we dont get anything for a manual max min, just set our max and
		## min values for the graph range from the data
		minShow = float(int(min(values)))	
		maxShow = float(int(max(values)))			
	
	distMean = distStats.Mean(values)
	distMedian = distStats.Median(values)
	distVar = distStats.Variance(values)
	
	
	
	plt.subplot(subplot_col, subplot_row, subplot_no)

	plt.axvline(x=distMean, ymin=0.0, ymax = plotMax, linewidth=1, color='b', alpha=0.8)
	plt.axvline(x=distMedian, ymin=0.0, ymax = plotMax, linewidth=1, color='r', alpha=0.8)
	plt.axvline(x=distVar, ymin=0.0, ymax = plotMax, linewidth=1, color='g', alpha=0.8)		
	
	n, bins, patches = plt.hist(values, binCount, normed=1, facecolor='blue', alpha = 0.55)
	## bins are the endpoints of bins
	
	## n are the respective counts for those bins
	

	plotMax = snapToNearestTen(max(n))
	
	
	print output_filename
	##print "n ", n, 'len %i\n bins ' % len(n) ,  bins, 'len %i\npatches ' % len(bins) , patches
	
	
	def gaus(x,a,x0,sigma):
		return a*exp(-(x-x0)**2/(2*sigma**2))
	
	def expDist(x, a, x0, sigma):
		return a*(exp(-(x/x0))/x0)
	
	sigma = distStats.standardDeviation(values)
	
	##plt.plot(bins[:-1], n, 'r-')
	
	ableToFit = True
	
	paramsString = 'Unable to Fit Curve to Data'
	try:
		popt,pcov = curve_fit(gaus,bins[:-1], n, p0=[1,distMean,sigma])
		plt.plot(bins[:-1], gaus(bins[:-1],*popt),'c-',label="Gaussian Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2]), alpha=0.5)
		print "Fitted gaussian curve to data with params a %f, x0 %f, sigma %f" % (popt[0], popt[1], popt[2])
		paramsString = "Gaussian Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2])
	except RuntimeError:
		try:
			popt,pcov = curve_fit(expDist,bins[:-1],n,p0=[1,distMean,sigma])
			plt.plot(bins[:-1],expDist(bins[:-1],*popt),'c-',label="Fitted exponential curve to data with params a %f, x0 %f, sigma %f" % (popt[0], popt[1], popt[2]), alpha=0.5)		
			print "Fitted exponential curve to data"
			print "Fitted exponential curve to data with params a %f, x0 %f, sigma %f" % (popt[0], popt[1], popt[2])
			paramsString = "Exponential Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2])
		except RuntimeError:	
			print "Unable to fit curve"
			ableToFit = False
	if(ableToFit == False):
		plt.plot([], [], 'c-', label=paramsString)
	plt.legend()
	
	## histogram construction step
	## I forget, I think this was copy paste
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	## label our axes like good students
	title_ = "%s, n = %i\nMean (blue) %.3f, Median (red) %.3f, Variance (green) %.3f, Skewness %.3f, Kurtosis %.3f" % (title, nVal, distMean, distMedian, distVar, getSkewness(values), getAdjustedKurtosis(values))
	plt.title(title_)
	## an' title it
	print "Plot x min %f, x max %f, y min %f, y max %f" % (minShow, maxShow, 0.0, plotMax)
	
	if(minShow == maxShow):
		print "Histogram bounds identical, attempting to reset"
		minShow = float(int(min(values))-1)	
		maxShow = float(int(max(values))+1)		
		print "Plot x min %f, x max %f, y min %f, y max %f" % (minShow, maxShow, 0.0, plotMax)	

	plt.axis([minShow, maxShow, 0.0, abs(plotMax)])

	## 40 here was a working value for the range of possible bin values for this
	## dataset
	## I need to figure out how to get a max from our plt.hist output
	plt.grid(True)
	## make sure we got a grid on
	##plt.show()
	## showit

def plotHistogram(xlabel, ylabel, title, values, output_path, output_directory, output_filename, minShow='foo', maxShow='bar', binCount=39):
	## TLDR, takes a set of values and histograms them, whoop whop
	generateHistogram(xlabel, ylabel, title, values, output_path, output_directory, output_filename, 1, 1, 1, minShow, maxShow, binCount)
	output_ = "%s/%s/%s" % (output_path, output_directory, output_filename)
	try:
		plt.savefig(output_)
	except UserWarning:
		print "Duh"
	except IOError:
		os.makedirs('%s/%s/' % (output_path, output_directory))
		plt.savefig(output_)
	plt.close()
	
def trendline(x, gradient, intercept):
	output = gradient*x + intercept		
	return output
	
def getLinearModel(x_values, y_values, k=1.0, l=1.0):
	gradient, intercept, r_value, p_value, std_err = stats.linregress(x_values,y_values)	

	y_model = []
	
	grad = k*gradient
	interc = l*intercept
	
	for x in x_values:
		y = trendline(x, grad, interc)
		y_model.append(y)
	
	return y_model
	
def getLinearModel_rValue(x_values, y_values):
	gradient, intercept, r_value, p_value, std_err = stats.linregress(x_values,y_values)
	return r_value

def getLinearModel_pValue(x_values, y_values):
	gradient, intercept, r_value, p_value, std_err = stats.linregress(x_values,y_values)
	return p_value
		
def getLinearModelDeltas(x_values, y_values, k=1.0, l=1.0):
	if((k!=1.0)or(l!=1.0)):
		y_model = getLinearModel(x_values, y_values, k, l)		
	else:	
		y_model = getLinearModel(x_values, y_values)
	modelDeltas = []
	
	for i in range(0, len(x_values)):
		modelDelta = y_values[i] - y_model[i]
		modelDeltas.append(modelDelta)
	return modelDeltas




def getGraphBounds(values, snapToNearest=10):
	lower = min(values)
	upper = max(values)
	
	mid = (float(lower+ upper))/2.0
	
	def sign(value):
		return value/abs(value)
		## if its negative we get -1, if positive it outputs 1
		
		## I guess the type will be determined by the original value

	def snapAwayFrom(value, mid, snapToNearest=10):
		newValue = int(math.ceil(value /float(snapToNearest)))*snapToNearest
		if(abs(newValue - mid) < abs(value - mid)):
			## our value that we determined is actually closer to the
			## midpoint than the original one, presumably because the
			## negative lower bound ended up getting rounded upwards
			newValue -= snapToNearest
		
		if(abs(newValue-min(values)) <= 0.2*snapToNearest):
			## if we have a value within 20% of our tick away from the
			## edge of the boundary, thats a bit too close for comfort,
			## so we tick it one more away
			newValue += snapToNearest*sign(value-mid)
			## this is to compensate for values that fall exactly on the
			## edge, or ones that are a wee bit too close for comfort
		
		return newValue
			
	lower = snapAwayFrom(lower, mid, snapToNearest)
	upper = snapAwayFrom(upper, mid, snapToNearest)	
	return (lower, upper)

if(__name__ == "__main__"):
	testValues = [3.583, -7.99]
	lower, upper = getGraphBounds(testValues)
	print testValues
	print "[%.3f, %.3f]" % (lower, upper)
	
	
	
	
	
	
	
	def weibullDist(x, a, lam):
		output = (a/lam)
		output *= (x/lam)**(a-1.0)
		output *= exp((x/lam)**a)
		
		return output
	
	
	def expDist(x, a, x0, sigma):
		return a*(exp(-(x/x0))/x0)
	
	xPdf = [1.0, 3.0, 9.0, 10.0, 20.0, 30.0, 40.0, 60.0,120.0]
	yPdf = [0.05,0.04, 0.03,0.0285, 0.024, 0.0215, 0.02001, 0.0176, 0.015]
	
	
	
	a=1.1
	x0 = 0.0
	sigma = 1.0
	
	#lam = 0.1
	
	ableToFit = True
	try:
		popt,pcov = curve_fit(expDist,xPdf, yPdf, p0=[a,x0, sigma])
		##plt.plot(bins[:-1], gaus(bins[:-1],*popt),'c-',label="Gaussian Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2]), alpha=0.5)
		print "Fitted exponential curve to data with params, ", popt
	except RuntimeError:	
		print "Unable to fit curve"
		ableToFit = False
		
	print len(popt)
	
	##lam *= 0.5
	##lam = (1.0/5.1)
	
		
	plt.plot(xPdf, yPdf, 'rs')

	print "a %f, lambda %f" % (popt[0], popt[1])

	
	print popt, len(popt), type(popt), type(popt[0]), popt[0], popt[1]
	print xPdf
	print yPdf
	print [expDist(xVal, popt[0], popt[1], popt[2]) for xVal in xPdf]



	xSamples = np.arange(0.1, 120, 200)
	##print xSamples
	plt.plot(xSamples, [expDist(xVal, *popt) for xVal in xSamples], 'c')
	
	plt.xlabel('value')
	plt.ylabel('pdf')
	plt.title('About as simple as it gets, folks')
	plt.grid(True)
	plt.savefig("./results/weibull/weibullfit.png")
	plt.show()
	plt.close()
	
	
	
	
	
	
	
	
	
	
	
	bullshitValues = []
	
	
	aVal = 100
	sigmaVal = 4.0
	
	for i in range(0, 10000):
		bullshitValues.append(aVal*np.random.exponential(1.0/sigmaVal))
		##bullshitValues.append(popt[1]*np.random.weibull(popt[0]))	
	nparr = np.array(bullshitValues)
	print nparr.shape
	
	##for i in range(len(a)-1):
	##	bullshitValues = [val for sublist in bullshitValues for val in sublist]
	##	nparr = np.array(bullshitValues)
	##	print "Flattened values by 1 dimension, current array dimensions are now ",
	##	print nparr.shape	
	##print type(bullshitValues)
	##print bullshitValues
	
	
	
	
	
	
	
	
	
	
	
	
	plotHistogram('value', 'count', 'histogram of weibull distribution', bullshitValues, './results', 'weibull', 'bullshit.png')
	
def plotScatterplot(xlabel, ylabel, title, x_values, y_values, output_path, output_directory, output_filename, minShow='foo', maxShow='bar', binCount=39):
	## TLDR, takes a set of values and histograms them, whoop whop
	n=len(x_values)
	
	if(minShow == 'foo'):
		## if we dont get anything for a manual max min, just set our max and
		## min values for the graph range from the data
		##minShow = float(int(min(x_values)))	
		##maxShow = float(int(max(x_values))+1)	
		minShow, maxShow = getGraphBounds(x_values)
		
	minY, maxY = getGraphBounds(y_values, 5)	
	##minY = float(int(min(y_values)))*1.2
	##if(min(y_values) < 0):
	##	minY = float(int(min(y_values))-1)*1.2
	##maxY = float(int(max(y_values)))*1.2
	##if(max(y_values) < 1):
	##	maxY = float(int(max(y_values))+1)*1.2
	
		
	print "minShow %f, maxShow %f, Y min %f, Y max %f" % (minShow, maxShow, minY, maxY)			
	##print "x values ", x_values, "End of x values\n\n"
	##print "y values", y_values, "End of y values"
	modifiers =  [0.5, 1.0, 1.50]
	
	for k in modifiers:
		for l in modifiers:
			y_model = getLinearModel(x_values, y_values, k, l)
			plt.plot(x_values, y_model, 'm-', alpha=0.4)
			## for each possible k and l modifier combination, find what the
			## model looks like when adjusted by k and l			
	
	y_model = getLinearModel(x_values, y_values)
	## calculate the base model that linregress gives us as a best fit line 
	plt.plot(x_values, y_model, "g")
	## plot the base model without any modifiers
	plt.plot(x_values, y_values, 'bs')
	## plot the actual data points themselves
	r_value = getLinearModel_rValue(x_values, y_values)
	p_value = getLinearModel_pValue(x_values, y_values)	
	## grab the r and p values that are calculated
	r_square = r_value**2
	## calculate the r_squared value of the base fit line

	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	## label our axes like good students
	
	title = "%s, n=%i, r^2 = %f, p = %f (k*m)x + (l*b)" % (title, n, r_square, p_value)
	plt.title(title, size=10)
	## an' title it
	
	agciFix = False
	
	plt.axis([minShow, maxShow, minY, maxY])
	##try:
	##	plt.axis([minShow, maxShow, float(int(min(y_values)))*1.4, float(int(max(y_values))+1)*1.4])
	##except UserWarning:
	##	agciFix = True
	##if(agciFix == True):
	##	plt.axis([minShow, maxShow, minY, maxY])	
	## win percentages between 0.000 and 1.000, so we put our top limit a bit
	## higher, so we can see the 1.000 datapoints without them going off the
	## graph
	
	## I need to figure out how to get a max from our plt.hist output
	plt.grid(True)
	## make sure we got a grid on
	##plt.show()
	## showit
	output_ = "%s/%s/%s" % (output_path, output_directory, output_filename)
	try:
		plt.savefig(output_)
	except IOError:
		os.makedirs('%s/%s/' % (output_path, output_directory))
		plt.savefig(output_)
	plt.close()	

	for k in range(0, len(modifiers)):
		for l in range(0, len(modifiers)):
			modelDeltas = getLinearModelDeltas(x_values, y_values, modifiers[k], modifiers[l])
			histTitle = "k = %.2f, l = %.2f (k*m)x + (l*b)" % (modifiers[k], modifiers[l])
			histOutputFilename = "%s_deltaModelHistogram_k%f_l%f.png" % (output_filename, k, l)
			plotloc = l+1
			##print "k %i, l %i, %i" % (k, l, plotloc)
			generateHistogram("Delta from model", "Count", histTitle, modelDeltas, output_path, output_directory, histOutputFilename, len(modifiers), 1, plotloc , -2.0, 2.0, 40)
	
		left  = 0.125  # the left side of the subplots of the figure
		right = 0.9    # the right side of the subplots of the figure
		bottom = 0.1   # the bottom of the subplots of the figure
		top = 0.80      # the top of the subplots of the figure
		wspace = 0.2   # the amount of width reserved for blank space between subplots
		hspace = 0.25   # the amount of height reserved for white space between subplots

		plt.subplots_adjust(left, bottom, right, top, 4*wspace, 4*hspace)

		output_ = "%s/%s/modelDeltas_k_%f_%s" % (output_path, output_directory, modifiers[k], output_filename)
		
		try:
			plt.savefig(output_)
		except IOError:
			os.makedirs('%s/%s/' % (output_path, output_directory))
			plt.savefig(output_)
		
		plt.close()	

