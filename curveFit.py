import numpy as np
from numpy import pi, r_
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.optimize import curve_fit 
import pylab
from math import *


class Data2(object):
    """An instance of data collected from the Aethalometer."""

    def __init__(self, BC1, BC2, BC3, BC4, BC5, BC6, BC7, time=None):
        """Initializes data from Aethalmeter. Sets values for AlphaBrC, massBC and
        massBrC to None. Sets meanVariance to None"""
        self.xdata = np.array([1.872,1.692,1.492,1.333,1,.926])
        self.BCdata2 = BC2
        self.BCdata3 = BC3
        self.BCdata4 = BC4
        self.BCdata5 = BC5
        self.BCdata6 = BC6
        self.BCdata7 = BC7
        self.ydata = np.array([BC2,BC3,BC4,BC5,BC6,BC7])
        self.AlphaBrC = None
        self.massBC = None
        self.massBrC = None
        self.time = time
        self.list = None #AlphaBrC,massBC,massBrC


	def func(self, x, a, MassBC, A):
		return A*(x**(-a)) + MassBC

	def curvefit(self):
		fitted = curve_fit(func, self.xdata, self.ydata)
		self.AlphaBrC = fitted[0][0]
		self.massBC = fitted[0][1]
		self.massBrC = fitted[0][2]
		self.list = [self.AlphaBrC,self.massBC,self.massBrC]
		



