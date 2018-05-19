import numpy as np
from numpy import pi, r_
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.optimize import curve_fit 
import pylab

"""def act():
	# Define function for calculating a power law
	powerlaw = lambda x, MassBC, amp, index: MassBC + amp * (.0513) * (x**index)

	##########
	# Generate data points with noise
	##########

	# Note: all positive, non-zero data
	xdata = array([2.378,1.872,1.692,1.492,1.333,1,.926])
	ydata = array([9640,6539,5299,4291,3577,2796,2754])

	##########
	# Fitting the data -- Least Squares Method
	##########

	# Power-law fitting is best done by first converting
	# to a linear equation and then fitting to a straight line.
	#
	#  y = a * x^b
	#  log(y) = log(a) + b*log(x)
	#

	logx = np.log10(xdata)
	logy = np.log10(ydata)

	# define our (line) fitting function
	fitfunc = lambda x, MassBC, amp, index: MassBC + amp * (.0513) * (x**index)

	pinit = [1.0, -1.0]
	out = optimize.leastsq(errfunc, pinit,
	                       args=(logx, logy, logyerr), full_output=1)

	pfinal = out[0]
	covar = out[1]
	print pfinal
	print covar

	index = pfinal[1]
	amp = 10.0**pfinal[0]

	indexErr = np.sqrt( covar[0][0] )
	ampErr = np.sqrt( covar[1][1] ) * amp

	##########
	# Plotting data
	##########

	plt.clf()
	plt.subplot(2, 1, 1)
	plt.plot(xdata, powerlaw(xdata, amp, index))     # Fit
	plt.errorbar(xdata, ydata, yerr=yerr, fmt='k.')  # Data
	plt.text(5, 6.5, 'Ampli = %5.2f +/- %5.2f' % (amp, ampErr))
	plt.text(5, 5.5, 'Index = %5.2f +/- %5.2f' % (index, indexErr))
	plt.title('Best Fit Power Law')
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.xlim(1, 11)

	plt.subplot(2, 1, 2)
	plt.loglog(xdata, powerlaw(xdata, amp, index))
	plt.errorbar(xdata, ydata, yerr=yerr, fmt='k.')  # Data
	plt.xlabel('X (log scale)')
	plt.ylabel('Y (log scale)')
	plt.xlim(1.0, 11)

act()"""


def func(x, a, MassBC, AMP):
	return AMP*(x**(a)) + MassBC

xdata = np.array([1.872,1.692,1.492,1.333,1,.926])
ydata = np.array([6539,5299,4291,3577,2796,2754])


def act():
	a = curve_fit(func, xdata, ydata)
	plt.plot(xdata, ydata, 'b-', label='data')
	popt, pcov = curve_fit(func, xdata, ydata)
	plt.plot(xdata, func(xdata, *popt), 'r-', label='fit')
	#popt, pcov = curve_fit(func, xdata, ydata, bounds=([3,1000,1000], [6, 4000, 4000]))
	#plt.plot(xdata, func(xdata, *popt), 'g--', label='fit-with-bounds')
	#pylab.show()
	plt.xlabel('x')
	plt.ylabel('y')
	plt.legend()
	plt.show()
	print a[0][0]

act()

