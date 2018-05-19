#Aethalometer
#Alexander Li
#2/17/17

from math import *
import numpy as np
from numpy import pi, r_
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.optimize import curve_fit 
import pylab

#Bounds for curve_fit
BOUNDS = (0, [8, 10000, 10000]) #Change as needed
BOUNDS2 = (0, [8, 90000])

#definitions
AlphaBC = 1.00
MAC_BC = 7.8
MAC_BrC = 0.4

#Fixed X parameters
T93X1 = 0.765991902834008
T93X2 = 0.565209634255129
T100X1 = 0.692307692307692
T100X2 = 0.491525423728814
T187X1 = 0.946024636058231
T187X2 = 0.872340425531915
T187X3 = 0.539007092198582
T187X4 = 0.380815001803101
T187XB = 0.684546788897957
SS_X1 = -0.0765400771223344
SS_X2 = 0 
SS_X3 = 0.627189212768148
SSXB = 0.183549711881938

#Lamdas
L1 = 370.0
L2 = 470.0
L3 = 520.0
L4 = 590.0
L5 = 660.0
L6 = 880.0
L7 = 950.0

#Sigma BCs
sigBC1 = MAC_BC*((L6/L1)**AlphaBC)
sigBC2 = MAC_BC*((L6/L2)**AlphaBC)
sigBC3 = MAC_BC*((L6/L3)**AlphaBC)
sigBC4 = MAC_BC*((L6/L4)**AlphaBC)
sigBC5 = MAC_BC*((L6/L5)**AlphaBC)
sigBC6 = MAC_BC*((L6/L6)**AlphaBC)
sigBC7 = MAC_BC*((L6/L7)**AlphaBC)
sigmaBC = [MAC_BC*((L6/L1)**AlphaBC), MAC_BC*((L6/L2)**AlphaBC), MAC_BC*((L6/L3)**AlphaBC),
           MAC_BC*((L6/L4)**AlphaBC), MAC_BC*((L6/L5)**AlphaBC), MAC_BC*((L6/L6)**AlphaBC),
           MAC_BC*((L6/L7)**AlphaBC)]


