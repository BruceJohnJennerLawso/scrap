## stat.py #####################################################################
## core shitty statistics module ###############################################
################################################################################
import math


## calls for the 3 basic properties of datasets ################################
################################################################################

def Mean(dataSet):
	output = 0
	for cy in dataSet:
		output += cy
	output /= float(len(dataSet))
	## gotta make sure its a float, otherwise our mean gets rounded like
	## an integer, which we dont want
	return output
	
def isOdd(value):
	if(value%2 != 0):
		return True	
	else:
		return False
	
def Median(dataSet):
	sortedData = sorted(dataSet)
	arrayLen = len(sortedData)
	if(isOdd(arrayLen)):
		## we take the middle value
		return sortedData[ (arrayLen+1)/2 -1 ]
		## not very confident with that, lets see if it works
	else:
		return float(sortedData[ (arrayLen/2) -1 ] + sortedData[ (arrayLen/2) ])/2
		
def Mode(dataSet):
	##sortedData = sorted(dataSet)
	mode = dataSet[0]
	maxHits = 0
	
	for cy in dataSet:
		##print "checking cy=%f, current maxHits is %f" % (cy, maxHits)
		hit = -1
		## negative 1, because we have to find the value itself at least once
		for cycy in dataSet:
			if(cycy == cy):
				hit += 1
		##print "Finished checking the list for hits, %f were found, previous maximum was %f" % (hit, maxHits)
		if(hit >= maxHits):
			mode = cy
			maxHits = hit
	return mode
		

def Variance(dataSet):
	mean = Mean(dataSet)
	
	N = float(len(dataSet))
	output = 0

	for cy in dataSet:
		output += ((cy - mean)**2)
	output /= (N - 1)
	return output
	
def standardDeviation(dataSet):
	variance = Variance(dataSet)
	output = math.sqrt(variance)
	return output

def absoluteMeanUncertainty(dataSet):
	sigma = standardDeviation(dataSet)
	output = sigma
	N = float(len(dataSet))
	output /= math.sqrt(N)
	## where our output sigma_{xbar} is the uncertainty +/- around the mean
	## -> the uncertainty of the mean
	return output
		



def probabilityAt(x, dataSet):
	mean = Mean(dataSet)
	variance = Mean(dataSet)
	deviation = standardDeviation(dataSet)

	output = math.exp( -((x - mean)**2)/(2*variance) )
	output /= (deviation * math.sqrt(2* math.pi))
	return output



	
## random value generators for convenience #####################################
################################################################################		
		
def randomValue(floor, ceiling):
	value = floor + (random.random()*(ceiling - floor))
	return value		
		
def randomIntegerValue(floor, ceiling):
	return int(randomValue(floor, ceiling+1))



## module tests ################################################################
################################################################################


def testListFunctions():
	testArray = []
	for i in range(randomIntegerValue(5,25)):
		randam = randomIntegerValue(0,10)
		testArray.append(randam)
	print "array\n-> ", testArray, "\nsorted\n-> ", sorted(testArray)
	
	print "Array length = %d\nArray Mean = %f,\nArray Median = %f,\nArray Mode %d" % (len(testArray), Mean(testArray), Median(testArray), Mode(testArray))
	print "Array Variance = %f\nArray Standard Deviation = %f" % (Variance(testArray), standardDeviation(testArray))

if(__name__ == "__main__"):
	
	import random
	testListFunctions()







