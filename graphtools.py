## graphtools.py ###############################################################
## graphing functions used by the analysis script(s) ###########################
################################################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy import stats



def plotHistogram(xlabel, ylabel, title, values, output_filename, minShow='foo', maxShow='bar', binCount=39):
	## TLDR, takes a set of values and histograms them, whoop whop
	if(minShow == 'foo'):
		## if we dont get anything for a manual max min, just set our max and
		## min values for the graph range from the data
		minShow = float(int(min(values)))	
		maxShow = float(int(max(values)))			
	
	n, bins, patches = plt.hist(values, binCount, normed=0, facecolor='blue', alpha = 0.65)
	## histogram construction step
	## I forget, I think this was copy paste
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	## label our axes like good students
	plt.title(title)
	## an' title it
	plt.axis([minShow, maxShow, 0.0, 40.0])
	## 40 here was a working value for the range of possible bin values for this
	## dataset
	
	## I need to figure out how to get a max from our plt.hist output
	plt.grid(True)
	## make sure we got a grid on
	##plt.show()
	## showit
	plt.savefig(output_filename)
	plt.close()
	
	
def plotScatterplot(xlabel, ylabel, title, x_values, y_values, output_filename, minShow='foo', maxShow='bar', binCount=39):
	## TLDR, takes a set of values and histograms them, whoop whop
	if(minShow == 'foo'):
		## if we dont get anything for a manual max min, just set our max and
		## min values for the graph range from the data
		minShow = float(int(min(x_values)))	
		maxShow = float(int(max(x_values)))			
	
	plt.plot(x_values, y_values, 'bs')
		
	
	gradient, intercept, r_value, p_value, std_err = stats.linregress(x_values,y_values)
	
	y_model = []
	
	for x in x_values:
		y = gradient*x + intercept
		y_model.append(y)
	
	plt.plot(x_values, y_model, "g")
	r_square = r_value**2
	## histogram construction step
	## I forget, I think this was copy paste
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	## label our axes like good students
	
	title = "%s, r^2 = %f" % (title, r_square)
	
	plt.title(title)
	## an' title it
	plt.axis([minShow, maxShow, 0.0, 1.2])
	## win percentages between 0.000 and 1.000, so we put our top limit a bit
	## higher, so we can see the 1.000 datapoints without them going off the
	## graph
	
	## I need to figure out how to get a max from our plt.hist output
	plt.grid(True)
	## make sure we got a grid on
	##plt.show()
	## showit
	plt.savefig(output_filename)
	plt.close()



