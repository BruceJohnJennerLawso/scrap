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
from scipy import asarray as ar,exp,log,sqrt


import math
import scipy.stats
import numpy as np

from distStats import *



import scipy.stats as st
import random

np.seterr(all='warn')


def gaus(x,a,x0,sigma):
	return a*exp(-(x-x0)**2/(2*sigma**2))

class distributionModel(object):
	def __init__(self, data):
		self.data = data
		self.fitted = False
		self.sampledCount = 0
		
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
		
	def getExpectedBinCount(self, x, binwidth, customSampleSize=False):
		## simple integral over [x,x+binwidth]
		left = x
		right = x+binwidth
		
		output = 0.0
		
		pdfVals = [self.getModelpdf(left), self.getModelpdf(right)]
		
		output += binwidth*min(pdfVals)
		output += 0.5*binwidth*(max(pdfVals) - min(pdfVals))		
		if(customSampleSize == False):
			output *= self.getDatasetSize()
		else:
			output *= customSampleSize	
		return output		


	def getpValue(self, test):
		if(test == "K-S"):
			if(self.getDistributionScipyId() == 'lognorm'):
				return scipy.stats.kstest(np.asarray(self.getDataSet()), self.getDistributionScipyId(), args=(self.getSigmaValue(),))[1]		
			else:
				return scipy.stats.kstest(np.asarray(self.getDataSet()), self.getDistributionScipyId())[1]

	def chosen(self):
		self.sampledCount += 1
		
	def getSampleProportion(self,sampleSize):
		return float(self.sampledCount/float(sampleSize))


##class multiModalModel(distributionModel):
##	def __init__(self, data, distributionPairs):
		
		
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
		
	
	def sampleFromDistribution(self):
		self.chosen()
		return np.random.uniform(self.a, self.b)	

		
		
	def distributionDescription(self):
		return "Uniform distribution model, a = %.3f, b = %.3f, p=%.7f" % (self.a, self.b, self.getpValue("K-S"))	
		
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
		
		
	def distributionDescription(self):		
		return "Exponential model with rate parameter %.3f, mean at %.3f, p=%.7f" % (self.getLambdaValue(), self.getx0Value(), self.getpValue("K-S"))
	
	



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
		
		
	def distributionDescription(self):		
		return "Normal model with Mean %.3f, Sigma %.3f, p=%.7f" % (self.getx0Value(), self.getSigmaValue(), self.getpValue("K-S"))
	
	


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
					
					output = 1.0/(  (x*sigma)*sqrt(2*np.pi) )
					output *= exp(-0.5*((log(x)- x0)/sigma)**2)
					
					
					return scipy.where((x<0), 0.0, output)
					
				
				param_bounds=([0,-np.inf],[np.inf,np.inf])
				self.n, self.bins, patches = plt.hist(self.getDataSet(), self.getDatasetSize()/10, normed=1, facecolor='blue', alpha = 0.55)
				popt,pcov = curve_fit(lognormDist,self.bins[:-1], self.n, p0=[mean, sigma], bounds=param_bounds)
				##plt.plot(bins[:-1], gaus(bins[:-1],*popt),'c-',label="Gaussian Curve with params\na=%f\nx0=%f\nsigma=%f" % (popt[0], popt[1], popt[2]), alpha=0.5)
				print "Fitted lognormal curve to data with params x0 %f, sigma %f" % (popt[0], popt[1])
				self.x0 = popt[0]
				self.sigma = popt[1]
				
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
					
					
		return scipy.where((x<0), 0.0, output)
		
	def getx0Value(self):
		return self.x0
		
	def getSigmaValue(self):
		return self.sigma
	
	def sampleFromDistribution(self):
		self.chosen()
		return np.random.lognormal(self.getx0Value(), self.getSigmaValue())
		
	def distributionDescription(self):		
		return "Log-Normal model with Mean %.3f, Sigma %.3f, p=%.7f" % (self.getx0Value(), self.getSigmaValue(), self.getpValue("K-S"))
	






















def getAvailableDistributionsByScipyIds():
	return ["uniform", "normal", "lognorm", "expon"]

def getDistributionByScipyId(distId, data):
	if(distId == "uniform"):
		return uniformModel(data)
	elif(distId == "normal"):
		return normalModel(data)
	elif(distId == "lognorm"):
		return logNormalModel(data)	
	elif(distId == "expon"):
		return exponentialModel(data)




