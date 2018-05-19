#peakFinder
#Alexander Li
#7/6/17

from math import *
import numpy as np
from sklearn import linear_model
from sklearn.metrics import r2_score
from scipy import stats
import matplotlib.pyplot as plt

class PeakFinder():
    """An instance of PeakFinder will locate spikes in the data, making sure that
    the PM2.5 and DC data both spike. It can also correlate PM data with DC data
    to make sure peaks are caused by woodsmoke."""
    
    def __init__(self):
        """Initializes PeakFinder"""
        
        #for linear regression
        self.regressionScore = None
        self.regressionShift = 0
        
        #for locateSinglePeak
        self.maxFound = 0
        self.maxDiffFound = 0
        self.dipsBelowHalf = 0 #number of times DC dips below half the max. More than 1 indicates 2 peaks
        
        #for inflection points
        self.inflections = 0
        
        self.list = None
        self.peakFound = False
        
    def differenceFinder(self, startIndex, endIndex, list):
        """Given a range within a list with start startIndex, and end endIndex,
        determine if the data peaked near the vicinity of that range. Looks 20 indices
        before and after, and finds the max difference between a found value and the
        value at the index. If the max difference is above a certain threshold, then a
        peak was found"""
        maxDiff = 0
        start = list[startIndex]
        end = list[endIndex]
        for x in range(20):
            diffBefore = abs(list[startIndex] - list[startIndex-x])
            if diffBefore > maxDiff:
                maxDiff = diffBefore
            diffAfter = abs(list[endIndex] - list[endIndex+x])
            if diffAfter > maxDiff:
                maxDiff = diffAfter
        temp = endIndex
        if list[startIndex] < list[endIndex]: #Compare middle with smaller start or end index
            temp = startIndex
        for x in range(startIndex, endIndex):
            diff = abs(list[x] - list[temp])
            if diff > maxDiff:
                maxDiff = diff
        return maxDiff
    
    def rangeFinder(self, startIndex, endIndex, list):
        """Given a startIndex, and end endIndex, determine the max range within the
        data, i.e. find the MAX-MIN between the start and end index"""
        max = list[startIndex]
        min = list[startIndex]
        for x in range(startIndex, endIndex):
            if list[x] > max:
                max = list[x]
            if list[x] < min:
                min = list[x]
        return max-min
    
    def locateSinglePeak(self, start, end, list):
        """Given bigGroupsList, identify if there are any single peaks inside of a
        bigGroup range"""
        for x in range(start,end):
            currentVal = list[x]
            if currentVal > self.maxFound:
                self.maxFound = currentVal
            diff = self.maxFound - currentVal
            if diff > self.maxDiffFound:
                self.maxDiffFound = diff
            if diff > self.maxFound/2:
                self.dipsBelowHalf += 1
    
    def locateInflectionPoint(self, start, end, list):
        """Given bigGroupsList, identify any upwards inflection points within the range,
        which signifies that there are 2 peaks in the group"""
        if end-start > 10:
            for x in range(start+5, end-5):
                if (list[x] < list[x-1] and list[x] < list[x-2] and list[x] < list[x-3]
                    and #list[x] < list[x-4] and list[x] < list[x-5] and
                    list[x] < list[x+1] and list[x] < list[x+2] and list[x] < list[x+3]):
                    #and list[x] < list[x+4] and list[x] < list[x+5]):
                    self.inflections += 1
  
    def performLinearRegression(self, start, end, dClist, pMlist, shift):
        """performs linear regression on the DC and PM data to see if there is any
        correlation between the 2"""
        
        indices = range(start,end)
        yData = pMlist[start:end] 
        xData = dClist[(start+shift):(end+shift)]
        new = []
        for x in xData:
            new.append([x])
        xData = new
        yData = np.array(yData)
        regr = linear_model.LinearRegression()
        regr.fit(xData, yData)
        score = regr.score(xData, yData)
        variance = np.mean((regr.predict(xData) - yData) ** 2)/1000000
        self.regressionScore = score
        #MAKE SURE YOU CHECK GRAPHS OCCASIONALLY
        """
        fig, ax1 = plt.subplots()
        ax1.plot(indices, xData, 'b-')
        ax1.set_xlabel('indices(s)')
        ax1.set_ylabel('DC', color='b')
        ax1.tick_params('y', colors='b')
        
        ax2 = ax1.twinx()
        ax2.plot(indices, yData, 'r-')
        ax2.set_ylabel('PM', color='r')
        ax2.tick_params('y', colors='r')
       
        #plt.plot(indices, xData, color='black')
        #plt.plot(indices, yData, color='blue')

        #plt.xticks(())
        #plt.yticks(())

        fig.tight_layout()
        plt.show()
        """
    
            
        
        
        
        
            
            
            
            