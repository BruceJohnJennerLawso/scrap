## modelUniform.py #############################################################
## model for uniformly distributed data ########################################
################################################################################
from distModel import *

from scipy.optimize import curve_fit
from scipy import asarray as ar,exp,log,sqrt

class uniformModel(distributionModel):
	
	
	def __init__(self, data, mleValue, fitParameters=True, a=None, b=None):
		super(uniformModel, self).__init__(data)

		

		self.MLE = mleValue
		
		if(None in [a,b]):
			fitParameters = True
		
		if(fitParameters):
			self.b = max(self.getDataSet())
			self.a = min(self.getDataSet())
			
			def uniDist(x, a, b):
				return scipy.where((a<=x) & (x<=b), 1.0/float(b-a), 0.0)
			
			try:
				
				
				
				self.n, self.bins, patches = plt.hist(self.getDataSet(), self.getDatasetSize()/10, normed=1, facecolor='blue', alpha = 0.55)
				popt,pcov = curve_fit(uniDist,self.bins[:-1], self.n, p0=[self.a, self.b])
				##plt.plot(bins[:-1], gaus(bins[:-1],*popt),'c-',label="Gaussian Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2]), alpha=0.5)
				print "Fitted uniform distribution pdf curve to data with params a %f, b %f" % (popt[0], popt[1])
				self.a = popt[0]
				self.b = popt[1]
				##self.sigma = popt[2]
				
				self.fitted = True
			except RuntimeError:
				print "Unable to fit data to uniform distribution pdf curve"
				raise
			except Warning:
				raise RuntimeError
		else:
			self.a = a
			self.b = b		
				
				
	def getModelpdf(self, x):
		if((x >= self.a)and(x <= self.b)):
			return float(1.0/float(self.b-self.a))
		else:
			return 0.000
	
	def getDistributionScipyId(self):
		return 'uniform'	
		
	
	def getaValue(self):
		return self.a
		
	def getbValue(self):
		return self.b	

	def getIntervalWidth(self):
		return (self.b - self.a)
	
	def sampleFromDistribution(self):
		self.chosen()
		return np.random.uniform(self.a, self.b)	

	def getTestStatistic(self, test):
		if(test == "K-S"):
			return scipy.stats.kstest(np.asarray(self.getDataSet()), self.getDistributionScipyId(), args=(self.getaValue(),self.getIntervalWidth()))	

	def getSquareParamShift(self, new_a, new_b):
		return ((self.getaValue() - new_a)**2 + (self.getbValue() - new_b)**2)
		
	def distributionDescription(self):
		return "Uniform distribution model, a = %.3f, b = %.3f, p=%.7f" % (self.a, self.b, self.getpValue("K-S"))	
