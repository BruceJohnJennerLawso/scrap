## modelSelection.py ###########################################################
## using models defined under distModel, fitting them alone or #################
## in groups to define a dataset ###############################################
################################################################################
from modelMultimodal import *




import matplotlib
if(__name__ != "__main__"):
	matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab



import math
import scipy.stats
import numpy as np

from distStats import *



import scipy.stats as st
import random

np.seterr(all='warn')





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
		generatedMean = -2.5 + random.random()*5.0
		generatedSigma = 0.1 + random.random()*0.4
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
	elif(currentChoice == 8):	
		return [normalModel([], 0.0, False, 1.443, 0.255), normalModel([], 0.0, False, -1.681, 0.273), exponentialModel([], 0.0, False, 0.078)]
	elif(currentChoice == 9):	
		return [normalModel([], 0.0, False, 4.443, 0.255), normalModel([], 0.0, False, 8.681, 0.273), normalModel([], 0.0, False, 12.844, 0.290)]
	elif(currentChoice == 10):	
		return [normalModel([], 0.0, False, 4.443, 0.255), normalModel([], 0.0, False, 4.481, 2.273)]
	elif(currentChoice == 11):	
		return [normalModel([], 0.0, False, 4.443, 0.255), normalModel([], 0.0, False, 4.481, 2.273), exponentialModel([], 0.0, False, 0.401,)]		