class dataModelSet(object):
	def __init__(self, data, mleDiffCutoff=1.0):
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

		self.modelSets = []

		self.modelOptions = [mod[0].name for mod in sorted(zip(distributions, mles), key=lambda d: d[1])]
		## list of scipy distribution ids sorted by their MLEs given the data
		## [0] is best, [1], next best and so on
		
		
		for model in sorted(zip(distributions, mles), key=lambda d: d[1]):
			if(model[0].name in getAvailableDistributionsByScipyIds()):
				try:
					modelDist = getDistributionByScipyId(model[0].name, data)
					self.modelSets.append([modelDist, model[1]])
					## append the distribution object and the MLE value for this
					## particular distribution & the data
					
					## ah frig, I think in the bimodal case, it will be
					## something like 
				except RuntimeError:
					pass	
			else:
				## nothing that can be done here, if we dont have a object of
				## the distribution needed available, we cant do much about it
				pass
				
	def getNthBestModelSet(self, n):
		if(n > (len(self.modelSets)-1) ):	
			## lists make this easy to handle
			## even in this out of range case
			return []
		else:
			return self.modelSets[n-1]
			## this should be list type
			
	def getBestModelSet(self):
		return self.getNthBestModelSet(1)
		## 1st best being best or whatever
				
		
		
	

def generateRandomDistribution(currentChoice):
	if(currentChoice == 0):
		
		generatedAValue = random.random()*5.0
		generatedBValue = generatedAValue + (1.0 + random.random()*5.0)
		print "generating uniform distribution, a=%f, b=%f" % (generatedAValue, generatedBValue)
		
		##data = [np.random.uniform(generatedAValue, generatedBValue) for i in range(samples)]
		model = uniformModel([], 0.0, False, generatedAValue, generatedBValue)
		
		return model
	elif(currentChoice == 1):
		generatedExponentialMean = 0.01 + random.random()*0.4
		##generatedAValue = random.random()*2.0
		print "generating exponential distribution, mean=%.3f, rate=%.3f" % (generatedExponentialMean, 1.0/generatedExponentialMean)
		
		model = exponentialModel([], 0.0, False, generatedExponentialMean)
		##data = [np.random.exponential(generatedExponentialMean) for i in range(samples)]		
		return model
	elif(currentChoice == 2):	
		generatedMean = -1.5 + random.random()*3.0
		generatedSigma = 0.1 + random.random()*1.9
		print "generating normal distribution with mean=%.3f, sigma %.3f" % (generatedMean, generatedSigma)
		##data = [np.random.normal(generatedMean, generatedSigma) for i in range(samples)]
		model = normalModel([], 0.0, False, generatedMean, generatedSigma)
		
		return model
	elif(currentChoice == 3):	
		generatedMean = 0.0 + random.random()*3.0
		generatedSigma = 0.1 + random.random()*1.9
		print "generating lognormal distribution with mean=%.3f, sigma %.3f" % (generatedMean, generatedSigma)
		##data = [np.random.lognormal(generatedMean, generatedSigma) for i in range(samples)]		
		
		model = logNormalModel([], 0.0, False, generatedMean, generatedSigma)
		
		return model
	elif(currentChoice == 4):
		## bimodal
		choices = [0,1,2,3]
		firstChoice = random.choice(choices)
		secondChoice = random.choice(choices)
		return [generateRandomDistribution(firstChoice), generateRandomDistribution(secondChoice)]

	elif(currentChoice == 5):
		## getting really interesting now
		choices = [0,1,2,3]
		
		multipleDists = []
		for i in range(0, 3+int(2*random.random())):
			thisChoice = random.choice(choices)
			multipleDists.append(generateRandomDistribution(thisChoice))
		return multipleDists	

	elif(currentChoice == 6):
		## bimodal
		choices = [2]
		firstChoice = random.choice(choices)
		secondChoice = random.choice(choices)
		return [generateRandomDistribution(firstChoice), generateRandomDistribution(secondChoice)]

	elif(currentChoice == 7):	
		generatedMean = 0.0
		generatedSigma = 1.0
		print "generating lognormal distribution with mean=%.3f, sigma %.3f" % (generatedMean, generatedSigma)
		##data = [np.random.lognormal(generatedMean, generatedSigma) for i in range(samples)]		
		
		model = logNormalModel([], 0.0, False, generatedMean, generatedSigma)
		
		return model





