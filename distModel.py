## distModel.py ################################################################
## object used to represent the statistical model assigned to a ################
## data set by curve fitting ###################################################
################################################################################
import matplotlib

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
		
	def getFractionOfTotalDataset(self, totalDatasetSize):
		return (self.getDatasetSize()/float(totalDatasetSize))	
		
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
				return scipy.stats.kstest(np.asarray(self.getDataSet()), self.getDistributionScipyId(), args=(self.getSigmaValue(),))[0]		
			elif(self.getDistributionScipyId() == 'norm'):
				return scipy.stats.kstest(np.asarray(self.getDataSet()), self.getDistributionScipyId(), args=(self.getx0Value(),self.getSigmaValue()))[0]						
			else:
				return scipy.stats.kstest(np.asarray(self.getDataSet()), self.getDistributionScipyId())[0]

	def chosen(self):
		self.sampledCount += 1
		
	def getSampleProportion(self,sampleSize):
		return float(self.sampledCount/float(sampleSize))




		
		
		
