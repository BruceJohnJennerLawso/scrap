## graphtools.py ###############################################################
## graphing functions used by the analysis script(s) ###########################
################################################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy import stats


def generateHistogram(xlabel, ylabel, title, values, output_path, output_directory, output_filename, subplot_col, subplot_row, subplot_no, minShow='foo', maxShow='bar', binCount=39):
	if(minShow == 'foo'):
		## if we dont get anything for a manual max min, just set our max and
		## min values for the graph range from the data
		minShow = float(int(min(values)))	
		maxShow = float(int(max(values)))			
	
	plt.subplot(subplot_col, subplot_row, subplot_no)
	
	n, bins, patches = plt.hist(values, binCount, normed=0, facecolor='blue', alpha = 0.65)
	## histogram construction step
	## I forget, I think this was copy paste
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	## label our axes like good students
	plt.title(title)
	## an' title it
	plt.axis([minShow, maxShow, 0.0, 60.0])
	## 40 here was a working value for the range of possible bin values for this
	## dataset
	
	## I need to figure out how to get a max from our plt.hist output
	plt.grid(True)
	## make sure we got a grid on
	##plt.show()
	## showit

def plotHistogram(xlabel, ylabel, title, values, output_path, output_directory, output_filename, minShow='foo', maxShow='bar', binCount=39):
	## TLDR, takes a set of values and histograms them, whoop whop
	generateHistogram(xlabel, ylabel, title, values, output_path, output_directory, output_filename, 1, 1, 1, minShow, maxShow, binCount)
	output_ = "%s/%s/%s" % (output_path, output_directory, output_filename)
	plt.savefig(output_)
	plt.close()
	
def trendline(x, gradient, intercept):
	output = gradient*x + intercept		
	return output
	
def plotScatterplot(xlabel, ylabel, title, x_values, y_values, output_path, output_directory, output_filename, minShow='foo', maxShow='bar', binCount=39):
	## TLDR, takes a set of values and histograms them, whoop whop
	if(minShow == 'foo'):
		## if we dont get anything for a manual max min, just set our max and
		## min values for the graph range from the data
		minShow = float(int(min(x_values)))	
		maxShow = float(int(max(x_values)))			
	
	modifiers =  [0.5, 1.0, 1.50]
	
	
		
	
	gradient, intercept, r_value, p_value, std_err = stats.linregress(x_values,y_values)
	

	for k in modifiers:
		for l in modifiers:
			grad = k*gradient
			interc = intercept*l
			y_model = []
			
			for x in x_values:
				y_model.append(trendline(x, grad, interc))
			plt.plot(x_values, y_model, 'm-', alpha=0.4)			
	
	y_model = []
	
	for x in x_values:
		y = trendline(x, gradient, intercept)
		y_model.append(y)
		


	plt.plot(x_values, y_model, "g")

	plt.plot(x_values, y_values, 'bs')

	r_square = r_value**2
	## histogram construction step
	## I forget, I think this was copy paste
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	## label our axes like good students
	
	title = "%s,\n r^2 = %f, p = %f\n(k*m)x + (l*b)" % (title, r_square, p_value)
	
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
	output_ = "%s/%s/%s" % (output_path, output_directory, output_filename)
	plt.savefig(output_)
	plt.close()	

	for k in range(0, len(modifiers)):
		for l in range(0, len(modifiers)):
			
			grad = modifiers[k]*gradient
			interc = intercept*modifiers[l]
			modelDeltas = []
			for i in range(0, len(x_values)):

				modelDelta = y_values[i] - trendline(x_values[i], grad, interc)
				modelDeltas.append(modelDelta)

				histTitle = "k = %.2f, l = %.2f\n(k*m)x + (l*b)" % (modifiers[k], modifiers[l])
				histOutputFilename = "%s_deltaModelHistogram_k%f_l%f.png" % (output_filename, k, l)
			##plotloc = ( k*len(modifiers) + (l+1) )
			plotloc = l+1
			print "k %i, l %i, %i" % (k, l, plotloc)
			generateHistogram("Delta from model", "Count", histTitle, modelDeltas, output_path, output_directory, histOutputFilename, len(modifiers), 1, plotloc , -2.0, 2.0, 40)
	

		left  = 0.125  # the left side of the subplots of the figure
		right = 0.9    # the right side of the subplots of the figure
		bottom = 0.1   # the bottom of the subplots of the figure
		top = 0.9      # the top of the subplots of the figure
		wspace = 0.2   # the amount of width reserved for blank space between subplots
		hspace = 0.2   # the amount of height reserved for white space between subplots

		plt.subplots_adjust(left, bottom, right, top, 4*wspace, 4*hspace)

		output_ = "%s/%s/modelDeltas_k_%f_%s" % (output_path, output_directory, modifiers[k], output_filename)
		plt.savefig(output_)
		plt.close()	

