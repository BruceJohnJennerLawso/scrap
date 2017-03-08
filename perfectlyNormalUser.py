## perfectlyNormalUser.py ######################################################
## nothing to see here human, just another completely human ####################
## visitor to the website of which you are running, you filthy meatbag #########
################################################################################
import scipy.stats as st

import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import math
import heapq


def interpolateFromPdfSamples(pdfSamples, x):
	
	xSamples = sorted([i[0] for i in pdfSamples])
	
	if((x<= max(xSamples))and(x >= min(xSamples))):
		if(x in xSamples):
			## we have an exact match, so we can just return the exact p
			## value that was sampled at this point
			for xySample in pdfSamples:
				if(xySample[0] == x):
					return xySample[1]
		else:
			## the x value we want to sample the probability of falls in
			## the range of x values that we have a p value for, so we
			## linearly interpolate between the two closest pairs of
			## values in x
			below = [xySample for xySample in pdfSamples if (xySample[0] < x)]
			above = [xySample for xySample in pdfSamples if (xySample[0] > x)]
			ptBelow = [xySample for xySample in below if (xySample[0] == max([pt[0] for pt in below]))]
			ptBelow =[item for sublist in ptBelow for item in sublist]
			ptAbove = [xySample for xySample in above if (xySample[0] == min([pt[0] for pt in above]))]	
			ptAbove =[item for sublist in ptAbove for item in sublist]
			
			m = (ptAbove[1]-ptBelow[1])/(ptAbove[0]-ptBelow[0])
			## calculate slope in this interval
			output = ptBelow[1] + m*(x- ptBelow[0])
			return output		
	else:
		## the x point in question is beyond the margins that we sampled
		## from the pdf, so we linearly interpolate based on the last
		## two endpoints
		if(x > max(xSamples)):
			secondBiggestX = min(heapq.nlargest(2, xSamples))

			largest = [xySample for xySample in pdfSamples if (xySample[0] > secondBiggestX)]
			largest = [item for sublist in largest for item in sublist]	
			secondLargest = [xySample for xySample in pdfSamples if (xySample[0] == secondBiggestX)]
			secondLargest = [item for sublist in secondLargest for item in sublist]	
			
			m = (largest[1]-secondLargest[1])/(largest[0]-secondLargest[0])
			## calculate slope in this interval
			output = largest[1] + m*(x- largest[0])	
		elif(x < min(xSamples)):
			secondSmallestX = max(heapq.nsmallest(2, xSamples))
			smallest = [xySample for xySample in pdfSamples if (xySample[0] < secondSmallestX)]
			smallest = [item for sublist in smallest for item in sublist]	
			secondSmallest = [xySample for xySample in pdfSamples if (xySample[0] == secondSmallestX)]
			secondSmallest = [item for sublist in secondSmallest for item in sublist]	
			m = (secondSmallest[1]-smallest[1])/(secondSmallest[0]-smallest[0])
			## calculate slope in this interval
			output = smallest[1] + m*(x- smallest[0])		
		return output				

def normalPdf(x):
	sigma = 0.9
	mean = 10.0
	output = np.exp(-0.5*((x - mean)/sigma)**2)
	output *= 1.0/np.sqrt(2*np.pi*(sigma**2))
	return output

def getWebPageWeibullPdfSample():
	return [[2,0.05],[3,0.04],[5,0.035],[7,0.03],[10,0.028],[15,0.025],[20,0.024],[30,0.021],[40,0.020],[50,0.019],[60,0.018]]


def sampleWebPageVisitLength():
	weibullPts = getWebPageWeibullPdfSample()
	
	class my_pdf(st.rv_continuous):
		def _pdf(self,x):
			##return normalPdf(x)  # Normalized over its range, in this case [0,1]
			return interpolateFromPdfSamples(weibullPts, x)
	my_cv = my_pdf(a=0, b=190.0, name='my_pdf')

	return my_cv.rvs()

if(__name__ == "__main__"):
	weibullPts = getWebPageWeibullPdfSample()
	samples = []
	print "generating samples.."
	for i in range(2000):
		sample = sampleWebPageVisitLength()
		print i, sample
		samples.append(sample)
	print "graphing data"
	hist, bins = np.histogram(samples, bins=20, normed = 1)
	print "finished binning data, plotting"
	width = 0.7 * (bins[1] - bins[0])
	center = (bins[:-1] + bins[1:]) / 2
	plt.bar(center, hist, align='center', width=width)
	
	
	xPts = [pt[0] for pt in weibullPts]
	plt.plot(xPts, [pt[1] for pt in weibullPts], 'cs')
	

	
	xSamplePoints = np.arange(min(xPts) - 20, max(xPts) + 20, len(xPts)*0.1)
	print len(xPts)
	print xSamplePoints
	interpolatedYPoints = [interpolateFromPdfSamples(weibullPts, xVal) for xVal in xSamplePoints]
	plt.plot(xSamplePoints, interpolatedYPoints , 'r-')
	plt.show()

