## distModel.py ################################################################
## object used to represent the statistical model assigned to a ################
## data set by curve fitting ###################################################
################################################################################
import matplotlib
if(__name__ != "__main__"):
	matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

from scipy.optimize import curve_fit
from scipy import asarray as ar,exp


import math
import scipy.stats
import numpy as np

from distStats import *



def gaus(x,a,x0,sigma):
	return a*exp(-(x-x0)**2/(2*sigma**2))

class distributionModel(object):
	def __init__(self, data):
		self.data = data
		self.fitted = False
		
		
	def getDataTypes(self):
		return [ty for ty in set([type(el) for el in self.data])]

	def getDataSet(self):
		return self.data
		
	def getDatasetSize(self):
		return len(self.data)
		
	def modelWasFitted(self):
		return self.fitted	


	def getBinProb(self, x, binwidth):
		## simple integral over [x,x+binwidth]
		left = x
		right = x+binwidth
		
		output = 0.0
		
		pdfVals = [self.getModelpdf(left), self.getModelpdf(right)]
		
		output += binwidth*min(pdfVals)
		output += 0.5*binwidth*(max(pdfVals) - min(pdfVals))		
		
		return output
		
class uniformModel(distributionModel):
	def __init__(self, data):
		super(uniformModel, self).__init__(data)

		mean = Mean(self.getDataSet())		
		sigma = standardDeviation(self.getDataSet())
		
		b = max(self.getDataSet())
		a = min(self.getDataSet())
		
		
		##def uniDist(x, a, b):
		##	if(type(x) == list):
		##		pass
		##	if((x >= a)and(x <= b)):
		##		return float(1.0/float(b-a))
		##	else:
		##		return 0.000
				
		def uniDist(x, a, b):
			return scipy.where((a<=x) & (x<=b), 1.0/float(b-a), 0.0)
		
		try:
			
			
			
			self.n, self.bins, patches = plt.hist(self.getDataSet(), self.getDatasetSize()/10, normed=1, facecolor='blue', alpha = 0.55)
			popt,pcov = curve_fit(uniDist,self.bins[:-1], self.n, p0=[a, b])
			##plt.plot(bins[:-1], gaus(bins[:-1],*popt),'c-',label="Gaussian Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2]), alpha=0.5)
			print "Fitted uniform distribution pdf curve to data with params a %f, b %f, sigma %f" % (popt[0], popt[1], sigma)
			self.a = popt[0]
			self.b = popt[1]
			##self.sigma = popt[2]
			
			self.fitted = True
		except RuntimeError:
			print "Unable to fit data to uniform distribution pdf curve"
			
	def getModelpdf(self, x):
		if((x >= self.a)and(x <= self.b)):
			return float(1.0/float(self.b-self.a))
		else:
			return 0.000
	
		
		
	
	def getaValue(self):
		return self.a
		
	def getbValue(self):
		return self.b	
		
	
	def sampleFromDistribution(self):
		return np.random.uniform(a, b)	
		
	def distributionDescription(self):
		return "Uniform distribution model, a = %.3f, b = %.3f" % (self.a, self.b)	
		
class exponentialModel(distributionModel):
	def __init__(self, data):
		super(exponentialModel, self).__init__(data)

		mean = Mean(self.getDataSet())		
		sigma = standardDeviation(self.getDataSet())
		
		try:
			
			def expDist(x, x0):
				return (exp(-(x/x0))/x0)
			
			self.n, self.bins, patches = plt.hist(self.getDataSet(), self.getDatasetSize()/10, normed=1, facecolor='blue', alpha = 0.55)
			popt,pcov = curve_fit(expDist,self.bins[:-1], self.n, p0=[mean])
			##plt.plot(bins[:-1], gaus(bins[:-1],*popt),'c-',label="Gaussian Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2]), alpha=0.5)
			print "Fitted gaussian curve to data with params x0 %f, sigma %f" % (popt[0], sigma)
			self.x0 = popt[0]
			##self.sigma = popt[2]
			
			self.fitted = True
		except RuntimeError:
			print "Unable to fit data to exponential curve"
			
	def getModelpdf(self, x):
		return (exp(-(x/self.x0))/self.x0)
		
	def getx0Value(self):
		return self.x0
		
	def getLambdaValue(self):
		return 1.0/float(self.getx0Value())
	
	def sampleFromDistribution(self):
		return np.random.exponential(self.getx0Value())
		
	def distributionDescription(self):		
		return "Exponential model with rate parameter %.3f, mean at %.3f" % (self.getLambdaValue(), self.getx0Value())
	
	
		
