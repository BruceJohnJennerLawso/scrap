## modelMultimodal.py ##########################################################
## overaarching object type that multimodal distributions are defined under ####
################################################################################
from modelNormal import *
from modelExponential import *
from modelUniform import *
from modelLogNormal import *

import random

def getAvailableDistributionsByScipyIds():
	return ["uniform", "normal", "lognorm", "expon"]

def getDistributionByScipyId(distId, data, mle):
	if(distId == "uniform"):
		return uniformModel(data, mle)
	elif((distId == "normal")or(distId == "norm")):
		return normalModel(data, mle)
	elif(distId == "lognorm"):
		return logNormalModel(data, mle)	
	elif(distId == "expon"):
		return exponentialModel(data, mle)
	else:
		print "Unable to identify '%s' distribution provided, returning none, gonna crash" % distId



def getScipyFitById(distId, data):
	if(distId == "uniform"):
		return st.uniform.fit(data)
	elif((distId == "normal")or(distId == "norm")):
		return st.norm.fit(data)
	elif(distId == "lognorm"):
		return st.lognorm.fit(data)	
	elif(distId == "expon"):
		return st.expon.fit(data)
	else:
		print "Unable to identify '%s' distribution provided, returning none, gonna crash" % distId


class multiModalModel(distributionModel):
	def __init__(self, data, distributionTypes):
		super(multiModalModel, self).__init__(data)
		
		## distribution types here are the ids of the distributions to be fitted
		## ie ['expon', 'norm', 'norm']
		self.subDistributions = []
		subDistributions = []

		bounds = sorted([Mean(data) + 1.2*(min(data) - Mean(data)), Mean(data) + 1.2*(max(data)  - Mean(data))])

		mu1 = min(bounds)
		sigma1 = (1/3.0)*(max(bounds)-min(bounds))

		mu2 = max(bounds)
		sigma2 = sqrt(sigma1)
		
		mu1 = min(bounds) + (max(bounds)-min(bounds))/2.0
		mu2 = min(bounds) + (max(bounds)-min(bounds))/2.0			
		
		normCount = 0
		exponCount = 0
		for distType in distributionTypes:
			if(distType == 'norm'):
				
				
				if((normCount%2) == 0):
					## even case starts from the low mean, high sigma case
					subDistributions.append(normalModel([], 0.0, False, mu1, sigma1))
				elif((normCount%3) == 0):
					subDistributions.append(normalModel([], 0.0, False, mu1, sigma2))
				elif((normCount%4) == 0):
					subDistributions.append(normalModel([], 0.0, False, mu2, sigma1))										
				else:
					subDistributions.append(normalModel([], 0.0, False, mu2, sigma2))		
				## basically what is happenning here, is we are trying to lay out the 
				## initial conditions for the normal models in a way that makes
				## the initial distributions different enough from one another
				## (and from what they will look like in the end) that they will
				## be forced to move aggressively towards a truer fit with each
				## round of fitting. This is becase initially placing a bimodal
				## case at identical sigmas and slightly different means was
				## occasionally getting stuck producing not very accurate fits		
				normCount += 1	
			elif(distType == 'expon'):
				exponCount += 1
				subDistributions.append(exponentialModel([], 0.0, False, mu2*exponCount))	
				## I have not yet tested this at all, so as usual, Im going to
				## try placing an exponential in the 'wrongest' position I can
				## imagine, hoping that it will migrate aggressively towards
				## the correct shape
			elif(distType == 'uniform'):
				subDistributions.append(uniformModel([], 0.0, False, mu1, mu2))				
				
		data = np.asarray(data)
		

	
		#criterion to stop iteration
		##epsilon = sqrt(max(bounds)-min(bounds))
		epsilon = 0.0005
		
		stop = False

		totalParamshift = -1

		fittingLoops = 0

		while  not stop :  
			#step1
			bimodalLoops +=1
			
			classification = np.zeros(len(data))
			for i in range(len(subDistributions)):
	
				classification[subDistributions[i].getModelpdf(data) > np.asarray([max([subDistributions[j].getModelpdf(d) for j in range(len(subDistributions)) if j != i]) for d in data])] = i+1				
				## wordy, but should hopefully work
				
				##classification[st.norm.pdf(data, mu1, sigma1) > st.norm.pdf(data, mu2, sigma2)] = 1
	
			##mu1_old, mu2_old, sigma1_old, sigma2_old = mu1, mu2, sigma1, sigma2
		
			#step2

			paramshift = 0.0

			for i in range(len(subDistributions)):
				k = i+1
				
				
				distId = subDistributions[i].getDistributionScipyId()
				
				pars = getScipyFitById(distId, data[classification == k])
				if(distId == "norm"):
					mu, sigma = pars
					
					paramshift += distId = subDistributions[i].getSquareParamShift(mu, sigma)
					
					subDistributions[i].x0 = mu
					subDistributions[i].sigma = sigma
					
					
					
				elif(distId == "uniform"):
					a, w = pars

					paramshift += distId = subDistributions[i].getSquareParamShift(a, a+w)

					subDistributions[i].a = a
					subDistributions[i].b = a+w
					
					
					
				else:
					x0 = pars
					
					paramshift += distId = subDistributions[i].getSquareParamShift(x0)
					
					subDistributions[i].x0 = x0
	
			
	
			#stopping criterion
			##paramshift = ((mu1_old - mu1)**2 + (mu2_old - mu2)**2 +(sigma1_old - sigma1)**2 +(sigma2_old - sigma2)**2)
			
			if(totalParamshift == -1):
				totalParamshift = paramshift - epsilon
			
			else:
				prog = ((paramshift - epsilon)/totalParamshift)
				## rough measure of how close we are to our target of getting
				## paramshift for a given run under epsilon
				if(prog < 0):
					prog = 0.00
				print paramshift, epsilon, prog
			
				##plt.plot(trueBins, [estMod1.getExpectedBinCount(xval, binwidth, samples*rate1) for xval in model.bins[:-1]],'m_', alpha=(0.75*(0.5 + 0.5*prog)), linewidth=2, markersize=2)			
				##plt.plot(trueBins, [estMod2.getExpectedBinCount(xval, binwidth, samples*rate2) for xval in model.bins[:-1]],'y_', alpha=(0.75*(0.5 + 0.5*prog)), linewidth=2, markersize=2)					
			stop = paramshift < epsilon
			if(stop):
				print "Finished fitting bimodal case"
		
		
		## now that the fitter is finished working, we use the fact that the
		## data set is now sorted into classifications to fit the distributions
		## to the data set 
		
		for i in range(len(subDistributions)):
			k = i+1
			
			distType = subDistributions[i].getDistributionScipyId()
			
			if(distType == "norm"):
				self.subDistributions.append(normalModel(data[classification == k]))
			elif(distType == "expon"):
				self.subDistributions.append(exponentialModel(data[classification == k]))	
			elif(distType == "uniform"):
				self.subDistributions.append(uniformModel(data[classification == k]))		
		
		#result    
		print "epsilon, ", epsilon
		print "%i Loops run to fit %i-modal case" % (bimodalLoops, len(distributionTypes))
		
		for i in range(len(self.subDistributions)):
			k = i+1
			print min(data[classification == k]), max(data[classification == k])		
		
	def getDistributionScipyId(self):
		return 'multimodal'	
		## this could be a problem eventually

	def getModelpdf(self, x):
		return sum([mod.getModelpdf(x)*mod.getFractionOfTotalDataset(self.getDatasetSize()) for mod in self.subDistributions])
	
	def sampleFromDistribution(self):
		choice = random.random()
		
		topProbHere = 0.0
		for subDist in self.subDistributions:
			topProbHere += subDist.getFractionOfTotalDataset(self.getDatasetSize())
			if(choice <= topProbHere):
				return subDist.sampleFromDistribution()
	
	def getTestStatistic(self, test):
		return sum([mod.getTestStatistic(test) for mod in self.subDistributions])			

		
	def distributionDescription(self):		
		output = "Multimodal Distribution with %i modes, p=%.3f\n" % (len(self.subDistributions), self.getTestStatistic("K-S"))
		for subDist in self.subDistributions:
			output += "-%s" % subDist.distributionDescription()
		return output
