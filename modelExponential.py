## modelExponential.py #########################################################
## model for data arising from an exponential distribution #####################
################################################################################
from distModel import *

from scipy.optimize import curve_fit
from scipy import asarray as ar,exp,log,sqrt
		
class exponentialModel(distributionModel):
	def __init__(self, data, mleValue, fitParameters=True, mean=None):
		super(exponentialModel, self).__init__(data)

		self.MLE = mleValue
		
		if(None in [mean]):
			fitParameters = True
			
		if(fitParameters):
			mean = Mean(self.getDataSet())		
			try:
					
				def expDist(x, x0):
					return (exp(-(x/x0))/x0)
				
				self.n, self.bins, patches = plt.hist(self.getDataSet(), self.getDatasetSize()/10, normed=1, facecolor='blue', alpha = 0.55)
				popt,pcov = curve_fit(expDist,self.bins[:-1], self.n, p0=[mean])
				##plt.plot(bins[:-1], gaus(bins[:-1],*popt),'c-',label="Gaussian Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2]), alpha=0.5)
				print "Fitted gaussian curve to data with params x0 %f" % (popt[0])
				self.x0 = popt[0]
				##self.sigma = popt[2]
				
				self.fitted = True
			except RuntimeError:
				print "Unable to fit data to exponential curve"
				raise
			except Warning:
				raise RuntimeError
		else:
			self.x0 = mean

	def getDistributionScipyId(self):
		return 'expon'	
	
	
	def getModelpdf(self, x):
		return (exp(-(x/self.x0))/self.x0)
		
	def getx0Value(self):
		return self.x0
		
	def getLambdaValue(self):
		return 1.0/float(self.getx0Value())
	
	def sampleFromDistribution(self):
		self.chosen()
		return np.random.exponential(self.getx0Value())
		
		
	def getTestStatistic(self, test):
		if(test == "K-S"):
			return scipy.stats.kstest(np.asarray(self.getDataSet()), self.getDistributionScipyId(), args=(0.0,self.getx0Value()))			
		
	def getSquareParamShift(self, new_mu):
		return (2.0*(self.getx0Value() - new_mu)**2)	
		## double up on this because theres only one parameter to shift in an
		## exponential, and we dont want the fitting loop to exit too early
		## while the exponential is still fitting
		
	def distributionDescription(self):		
		return "Exponential model with rate parameter %.3f, mean at %.3f, p=%.7f" % (self.getLambdaValue(), self.getx0Value(), self.getpValue("K-S"))
	
	