if(__name__ == "__main__"):


	choices = [0,1,2,3,4]
	currentChoice = random.choice(choices)


	samples = 4800

	currentChoice = 9


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
	
	
	distList = sorted(zip(distributions, mles), key=lambda d: d[1])
	

	nthBestDistributionChosen = 0
	
	model = None
	
	while(True):
		print nthBestDistributionChosen, nthBestDistributionChosen+1, len(distList)
		
		currentDistribution = distList[nthBestDistributionChosen]
		print "Best fit %s, building model..." % currentDistribution[0].name
		
		try:
			model = getDistributionByScipyId(currentDistribution[0].name, data, currentDistribution[1])
		except ValueError:
			## we tried to fit, but the fitter coughed up a hairball, likely because
			## the distribution we got wasnt actually that great of a fit for the
			## data
			
			nthBestDistributionChosen += 1
			
			
			if(nthBestDistributionChosen < len(distList)):
				continue
			else:
				## ran out of distributions to fit to the data, giving up on
				## life
				print "Unable to fit model to data"
				ableToFit = False	
				break
		break
	
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
	
		plt.plot(trueBins, modelPrediction,'go-',label="Model Curve", alpha=0.75, linewidth=2, color='g', markersize=2)
	
		## hoping this is actually true
	
	
		fivePt = [(min(model.bins[:-1]) + k*(max(model.bins[:-1]) - min(model.bins[:-1]))) for k in [0.0,0.25,0.50,0.75, 1.0] ]
		print fivePt
		print [model.getModelpdf(x) for x in fivePt]



		if(not multimodal):
			## an exponential distribution was detected			
			plt.plot(trueBins, [initialModel.getExpectedBinCount(xval, binwidth, samples) for xval in model.bins[:-1]],'ro-',label="Target Curve", alpha=0.75, linewidth=2, markersize=2)
		else:
			plt.plot(trueBins, [samples*sum([mod.getBinProb(xval, binwidth)*mod.getSampleProportion(samples) for mod in initialModel]) for xval in model.bins[:-1]],'co-',label="Target Curve Net pdf", alpha=0.75, linewidth=2, markersize=2)					
			
			for mod in initialModel:
				plt.plot(trueBins, [mod.getExpectedBinCount(xval, binwidth, samples*mod.getSampleProportion(samples)) for xval in model.bins[:-1]],'ro-',label="Target Curve %i (%s), sample proportion %.3f" % ((initialModel.index(mod) +1), mod.getDistributionScipyId(), (mod.sampledCount/float(samples))), alpha=0.60 + 0.2*float(1.0/len(initialModel)), linewidth=2, markersize=2)			

	if(currentChoice == 9):
		trimodDist = multiModalModel(data, ['norm', 'norm', 'norm'])
		
		print trimodDist.distributionDescription()
		plt.plot(trueBins, [trimodDist.getExpectedBinCount(xval, binwidth, samples) for xval in model.bins[:-1]],'c--',label="Fitted Total Curve in Multimodal Case", alpha=0.75, linewidth=2, markersize=2)							
	if(currentChoice == 11):
		trimodDist = multiModalModel(data, ['norm', 'norm', 'expon'])
		
		print trimodDist.distributionDescription()
		plt.plot(trueBins, [trimodDist.getExpectedBinCount(xval, binwidth, samples) for xval in model.bins[:-1]],'c--',label="Fitted Total Curve in Multimodal Case", alpha=0.75, linewidth=2, markersize=2)				
	else:
		data = np.asarray(data)
		
		mu1 = min(bounds)
		sigma1 = (1/3.0)*(max(bounds)-min(bounds))

		mu2 = max(bounds)
		sigma2 = sqrt(sigma1)
	
		#criterion to stop iteration
		epsilon = sqrt(max(bounds)-min(bounds))
		epsilon = 0.0005


		mu1 = min(bounds) + (max(bounds)-min(bounds))/2.0
		mu2 = min(bounds) + (max(bounds)-min(bounds))/2.0		
		

		print "epsilon, ", epsilon
		print "dist1, ", mu1, sigma1
		print "dist2, ", mu2, sigma2
		stop = False

		totalParamshift = -1

		bimodalLoops = 0

		while  not stop :  
			#step1
			bimodalLoops +=1
			
			classification = np.zeros(len(data))
			classification[st.norm.pdf(data, mu1, sigma1) > st.norm.pdf(data, mu2, sigma2)] = 1
	
			mu1_old, mu2_old, sigma1_old, sigma2_old = mu1, mu2, sigma1, sigma2
		
			#step2
			pars1 = st.norm.fit(data[classification == 1])
			mu1, sigma1 = pars1
			pars2 = st.norm.fit(data[classification == 0])
			mu2, sigma2 = pars2
	
	
			estMod1 = normalModel([], 1.0, False, mu1, sigma1)
		
			rate1 = np.mean(classification)
			rate2 = 1.0 - rate1
			
			estMod2 = normalModel([], 1.0, False, mu2, sigma2)	
	
			#stopping criterion
			paramshift = ((mu1_old - mu1)**2 + (mu2_old - mu2)**2 +(sigma1_old - sigma1)**2 +(sigma2_old - sigma2)**2)
			if(totalParamshift == -1):
				totalParamshift = paramshift - epsilon
				plt.plot(trueBins, [estMod1.getExpectedBinCount(xval, binwidth, samples*rate1) for xval in model.bins[:-1]],'m', alpha=(0.75*(0.5)), linewidth=2, markersize=2)			
				plt.plot(trueBins, [estMod2.getExpectedBinCount(xval, binwidth, samples*rate2) for xval in model.bins[:-1]],'y', alpha=(0.75*(0.5)), linewidth=2, markersize=2)								
			
			else:
				prog = ((paramshift - epsilon)/totalParamshift)
				if(prog < 0):
					prog = 0.00
				print paramshift, epsilon, prog
			
				plt.plot(trueBins, [estMod1.getExpectedBinCount(xval, binwidth, samples*rate1) for xval in model.bins[:-1]],'m_', alpha=(0.75*(0.5 + 0.5*prog)), linewidth=2, markersize=2)			
				plt.plot(trueBins, [estMod2.getExpectedBinCount(xval, binwidth, samples*rate2) for xval in model.bins[:-1]],'y_', alpha=(0.75*(0.5 + 0.5*prog)), linewidth=2, markersize=2)					
			stop = paramshift < epsilon
			if(stop):
				print "Finished fitting bimodal case"
		#result    
		##print "The first density is gaussian, mean=%.3f, sigma=%.3f :" % ( mu1, sigma1)
		##print "The second density is gaussian, mean=%.3f, sigma=%.3f :" % (mu2, sigma2)
		print("A rate of ", np.mean(classification), "is classified in the first density")
		print "epsilon, ", epsilon
		print "dist1, ", mu1, sigma1
		print "dist2, ", mu2, sigma2
		print "%i Loops run to fit bimodal case" % bimodalLoops
		estMod1 = normalModel([], 1.0, False, mu1, sigma1)
		
		rate1 = np.mean(classification)
		rate2 = 1.0 - rate1
		
		estMod2 = normalModel([], 1.0, False, mu2, sigma2)
		
		
		binwidth = model.bins[:-1][1] - model.bins[:-1][0]	
		
		trueBins = [(binstart+(0.5*binwidth)) for binstart in model.bins[:-1]]
		
		plt.plot(trueBins, [estMod1.getExpectedBinCount(xval, binwidth, samples*rate1) + estMod2.getExpectedBinCount(xval, binwidth, samples*rate2) for xval in model.bins[:-1]],'c--',label="Fitted Total Curve in Bimodal Case", alpha=0.75, linewidth=2, markersize=2)			
		for mod in [1, 2]:
			if(mod == 1):
				rate = rate1
				currentModel = estMod1
				colo = 'm'
			elif(mod == 2):
				rate = rate2
				currentModel = estMod2	
				colo = 'y'
			plt.plot(trueBins, [currentModel.getExpectedBinCount(xval, binwidth, samples*rate) for xval in model.bins[:-1]],'%s--' % colo,label="Fitted Normal Curve in Bimodal Case", alpha=0.75, linewidth=2, markersize=2)
		print min(data[classification == 0]), max(data[classification == 0])		
		
		print min(data[classification == 1]), max(data[classification == 1])

		ks0 = scipy.stats.kstest(np.asarray(data[classification == 0]), 'norm', args=(mu2, sigma2))
		ks1 = scipy.stats.kstest(np.asarray(data[classification == 1]), 'norm', args=(mu1, sigma1))	
		kswhatever = scipy.stats.kstest(np.asarray(data[classification == 1]), 'norm')	
		print ks0 
		print ks1
		print kswhatever
		print "Product, ", (ks0[0]*ks1[0])
		print "Sum, ", (ks0[0]+ks1[0])	
	
	print model.getTestStatistic("K-S")
		
	print model.distributionDescription()

	plt.legend(loc=2,prop={'size':10})
	plt.show()



























