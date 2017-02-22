## modelLogNormal.py ###########################################################
## model for log-normally distributed data #####################################
################################################################################
from distModel import *

from scipy.optimize import curve_fit
from scipy import asarray as ar,exp,log,sqrt

class logNormalModel(distributionModel):
	def __init__(self, data, mleValue, fitParameters=True, mean=None, sigma=None):
		super(logNormalModel, self).__init__(data)

		self.MLE = mleValue
		
		
		if(None in [mean, sigma]):
			
			fitParameters = True
		
		
		if(fitParameters):
					
			mean = Mean(self.getDataSet())		
			sigma = standardDeviation(self.getDataSet())
			
			try:
				
				def lognormDist(x, x0, sigma):
					return scipy.where((x<0), 0.0, (1.0/(  (x*sigma)*sqrt(2*np.pi) ))*exp(-0.5*((log(x)- x0)/sigma)**2))
					
				
				param_bounds=([0,-np.inf],[0.0,np.inf])
				self.n, self.bins, patches = plt.hist(self.getDataSet(), self.getDatasetSize()/10, normed=1, facecolor='blue', alpha = 0.55)
				##popt,pcov = curve_fit(lognormDist,self.bins[:-1], self.n, p0=[mean, sigma], bounds=param_bounds)
				##plt.plot(bins[:-1], gaus(bins[:-1],*popt),'c-',label="Gaussian Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2]), alpha=0.5)
				
				self.x0 = 0.0
				self.sigma = sigma
				
				
				##for i in range(10):
				self.x0, self.sigma = st.norm.fit(self.getDataSet(), loc = self.x0, scale =self.sigma)
				
				
				print "Fitted lognormal curve to data with params x0 %f, sigma %f" % (self.x0, self.sigma)
				##self.x0 = popt[0]
				##self.sigma = popt[1]
				
				self.fitted = True
			except RuntimeError:
				print "Unable to fit data to log-normal curve"
				raise
			except Warning:
				raise RuntimeError
		else:
			self.x0 = mean
			self.sigma = sigma
		
		
	def getDistributionScipyId(self):
		return 'lognorm'	


	def getModelpdf(self, x):
		if(x>=0):
			output = 1.0/(  (x*self.getSigmaValue())*sqrt(2*np.pi) )
			output *= exp(-0.5*((log(x)- self.getx0Value())/self.getSigmaValue())**2)
		else:
			output = x		
					
		return scipy.where((x<0), 0.0, output)
		
	def getx0Value(self):
		return self.x0
		
	def getSigmaValue(self):
		return self.sigma
	
	def sampleFromDistribution(self):
		self.chosen()
		return np.random.lognormal(self.getx0Value(), self.getSigmaValue())
	
	def getTestStatistic(self, test):
		if(test == "K-S"):
			##return scipy.stats.kstest(np.asarray(self.getDataSet()), self.getDistributionScipyId(), args=(self.getx0Value(),self.getSigmaValue()))			
			return scipy.stats.kstest(np.asarray(self.getDataSet()), 'lognorm', args=(self.getx0Value(),self.getSigmaValue()))				

	def getSquareParamShift(self, new_mu, new_sigma):
		return ((self.getx0Value() - new_mu)**2 + (self.getSigmaValue() - new_sigma)**2)
		
	def distributionDescription(self):		
		return "Log-Normal model with Mean %.3f, Sigma %.3f, p=%.7f" % (self.getx0Value(), self.getSigmaValue(), self.getpValue("K-S"))
	
