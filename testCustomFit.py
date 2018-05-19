#testCustomFit
#Alexander Li
#5/16/17

from customFit2 import *
import matplotlib.pyplot as plt
import scipy.optimize as optimize

def testCustomFit():
    """Tests curve fit"""
    a = Data(9640,6539,5299,4291,3577,2796,2754)
    print a.curveFit1()
    print a.curveFitOld()
    print a.curveFit(a.alpha)
    plt.plot(a.xData2, a.yData2, 'b-', label='data')
    popt, pcov = optimize.curve_fit(a.func, a.xData2, a.yData2)
    plt.plot(a.xData2, a.func(a.xData2, *popt), 'r-', label='fit')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()


testCustomFit()