def oldStyleFitter(currentChoice):

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
	
	
	distList = sorted(zip(distributions, mles), key=lambda d: d[1])
	

	nthBestDistributionChosen = 0
	
	model = None
	
	while(True):
		print nthBestDistributionChosen, nthBestDistributionChosen+1, len(distList)
		
		currentDistribution = distList[nthBestDistributionChosen]
		print "Best fit %s, building model..." % currentDistribution[0].name
		
		try:
			model = getDistributionByScipyId(currentDistribution[0].name, data, currentDistribution[1])
		except ValueError:
			## we tried to fit, but the fitter coughed up a hairball, likely because
			## the distribution we got wasnt actually that great of a fit for the
			## data
			
			nthBestDistributionChosen += 1
			
			
			if(nthBestDistributionChosen < len(distList)):
				continue
			else:
				## ran out of distributions to fit to the data, giving up on
				## life
				print "Unable to fit model to data"
				ableToFit = False	
				break
		break
	
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
	
		plt.plot(trueBins, modelPrediction,'go-',label="Model Curve", alpha=0.75, linewidth=2, color='g', markersize=2)
	
		## hoping this is actually true
	
	
		fivePt = [(min(model.bins[:-1]) + k*(max(model.bins[:-1]) - min(model.bins[:-1]))) for k in [0.0,0.25,0.50,0.75, 1.0] ]
		print fivePt
		print [model.getModelpdf(x) for x in fivePt]



		if(not multimodal):
			## an exponential distribution was detected			
			plt.plot(trueBins, [initialModel.getExpectedBinCount(xval, binwidth, samples) for xval in model.bins[:-1]],'ro-',label="Target Curve", alpha=0.75, linewidth=2, markersize=2)
		else:
			plt.plot(trueBins, [samples*sum([mod.getBinProb(xval, binwidth)*mod.getSampleProportion(samples) for mod in initialModel]) for xval in model.bins[:-1]],'co-',label="Target Curve Net pdf", alpha=0.75, linewidth=2, markersize=2)					
			
			for mod in initialModel:
				plt.plot(trueBins, [mod.getExpectedBinCount(xval, binwidth, samples*mod.getSampleProportion(samples)) for xval in model.bins[:-1]],'ro-',label="Target Curve %i (%s), sample proportion %.3f" % ((initialModel.index(mod) +1), mod.getDistributionScipyId(), (mod.sampledCount/float(samples))), alpha=0.60 + 0.2*float(1.0/len(initialModel)), linewidth=2, markersize=2)			
			
			
	if(True):
		data = np.asarray(data)
		
		mu1 = min(bounds)
		sigma1 = (1/3.0)*(max(bounds)-min(bounds))

		mu2 = max(bounds)
		sigma2 = sqrt(sigma1)
	
		#criterion to stop iteration
		epsilon = sqrt(max(bounds)-min(bounds))
		epsilon = 0.0005


		mu1 = min(bounds) + (max(bounds)-min(bounds))/2.0
		mu2 = min(bounds) + (max(bounds)-min(bounds))/2.0		
		

		print "epsilon, ", epsilon
		print "dist1, ", mu1, sigma1
		print "dist2, ", mu2, sigma2
		stop = False

		totalParamshift = -1

		bimodalLoops = 0

		while  not stop :  
			#step1
			bimodalLoops +=1
			
			classification = np.zeros(len(data))
			classification[st.norm.pdf(data, mu1, sigma1) > st.norm.pdf(data, mu2, sigma2)] = 1
	
			mu1_old, mu2_old, sigma1_old, sigma2_old = mu1, mu2, sigma1, sigma2
		
			#step2
			pars1 = st.norm.fit(data[classification == 1])
			mu1, sigma1 = pars1
			pars2 = st.norm.fit(data[classification == 0])
			mu2, sigma2 = pars2
	
	
			estMod1 = normalModel([], 1.0, False, mu1, sigma1)
		
			rate1 = np.mean(classification)
			rate2 = 1.0 - rate1
			
			estMod2 = normalModel([], 1.0, False, mu2, sigma2)	
	
			#stopping criterion
			paramshift = ((mu1_old - mu1)**2 + (mu2_old - mu2)**2 +(sigma1_old - sigma1)**2 +(sigma2_old - sigma2)**2)
			if(totalParamshift == -1):
				totalParamshift = paramshift - epsilon
				plt.plot(trueBins, [estMod1.getExpectedBinCount(xval, binwidth, samples*rate1) for xval in model.bins[:-1]],'m', alpha=(0.75*(0.5)), linewidth=2, markersize=2)			
				plt.plot(trueBins, [estMod2.getExpectedBinCount(xval, binwidth, samples*rate2) for xval in model.bins[:-1]],'y', alpha=(0.75*(0.5)), linewidth=2, markersize=2)								
			
			else:
				prog = ((paramshift - epsilon)/totalParamshift)
				if(prog < 0):
					prog = 0.00
				print paramshift, epsilon, prog
			
				plt.plot(trueBins, [estMod1.getExpectedBinCount(xval, binwidth, samples*rate1) for xval in model.bins[:-1]],'m_', alpha=(0.75*(0.5 + 0.5*prog)), linewidth=2, markersize=2)			
				plt.plot(trueBins, [estMod2.getExpectedBinCount(xval, binwidth, samples*rate2) for xval in model.bins[:-1]],'y_', alpha=(0.75*(0.5 + 0.5*prog)), linewidth=2, markersize=2)					
			stop = paramshift < epsilon
			if(stop):
				print "Finished fitting bimodal case"
		#result    
		##print "The first density is gaussian, mean=%.3f, sigma=%.3f :" % ( mu1, sigma1)
		##print "The second density is gaussian, mean=%.3f, sigma=%.3f :" % (mu2, sigma2)
		print("A rate of ", np.mean(classification), "is classified in the first density")
		print "epsilon, ", epsilon
		print "dist1, ", mu1, sigma1
		print "dist2, ", mu2, sigma2
		print "%i Loops run to fit bimodal case" % bimodalLoops
		estMod1 = normalModel([], 1.0, False, mu1, sigma1)
		
		rate1 = np.mean(classification)
		rate2 = 1.0 - rate1
		
		estMod2 = normalModel([], 1.0, False, mu2, sigma2)
		
		
		binwidth = model.bins[:-1][1] - model.bins[:-1][0]	
		
		trueBins = [(binstart+(0.5*binwidth)) for binstart in model.bins[:-1]]
		
		plt.plot(trueBins, [estMod1.getExpectedBinCount(xval, binwidth, samples*rate1) + estMod2.getExpectedBinCount(xval, binwidth, samples*rate2) for xval in model.bins[:-1]],'c--',label="Fitted Total Curve in Bimodal Case", alpha=0.75, linewidth=2, markersize=2)			
		for mod in [1, 2]:
			if(mod == 1):
				rate = rate1
				currentModel = estMod1
				colo = 'm'
			elif(mod == 2):
				rate = rate2
				currentModel = estMod2	
				colo = 'y'
			plt.plot(trueBins, [currentModel.getExpectedBinCount(xval, binwidth, samples*rate) for xval in model.bins[:-1]],'%s--' % colo,label="Fitted Normal Curve in Bimodal Case", alpha=0.75, linewidth=2, markersize=2)
		print min(data[classification == 0]), max(data[classification == 0])		
		
		print min(data[classification == 1]), max(data[classification == 1])

	ks0 = scipy.stats.kstest(np.asarray(data[classification == 0]), 'norm', args=(mu2, sigma2))
	ks1 = scipy.stats.kstest(np.asarray(data[classification == 1]), 'norm', args=(mu1, sigma1))	
	kswhatever = scipy.stats.kstest(np.asarray(data[classification == 1]), 'norm')	
	print ks0 
	print ks1
	print kswhatever
	print "Product, ", (ks0[0]*ks1[0])
	print "Sum, ", (ks0[0]+ks1[0])	
	
	print model.getTestStatistic("K-S")
	print model.distributionDescription()

	plt.legend(loc=2,prop={'size':10})
	plt.show()
