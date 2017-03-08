## bimod.py ####################################################################
## identifying bimodal distributions ###########################################
################################################################################
import numpy as np
import scipy.stats as st



if(__name__ == "__main__"):
	#hard coded data generation
	data = np.random.normal(-3, 1, size = 1000)
	data[600:] = np.random.normal(loc = 3, scale = 2, size=400)

	#initialization

	mu1 = -1
	sigma1 = 1

	mu2 = 1
	sigma2 = 1

	#criterion to stop iteration
	epsilon = 0.1
	stop = False

	while  not stop :  
		#step1
		classification = np.zeros(len(data))
		classification[st.norm.pdf(data, mu1, sigma1) > st.norm.pdf(data, mu2, sigma2)] = 1
	
		mu1_old, mu2_old, sigma1_old, sigma2_old = mu1, mu2, sigma1, sigma2
	
		#step2
		pars1 = st.norm.fit(data[classification == 1])
		mu1, sigma1 = pars1
		pars2 = st.norm.fit(data[classification == 0])
		mu2, sigma2 = pars2
	
	
		#stopping criterion
		stop = ((mu1_old - mu1)**2 + (mu2_old - mu2)**2 +(sigma1_old - sigma1)**2 +(sigma2_old - sigma2)**2) < epsilon

	#result    
	print min(data[classification == 1]), max(data[classification == 1])



	print type(pars1), type(pars2)
	print pars1
	print pars2
	print("The first density is gaussian :", mu1, sigma1)
	print("The first density is gaussian :", mu2, sigma2)
	print("A rate of ", np.mean(classification), "is classified in the first density")
