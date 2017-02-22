## modelNormal.py ##############################################################
## model for normally distributed data #########################################
################################################################################
from distModel import *


from scipy.optimize import curve_fit
from scipy import asarray as ar,exp,log,sqrt


class normalModel(distributionModel):
	def __init__(self, data, mleValue, fitParameters=True, mean=None, sigma=None):
		super(normalModel, self).__init__(data)



		
		self.MLE = mleValue
		
		if(None in [mean, sigma]):
			fitParameters=True
		if(fitParameters):
			mean = Mean(self.getDataSet())		
			sigma = standardDeviation(self.getDataSet())
			try:
				
				def normDist(x, x0, sigma):
					output = 1.0/sqrt(2*np.pi*(sigma**2))
					output *= exp(-0.5*((x - x0)/sigma)**2)
					return output
				
				self.n, self.bins, patches = plt.hist(self.getDataSet(), self.getDatasetSize()/10, normed=1, facecolor='blue', alpha = 0.55)
				popt,pcov = curve_fit(normDist,self.bins[:-1], self.n, p0=[mean, sigma])
				##plt.plot(bins[:-1], gaus(bins[:-1],*popt),'c-',label="Gaussian Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2]), alpha=0.5)
				print "Fitted gaussian curve to data with params x0 %f, sigma %f" % (popt[0], popt[1])
				self.x0 = popt[0]
				self.sigma = popt[1]
				
				self.fitted = True
			except RuntimeError:
				print "Unable to fit data to normal curve, runtime error"
				raise
			except Warning:
				raise RuntimeError
		else:
			self.x0 = mean
			self.sigma = sigma

	def getDistributionScipyId(self):
		return 'norm'	


	def getModelpdf(self, x):
		output = 1.0/math.sqrt(2*np.pi*(self.getSigmaValue()**2))
		output *= math.exp(-0.5*((x - self.getx0Value())/self.getSigmaValue())**2)
		return output
		
	def getx0Value(self):
		return self.x0
		
	def getSigmaValue(self):
		return self.sigma
	
	def sampleFromDistribution(self):
		self.chosen()
		return np.random.normal(self.getx0Value(), self.getSigmaValue())
		

	def getTestStatistic(self, test):
		if(test == "K-S"):
			return scipy.stats.kstest(np.asarray(self.getDataSet()), self.getDistributionScipyId(), args=(self.getx0Value(),self.getSigmaValue()))			
	
	def getSquareParamShift(self, new_mu, new_sigma):
		return ((self.getx0Value() - new_mu)**2 + (self.getSigmaValue() - new_sigma)**2)
		

		
	def distributionDescription(self):		
		return "Normal model with Mean %.3f, Sigma %.3f, p=%.7f" % (self.getx0Value(), self.getSigmaValue(), self.getpValue("K-S"))
	