if(__name__ == "__main__"):


	choices = [0,1,2,3,4]
	currentChoice = random.choice(choices)


	samples = 4000

	currentChoice = 5


	initialModel = generateRandomDistribution(currentChoice)


	multimodal = False
	if(type(initialModel) == list):
		multimodal = True
		
	if(multimodal):
		data = []		
		for i in range(samples):
			chosenModel = random.choice(initialModel)
			##print chosenModel.sampledCount
			data.append(chosenModel.sampleFromDistribution())
			
	else:	
		data = [initialModel.sampleFromDistribution() for i in range(samples)]
	
	print [min(data), max(data)]

	
	##distributions = [st.laplace, st.norm, st.expon, st.dweibull, st.invweibull, st.lognorm, st.uniform]

	distributions = [st.norm, st.expon, st.lognorm, st.uniform]
	
	distributionPairs = [[modelA.name, modelB.name] for modelA in distributions for modelB in distributions]
	##print distributionPairs
	##exit()
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

	
	print [mod[0].name for mod in sorted(zip(distributions, mles), key=lambda d: d[1])]
	##exit()
	
	ableToFit = True
	
	if(best_fit[0].name == "uniform"):
		print "Best fit uniform, building model..."
		model = uniformModel(data, best_fit[1])
	elif(best_fit[0].name == "expon"):
		print "Best fit exponential, building model..."
		model = exponentialModel(data, best_fit[1])
	elif(best_fit[0].name == "norm"):
		print "Best fit normal, building model..."
		model = normalModel(data, best_fit[1])		
	elif(best_fit[0].name == "lognorm"):
		print "Best fit lognormal, building model..."
		model = logNormalModel(data, best_fit[1])				
	else:
		print "Fitted unknown model '%s'" % (best_fit[0].name)
		ableToFit = False
		##exit()
	
	if(ableToFit):
		print model.distributionDescription()
	
	n, bins, patches = plt.hist(data, len(data)/10, normed=0, facecolor='blue', alpha=0.75)

	# add a 'best fit' line
	##l = plt.plot(bins, n)

	plt.xlabel('Value')
	plt.ylabel('Probability')
	
	
	if(ableToFit):
		descString = model.distributionDescription()
	else:
		descString = "Unable to fit model to data"
	plt.title('Histogram of dist values,\n%s' % (descString))
	bounds = sorted([Mean(data) + 1.2*(min(data) - Mean(data)), Mean(data) + 1.2*(max(data)  - Mean(data))])
	print "Absolute data bounds ", [min(data), max(data)]
	print "Adjusted data bounds ", bounds
	plt.axis([bounds[0], bounds[1], -0.1, max(n)*2.0])	
	plt.grid(True)



	if(ableToFit):
		print model.getDatasetSize()
	
		binwidth = model.bins[:-1][1] - model.bins[:-1][0]	
		
		trueBins = [(binstart+(0.5*binwidth)) for binstart in model.bins[:-1]]
		
		modelPrediction = [model.getExpectedBinCount(binVal, binwidth) for binVal in bins[:-1]]
	
		r = lambda: random.randint(0,255)
		hexCo = '#%02X%02X%02X' % (r(),r(),r())
	
		plt.plot(trueBins, modelPrediction,'o-',label="Model Curve", alpha=0.75, linewidth=2, color='%s' % hexCo, markersize=2)
	
		## hoping this is actually true
	
	
		fivePt = [(min(model.bins[:-1]) + k*(max(model.bins[:-1]) - min(model.bins[:-1]))) for k in [0.0,0.25,0.50,0.75, 1.0] ]
		print fivePt
		print [model.getModelpdf(x) for x in fivePt]



		if(not multimodal):
			## an exponential distribution was detected			
			plt.plot(trueBins, [initialModel.getExpectedBinCount(xval, binwidth, samples) for xval in model.bins[:-1]],'ro-',label="Target Curve", alpha=0.75, linewidth=2, markersize=2)
		else:
			for mod in initialModel:
				plt.plot(trueBins, [mod.getExpectedBinCount(xval, binwidth, samples*mod.getSampleProportion(samples)) for xval in model.bins[:-1]],'ro-',label="Target Curve %i (%s), sample bias %.3f" % ((initialModel.index(mod) +1), mod.getDistributionScipyId(), (mod.sampledCount/float(samples))), alpha=0.60 + 0.2*float(1.0/len(initialModel)), linewidth=2, markersize=2)			
			
			plt.plot(trueBins, [samples*sum([mod.getBinProb(xval, binwidth)*mod.getSampleProportion(samples) for mod in initialModel]) for xval in model.bins[:-1]],'co-',label="Target Curve Net pdf", alpha=0.75, linewidth=2, markersize=2)					
	print scipy.stats.kstest(np.asarray(model.getDataSet()), 'norm')

	plt.legend(loc=2,prop={'size':10})
	plt.show()
