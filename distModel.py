## distModel.py ################################################################
## object used to represent the statistical model assigned to a ################
## data set by curve fitting ###################################################
################################################################################
import matplotlib
##matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


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
		
		
class uniformModel(distributionModel):
	def __init__(self, data):
		super(uniformModel, self).init(data)

		mean = Mean(self.getDataSet())		
		sigma = standardDeviation(self.getDataSet())
		
		try:
			self.n, self.bins, patches = plt.hist(self.getDataSet(), self.getDatasetSize()/10, normed=1, facecolor='blue', alpha = 0.55)
			popt,pcov = curve_fit(gaus,self.bins[:-1], self.n, p0=[1,mean])
			##plt.plot(bins[:-1], gaus(bins[:-1],*popt),'c-',label="Gaussian Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2]), alpha=0.5)
			print "Fitted gaussian curve to data with params a %f, x0 %f, sigma %f" % (popt[0], popt[1], sigma)
			self.a = popt[0]
			self.x0 = popt[1]
			##self.sigma = popt[2]
			
			self.fitted = True
		except RuntimeError:
			print "Unable to fit data to exponential curve"
			
	def getModelpdf(self, x):
		return self.a*(exp(-(x/self.x0))/self.x0)
		
	def getx0Value(self):
		return self.x0
	
	def getaValue(self):
		return self.a
		
	def getLambdaValue(self):
		return 1.0/float(self.getx0Value())
	
	def sampleFromDistribution(self):
		return np.random.exponential(self.getx0Value())		
		
		
class exponentialModel(distributionModel):
	def __init__(self, data):
		super(exponentialModel, self).init(data)

		mean = Mean(self.getDataSet())		
		sigma = standardDeviation(self.getDataSet())
		
		try:
			
			def expDist(x, a, x0, sigma):
				return a*(exp(-(x/x0))/x0)
			
			self.n, self.bins, patches = plt.hist(self.getDataSet(), self.getDatasetSize()/10, normed=1, facecolor='blue', alpha = 0.55)
			popt,pcov = curve_fit(expDist,self.bins[:-1], self.n, p0=[1,mean])
			##plt.plot(bins[:-1], gaus(bins[:-1],*popt),'c-',label="Gaussian Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2]), alpha=0.5)
			print "Fitted gaussian curve to data with params a %f, x0 %f, sigma %f" % (popt[0], popt[1], sigma)
			self.a = popt[0]
			self.x0 = popt[1]
			##self.sigma = popt[2]
			
			self.fitted = True
		except RuntimeError:
			print "Unable to fit data to exponential curve"
			
	def getModelpdf(self, x):
		return self.a*(exp(-(x/self.x0))/self.x0)
		
	def getx0Value(self):
		return self.x0
	
	def getaValue(self):
		return self.a
		
	def getLambdaValue(self):
		return 1.0/float(self.getx0Value())
	
	def sampleFromDistribution(self):
		return np.random.exponential(self.getx0Value())
		
		
		
		
if(__name__ == "__main__"):
	import numpy as np
	import scipy.stats as st

	

	##data = [np.random.weibull(5.0) for i in range(10000)]

	##data = [np.random.uniform(5.0, 10.0) for i in range(1000)]

	data = [np.random.exponential(0.03) for i in range(1000)]

	print type(data)
	distributions = [st.laplace, st.norm, st.exponweib, st.dweibull, st.invweibull, st.lognorm]
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


	n, bins, patches = plt.hist(data, len(data)/10, normed=1, facecolor='blue', alpha=0.75)

	# add a 'best fit' line
	##l = plt.plot(bins, n)

	plt.xlabel('Value')
	plt.ylabel('Probability')
	plt.title('Histogram of dist values')
	bounds = sorted([Mean(data) + 1.2*(min(data) - Mean(data)), Mean(data) + 1.2*(max(data)  - Mean(data))])
	print "Absolute data bounds ", [min(data), max(data)]
	print "Adjusted data bounds ", bounds
	plt.axis([bounds[0], bounds[1], 0, max(n)*2.0])	
	plt.grid(True)

	plt.show()
