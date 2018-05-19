#customFit2
#Alexander Li
#5/16/17

import numpy
import scipy.optimize as optimize


class Data(object):
    """An instance of data collected from the Aethalometer"""

    def __init__(self, BC1, BC2, BC3, BC4, BC5, BC6, BC7, time=None):
        """Initializes data from Aethalmeter. Sets values for AlphaBrC, massBC and
                massBrC to None. Sets meanVariance to None"""
        self.BCdata1 = BC1
        self.BCdata2 = BC2
        self.BCdata3 = BC3
        self.BCdata4 = BC4
        self.BCdata5 = BC5
        self.BCdata6 = BC6
        self.BCdata7 = BC7
        self.yData = numpy.array([BC1,BC2,BC3,BC4,BC5,BC6,BC7])
        self.yData2 = numpy.array([BC2, BC3, BC4, BC5, BC6, BC7]) #w/o channel 1
        self.xData = numpy.array([880.0/370,880.0/470,880.0/520,880.0/590,880.0/660,880.0/880,880.0/950])#880/Lambda
        self.xData2 = numpy.array([880.0/470, 880.0/520, 880.0/590, 880.0/660, 880.0/880, 880.0/950]) #w/o channel 1
        self.AlphaBrC = None
        self.massBC = None
        self.massBrC = None
        self.alpha = None #trial alpha used in func to find actual alpha
        self.alpha2 = None #trial alpha for curveFitOld

    def func(self, x, A, MBC):
        return A*(x**(self.alpha)) + MBC

    def curveFit(self, a):
        fitted = optimize.curve_fit(self.func, self.xData2, self.yData2)
        perr = numpy.sqrt(numpy.diag(fitted[1]))
        #self.AlphaBrC = self.cround(fitted[0][0])
        #self.massBC = self.cround(fitted[0][1])
        #self.massBrC = self.cround(7.8*fitted[0][2]/0.4)
        #self.list = [self.AlphaBrC,self.massBC,self.massBrC]
        return perr[0]

    def curveFit1(self):
        """Calls curve_fit iteratively to find the best alpha value"""
        dict = {}
        for x in range(8): #try out initial alpha values 1-9
            self.alpha = x+1
            fitted = optimize.curve_fit(self.func, self.xData2, self.yData2)
            perr = numpy.sqrt(numpy.diag(fitted[1]))
            dict[perr[1]] = x #store alpha values with corresponding variance
        minError = min(dict.keys())
        minErrorAlpha = dict[minError]
        print minErrorAlpha
        minErrorAlpha2 = self.curveFit2(minErrorAlpha)
        self.alpha=minErrorAlpha2
        return minErrorAlpha2

    def curveFit2(self, alpha):
        """Calls curve_fit iteratively to find the best alpha value"""
        dict = {}
        self.alpha = alpha - 1 #change starting alpha to curveFit1 alpha-1
        for x in self.crange(alpha-1,alpha+1,.2): #try out initial alpha values +- 1 of the curveFit1() alpha
            self.alpha = x #increment by .2
            fitted = optimize.curve_fit(self.func, self.xData2, self.yData2)
            perr = numpy.sqrt(numpy.diag(fitted[1]))
            dict[perr[1]] = x #store alpha values with corresponding variance
        minError2 = min(dict.keys())
        minErrorAlpha2 = dict[minError2]
        print minErrorAlpha2
        minErrorAlpha3 = self.curveFit3(minErrorAlpha2)
        return minErrorAlpha3

    def curveFit3(self, alpha):
        """Calls curve_fit iteratively to find the best alpha value"""
        dict = {}
        self.alpha = alpha - .2 #change starting alpha to curveFit1 alpha-1
        for x in self.crange(alpha-.2,alpha+.2,.01): #try out initial alpha values +- 1 of the curveFit1() alpha
            self.alpha = x #increment by .2
            fitted = optimize.curve_fit(self.func, self.xData2, self.yData2)
            perr = numpy.sqrt(numpy.diag(fitted[1]))
            dict[perr[1]] = x #store alpha values with corresponding variance
        minError3 = min(dict.keys())
        minErrorAlpha3 = dict[minError3]
        print minErrorAlpha3
        return minErrorAlpha3


    def findAlpha(self, a):
        first = self.curveFit(4)

    def funcOld(self, x, a, MassBC, A):
        """function for curveFitOld"""
        return A*(x**(a)) + MassBC

    def curveFitOld(self):
        """Calls curve_fit without incrementing alpha"""
        fitted = optimize.curve_fit(self.funcOld, self.xData2, self.yData2)
        self.alpha2 = self.cround(fitted[0][0])
        aBrC = self.cround(fitted[0][0])
        mBC = self.cround(fitted[0][1])
        mBrC = self.cround(7.8*fitted[0][2]/0.4)
        list = [aBrC,mBC,mBrC]
        return list

    def cround(self, number):
        """Returns: the number rounded to 3 decimal places"""
        shift = number*10**3
        add = shift+0.5
        addint = int(add)
        addfloat = float(addint)
        shift2 = addfloat/10**3
        return shift2

    def crange(self, start, end, step):
        """Returns: list of numbers from start to end with step step"""
        a = []
        for x in range(int((end-start)/step)):
            a.append(start+step*x)
        return a