## makeItFourier.py ############################################################
## smbc said it best ###########################################################
################################################################################
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

import math

def graph2dData(x, y, colour, zoomXAxis=False, threshold=0.001):
	fig, ax = plt.subplots()
	ax.plot(x, y, colour)
	plt.xlabel("x")
	
	
	xMax = max(x)
	for xVal in sorted(x):
		if((xVal <= threshold)and(xVal < xMax)):
			xMax = xVal
		else:
			break
	xMax *= 1.2	
	
	
	plt.axis([min(x), xMax, min(y), 1.2*max(y)])
	plt.show()
	plt.close()

def graphFourierTransform(x, y):
	N = len(y)
	T = 4.00*float(max(x) - min(y))/N
	## sure hope x is evenly spaced
	print "N, %i, T, %f" % (N, T)
	yf = scipy.fftpack.fft(y)
	print "yf, len %i, [%f, %f]" % ( len(yf), min(yf), max(yf))
	xf = np.linspace(0.0, 1.0/(4.0*T), N/2)
	print "xf, len %i, [%f, %f]" % ( len(xf), min(xf), max(xf))
	graph2dData(x, y, 'g')
	graph2dData(xf, 2.0/N * np.abs(yf[:N//2]), 'b', True)

	
def boxcar(x):
	if((x >= 1.0)and(x <=2.0)):
		return 1.0
	return 0.0
	
def sinc(x):
	if(x == 0.0):
		return 1.0
	return float(math.sin(x)/float(x))

def dualFreqSine(x):
	return ( np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x) )

def getSampleXYRanges(yFunc, numSamplePoints, rangeWidth, rangeCentre, xComp=1.0):
	# Number of samplepoints
	N = numSamplePoints
	# sample spacing
	##T = 1.0 / 60000.0
	
	## N*T = rangeWidth
	T = float(rangeWidth)/N
	
	x = np.linspace(rangeCentre-(N*T)/2.0, rangeCentre+(N*T)/2.0, N)
	##y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
	y = [yFunc(xComp*xVal) for xVal in x]
	return x, y


if(__name__ == "__main__"):

	x, y = getSampleXYRanges(sinc, 8*92000, 20.0, 0.0)
	graphFourierTransform(x, y)


