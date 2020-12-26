## stat.py #####################################################################
## core shitty statistics module ###############################################
################################################################################
import math
import scipy.stats

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
	
def geometricMean(dataSet):
	output = 1.000
	n = len(dataSet)
	
	for cy in dataSet:
		output *= cy
	output = math.pow(output, (1/float(n)))
	return output
	
def isInteger(value):
	if(value == int(value)):
		return True
	else:
		return False	

def twoClosestIntegers(value):
	roundedValue = int(value)
	if(roundedValue < value):
		return [roundedValue, roundedValue+1]
	elif(roundedValue > value):
		return [roundedValue-1, roundedValue]
	else:
		print("twoClosestIntegers() called on integer %f, crashing everything..." % value)
		return []


def getSkewness(dataSet):
	sumCubes = 0.0
	sumSquares = 0.0
	
	mean = Mean(dataSet)
	n = float(len(dataSet))
	
	
	for cy in dataSet:
		sumCubes += (cy-mean)**3
		sumSquares += (cy-mean)**2		
	
	output = (sumCubes/n)/((sumSquares/n)**1.5)
	return output

def getAdjustedKurtosis(dataSet):
	return scipy.stats.kurtosis(dataSet)
	
def getValueForPercentile(percentile, dataSet):
	n = float(len(dataSet))
	## plus 1 here because the dataset in the notes is from [y(1), ..., y(n)]
	
	m = percentile*(n+1.0)	
	
	print(sorted(dataSet))
	print([(i, (i+1), sorted(dataSet)[i]) for i in range(0, len(dataSet))])
	print("percentile %f, n %f" % (percentile, n))
	print("m %f, adjusted %d" % (m, (int(m) -2)))
	if(not isInteger(m)):
		print(twoClosestIntegers(m))
		
	if(isInteger(m)):
		return sorted(dataSet)[int(m)]
	else:
		return (sorted(dataSet)[twoClosestIntegers(m)[0]-2] + sorted(dataSet)[twoClosestIntegers(m)[1]-2])/2.0
	
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
		## average the two middle ones

		
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
	print("array\n-> ", testArray, "\nsorted\n-> ", sorted(testArray))
	
	print("Array length = %d\nArray Mean = %f,\nArray Median = %f,\nArray Mode %d\nArray Geometric Mean %f\nArray Skewness %f\nArray Kurtosis %f" % (len(testArray), Mean(testArray), Median(testArray), Mode(testArray), geometricMean(testArray), getSkewness(testArray), getAdjustedKurtosis(testArray)))
	##print "Array percentiles\np(0) %.3f, p(25) %.3f, p(50) %.3f, p(75) %.3f, p(100) %.3f" % (getValueForPercentile(0.0, testArray), getValueForPercentile(0.25, testArray), getValueForPercentile(0.5, testArray), getValueForPercentile(0.75, testArray), getValueForPercentile(1.00, testArray))
	print("Array Variance = %f\nArray Standard Deviation = %f" % (Variance(testArray), standardDeviation(testArray)))

if(__name__ == "__main__"):
	
	import random
	testListFunctions()