class Data(object):
    """An instance of data collectd from the Aethalometer."""

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
        
        self.BCdatalist = [BC1, BC2, BC3, BC4, BC5, BC6, BC7] #list of data for calculating variance
        self.ATN = None
        
        self.AlphaBrC = None
        self.massBC = None
        self.massBrC = None
        self.meanVariance = None #as a percent
       
        self.time = time
        self.list = None #AlphaBrC,massBC,massBrC,meanVariance
        
        self.xdata6 = np.array([1.872,1.692,1.492,1.333,1,.926]) 
        self.xWavelengths6 = np.array([470,520,590,660,880,950])
        self.ydata6 = np.array([BC2,BC3,BC4,BC5,BC6,BC7])
        
        self.xdata7 = np.array([2.378,1.872,1.692,1.492,1.333,1,.926])
        self.xWavelengths7 = np.array([370,470,520,590,660,880,950])
        self.ydata7 = np.array([BC1,BC2,BC3,BC4,BC5,BC6,BC7])
        
        self.xdataAvg7 = np.array([2.378,1.872,1.692,1.492,1.333,.962]) #Use all 7 but avg 880 and 950 u
        self.xWavelengthsAvg7 = np.array([370,470,520,590,660,915])
        self.ydataAvg7 = np.array([BC1,BC2,BC3,BC4,BC5,(BC6+BC7)/2])
        
        self.xdataAvg6 = np.array([1.872,1.692,1.492,1.333,.962]) #Use 6 but Avg 880 and 950
        self.xWavelengthsAvg6 = np.array([470,520,590,660,915])
        self.ydataAvg6 = np.array([BC2,BC3,BC4,BC5,(BC6+BC7)/2])
        
    def __str__(self):
        """Prints out the AlphaBrC, BCmass, and BrCmass after the input data has
        been analyzed as a tuple"""
        return str(("a: " + str(self.cround(self.AlphaBrC)),
                    "BC: " + str(self.cround(self.massBC)),
                    "BrC: " + str(self.cround(self.massBrC))))
                    #,"Timestamp: " + self.time))
        
    def analyze(self):
        """Performs analysis on the data. This part was copied over from the excel
        calculator.
        Stores AlphaBrC, massBC, and massBrC in the attributes"""
        T93Y1 = (self.BCdata3-self.BCdata7)/T93X1
        T93Y2 = (self.BCdata4-self.BCdata7)/T93X2
        T100Y1 = (self.BCdata3-self.BCdata6)/T100X1
        T100Y2 = (self.BCdata4-self.BCdata6)/T100X2
        T187Y1 = (self.BCdata2-self.BCdata7)/T187X1
        T187Y2 = (self.BCdata2-self.BCdata6)/T187X2
        T187Y3 = (self.BCdata2-self.BCdata5)/T187X3
        T187Y4 = (self.BCdata2-self.BCdata4)/T187X4
        T187YB = (T187Y1+T187Y2+T187Y3+T187Y4)/4
        
        SS_Y1A = (T93Y2-T93X2*(T93Y1-T93Y2)/(T93X1-T93X2))
        SS_Y2A = (T100Y2-T100X2*(T100Y1-T100Y2)/(T100X1-T100X2))
        SS_Y3A = (T187YB)-(T187XB)*((T187X1-T187XB)*(T187Y1-T187YB)+(T187X2-T187XB)*
            (T187Y2-T187YB)+(T187X3-T187XB)*(T187Y3-T187YB)+(T187X4-T187XB)*
            (T187Y4-T187YB))/((T187X1-T187XB)*(T187X1-T187XB)+(T187X2-T187XB)*
            (T187X2-T187XB)+(T187X3-T187XB)*(T187X3-T187XB)+(T187X4-T187XB)*(T187X4-T187XB))
        
        if SS_Y1A>0:
            SS_Y1 = log(SS_Y1A)
        else:
            SS_Y1 = 0
        
        if SS_Y2A>0:
            SS_Y2 = log(SS_Y2A)
        else:
            SS_Y2 = 0
            
        if SS_Y3A>0:
            SS_Y3 = log(SS_Y3A)
        else:
            SS_Y3 = 0
            
        SSYB = (SS_Y1+SS_Y2+SS_Y3)/3
        SLSL = ((SS_X1-SSXB)*(SS_Y1-SSYB)+(SS_X2-SSXB)*(SS_Y2-SSYB)+(SS_X3-SSXB)*
                (SS_Y3-SSYB))/((SS_X1-SSXB)*(SS_X1-SSXB)+(SS_X2-SSXB)*(SS_X2-SSXB)+
                (SS_X3-SSXB)*(SS_X3-SSXB))
        INTSL = SSYB-(SLSL*SSXB)
        ExpIntSL = exp(INTSL)
        BCequiv_ofBrC_ATN880 = ExpIntSL/(SLSL+1)
        #Assign attributes
        self.AlphaBrC = SLSL + 2
        self.massBC = self.BCdata6-BCequiv_ofBrC_ATN880
        self.massBrC = (ExpIntSL/(SLSL+1))*(MAC_BC/MAC_BrC)
        self.list = [self.cround(self.AlphaBrC), self.cround(self.massBC), self.cround(self.massBrC)]
    
    def variance(self):
        """Finds mean variance of the data. Copied from the excel spreadsheet"""
        #ATN BC
        ATN_BC = []
        for sigma in sigmaBC:
            ATN_BC.append((self.massBC/1000)*sigma)
        #Sigma BrCs
        sigmaBrC = [MAC_BrC*((L6/L1)**self.AlphaBrC), MAC_BrC*((L6/L2)**self.AlphaBrC),MAC_BrC*((L6/L3)**self.AlphaBrC),
            MAC_BrC*((L6/L4)**self.AlphaBrC),MAC_BrC*((L6/L5)**self.AlphaBrC),MAC_BrC*((L6/L6)**self.AlphaBrC),
            MAC_BrC*((L6/L7)**self.AlphaBrC)]
        #ATN BrC   
        ATN_BrC = []
        for sigma in sigmaBrC:
            ATN_BrC.append((self.massBrC/1000)*sigma)
        #Total ATN
        totalATN = []
        assert len(ATN_BC) == len(ATN_BrC)
        for x in range(len(ATN_BC)):
            totalATN.append(ATN_BC[x] + ATN_BrC[x])
        #BrC reported as if BC
        BrCasBC = []
        for x in range(len(ATN_BrC)):
            BrCasBC.append(1000*ATN_BrC[x]/sigmaBC[x])
        #BC + BrC reported as BC
        asBC = []
        for x in range(len(totalATN)):
            asBC.append(1000*totalATN[x]/sigmaBC[x])
        self.ATN = asBC #Total ATN
        #Mean variance
        rawVariance = []
        for x in range(1,len(asBC)):
            rawVariance.append(abs(self.BCdatalist[x]-asBC[x])/self.BCdatalist[x])
        meanVariance = sum(rawVariance)/float(len(rawVariance))
        self.meanVariance = meanVariance*100.0
        self.list.append(self.cround(self.meanVariance))
            
    def cround(self, number):
        """Returns: the number rounded to 3 decimal places"""
        shift = number*10**3
        add = shift+0.5
        addint = int(add)
        addfloat = float(addint)
        shift2 = addfloat/10**3
        return shift2

