#groupFinder
#Alexander Li
#7/6/17

class GroupFinder():
    """Finds groups of peaks in the DC data, creates groups of elevated DC"""
    
    def __init__(self, dCList):
        """initializes GroupFinder"""
        
        self.dCList = dCList
        self.elevatedDC = []
        self.durationList = [] #duration of found peaks
        
    def findElevatedDC(self, threshold):
        mini = []
        for index in range(len(self.dCList)):
            if self.dCList[index] > threshold:
                mini.append(index)
            else:
                mini.append(index)
                if len(mini) > 5:
                    new = self.condenseList(mini)
                    self.elevatedDC.append(new)
                    self.durationList.append(new[1]-new[0])
                    mini = []
                else:
                    mini = []
    
    
    def segmentDC(self, threshold):
        mini = []
        for index in range(len(self.dCList)):
            if self.dCList[index] > threshold and len(mini) < 5: #change to change side of segment
                mini.append(index)
            else:
                mini.append(index)
                if len(mini) >= 5: #change here too
                    new = self.condenseList(mini)
                    self.elevatedDC.append(new)
                    self.durationList.append(new[1]-new[0])
                    mini = []
                else:
                    mini = []
    
           
    def condenseList(self, list):
        """condense an ordered list so it only consists of first and last element"""
        result = []
        result.append(list[0])
        result.append(list[-1])
        return result