if(__name__ == "__main__"):
	import numpy as np
	import scipy.stats as st
	import random


	def expDist(x, a, x0):
		return a*(exp(-(x/x0))/x0)

	##print type(expDist([1.0,2.0,3.0], 1.0, 0.03))

	choices = [0,1]
	currentChoice = random.choice(choices)


	samples = 6400

	currentChoice = 0

	if(currentChoice == 0):
		
		generatedAValue = random.random()*5.0
		generatedBValue = generatedAValue + (1.0 + random.random()*5.0)
		print "generating uniform distribution, a=%f, b=%f" % (generatedAValue, generatedBValue)
		
		data = [np.random.uniform(generatedAValue, generatedBValue) for i in range(samples)]
	elif(currentChoice == 1):
		generatedExponentialMean = 0.01 + random.random()*0.4
		##generatedAValue = random.random()*2.0
		generatedAValue = 1.00
		print "generating exponential distribution, mean=%.3f, a=%.3f" % (generatedExponentialMean, generatedAValue)
		data = [generatedAValue*np.random.exponential(generatedExponentialMean) for i in range(samples)]		
		
	##data = [np.random.weibull(5.0) for i in range(4000)]
	print [min(data), max(data)]

	distributions = [st.laplace, st.norm, st.expon, st.dweibull, st.invweibull, st.lognorm, st.uniform]
	mles = []

	for distribution in distributions:
		pars = distribution.fit(data)
		mle = distribution.nnlf(pars, data)
		mles.append(mle)

	results = [(distribution.name, mle) for distribution, mle in zip(distributions, mles)]
	
	for dist in sorted(zip(distributions, mles), key=lambda d: d[1]):
		print dist
	best_fit = sorted(zip(distributions, mles), key=lambda d: d[1])[0]
	print 'Best fit reached using {}, MLE value: {}'.format(best_fit[0].name, best_fit[1])			

	
	if(best_fit[0].name == "uniform"):
		print "Best fit uniform, building model..."
		model = uniformModel(data)
	elif(best_fit[0].name == "expon"):
		print "Best fit exponential, building model..."
		model = exponentialModel(data)
	
	print model.distributionDescription()
	
	n, bins, patches = plt.hist(data, len(data)/10, normed=0, facecolor='blue', alpha=0.75)

	# add a 'best fit' line
	##l = plt.plot(bins, n)

	plt.xlabel('Value')
	plt.ylabel('Probability')
	plt.title('Histogram of dist values')
	bounds = sorted([Mean(data) + 1.2*(min(data) - Mean(data)), Mean(data) + 1.2*(max(data)  - Mean(data))])
	print "Absolute data bounds ", [min(data), max(data)]
	print "Adjusted data bounds ", bounds
	plt.axis([bounds[0], bounds[1], -0.1, max(n)*2.0])	
	plt.grid(True)

	def expDist(x, x0):
		return (exp(-(x/x0))/x0)

	def uniDist(x, a, b):
		return scipy.where((a<=x) & (x<=b), 1.0/float(b-a), 0.0)

	print model.getDatasetSize()
	
	binwidth = model.bins[:-1][1] - model.bins[:-1][0]	
	
	modelPrediction = [model.getDatasetSize()*model.getBinProb(binVal, binwidth) for binVal in bins[:-1]]
	
	plt.plot(model.bins[:-1], modelPrediction,'c-',label="Model Curve", alpha=0.75, linewidth=2)
	
	## hoping this is actually true
	
	
	fivePt = [(min(model.bins[:-1]) + k*(max(model.bins[:-1]) - min(model.bins[:-1]))) for k in [0.0,0.25,0.50,0.75, 1.0] ]
	print fivePt
	print [model.getModelpdf(x) for x in fivePt]
	if(currentChoice == 1):
		## an exponential distribution was detected
		generatedPrediction = [(0.5*binwidth*model.getDatasetSize()*(expDist(binVal, generatedExponentialMean) + expDist(binVal+binwidth, generatedExponentialMean))) for binVal in bins[:-1]]
		
		print "Exponential predicted min/max: ", [min(generatedPrediction), max(generatedPrediction), max(n for n in generatedPrediction if n!=max(generatedPrediction))]
		plt.plot(model.bins[:-1], [val for val in generatedPrediction],'m-',label="Target Curve", alpha=0.75, linewidth=2)
	elif(currentChoice == 0):
		generatedPrediction = [binwidth*model.getDatasetSize()*uniDist(binVal, generatedAValue, generatedBValue) for binVal in bins[:-1]]
		
		print "Uniform predicted min/max: ", [min(generatedPrediction), max(generatedPrediction)]
		plt.plot(model.bins[:-1], [val for val in generatedPrediction],'m-',label="Target Curve", alpha=0.75, linewidth=2)
	plt.legend()
	plt.show()