###############################################################################
    def func(self, x, a, MassBC, A):
        return A*(x**(a-1)) + MassBC
    
    def func2(self, x, a, A):
        return A*(x**(a-1))
    
    
    def curvefit6(self):
        fitted = curve_fit(self.func, self.xdata6, self.ydata6, bounds=BOUNDS)
        error= np.sqrt(np.diag(fitted[1]))
        self.AlphaBrC = self.cround(fitted[0][0])
        self.massBC = self.cround(fitted[0][1])
        self.massBrC = self.cround(7.8*fitted[0][2]/0.4)
        self.list = [self.AlphaBrC,self.massBC,self.massBrC,str(error)]
    
    def curvefit7(self):
        fitted = curve_fit(self.func, self.xdata7, self.ydata7,bounds=BOUNDS)
        error= np.sqrt(np.diag(fitted[1]))
        self.AlphaBrC = self.cround(fitted[0][0])
        self.massBC = self.cround(fitted[0][1])
        self.massBrC = self.cround(7.8*fitted[0][2]/0.4)
        self.list = [self.AlphaBrC,self.massBC,self.massBrC,str(error)]
        
    def curvefitAvg7(self):
        fitted = curve_fit(self.func, self.xdataAvg7, self.ydataAvg7,bounds=BOUNDS)
        error= np.sqrt(np.diag(fitted[1]))
        self.AlphaBrC = self.cround(fitted[0][0])
        self.massBC = self.cround(fitted[0][1])
        self.massBrC = self.cround(7.8*fitted[0][2]/0.4)
        self.list = [self.AlphaBrC,self.massBC,self.massBrC,str(error)]
        
    def curvefitAvg6(self):
        fitted = curve_fit(self.func, self.xdataAvg6, self.ydataAvg6,bounds=BOUNDS)
        error= np.sqrt(np.diag(fitted[1]))
        self.AlphaBrC = self.cround(fitted[0][0])
        self.massBC = self.cround(fitted[0][1])
        self.massBrC = self.cround(7.8*fitted[0][2]/0.4)
        self.list = [self.AlphaBrC,self.massBC,self.massBrC,str(error)]
        
    def curvefitWS(self):
        fitted = curve_fit(self.func2, self.xdataAvg7, self.ydataAvg7, bounds=BOUNDS2)
        error = np.sqrt(np.diag(fitted[1]))
        self.AlphaBrC = self.cround(fitted[0][0])
        self.massBC = 0
        self.massBrC = self.cround(fitted[0][1]/0.4)
        self.list = [self.AlphaBrC,self.massBC,self.massBrC,str(error)]