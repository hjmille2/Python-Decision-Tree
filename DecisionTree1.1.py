from math import log2
# a 2nd try on the decision trees

##get input 

print("Format: each object per line with the final column being the decision. The labels of each attribute should be the first row")
fileName = input("Please enter the file you'd like to read from that follows the above format: ")


try:
    inFile = open(fileName, "r")
    dataTemp = inFile.read().split("\n")
    inFile.close()
except FileNotFoundError:
    print("File was not found")
    raise

data = []

#split the data to be indiv objects per each object 
for s in dataTemp:
    st = s.split(" ")
    data.append(st)
    
#print(data)
#remove the labels from the data
label = data[0]
data.pop(0)

posAttr = data[0][-1]
#print(posAttr)
#worked as expected
#print(label)
#print(data)
 
 

#returns a dictionary with the total number of objects stored in the 
#first index the rest contain the end result and the number of outcomes
#based on the deciding attribute
#for example: {"total":5, "green":{"apple":1}, "yellow":{"apple":1, "lemon":1} ... } 
def getNumRes(inData, decidingAttr):
    totals = {}
    totals["total"] = 0
    index = label.index(decidingAttr)
    for d in inData:
        #print(d)
        attribute = d[index]
        decision = d[-1]
        
        if attribute not in totals:
            decTotal = {}
            decTotal[decision] = 1
            totals[attribute] = decTotal
        else:
            decTotal = totals[attribute]
            if decision not in decTotal:
                decTotal[decision] = 1
            else:
                decTotal[decision] += 1
            
            totals[attribute] = decTotal 
        totals["total"] += 1
    return totals
       
                
#testing to see if the dictionary with a dictionary worked as intended   
#print(getNumRes(data, "pat"))       
        
        
#definition of entropy is in the artificial intelligence book ed 3 pg 704
def calcEntropy(inData):
    tot = 0
    for d in inData:
        num = inData[d] / calcTotal(inData)
        if num != 0:
            tot += num * log2(num)
        else:
            tot += 0
    tot *= -1
    return tot

def calcTotal(inDict):
    tot = 0
    for d in inDict:
        tot += inDict[d]
        
    return tot

#gets the total number of results for the data passed in      
def getRes(inData):
    resList = {}
    for d in inData:
        if d[-1] not in resList:
            resList[d[-1]] = 1
        else:
            resList[d[-1]] += 1
    return resList

def calcInfoGain(inData, decidingAttr):
    totals = getNumRes(inData, decidingAttr)
    
    tot = 0
    
    for t in totals:
        if t == "total":
            continue
        tot += calcTotal(totals[t]) / totals["total"] * calcEntropy(totals[t])
    
    d = getRes(inData)
    gain = calcEntropy(d) - tot
    return round(gain, 3)
     

def findBestAttribute(inData):
    bestGain = 0
    bestAttr = ""
    num = len(label)-1
    for l in range(num):
        
        newGain = calcInfoGain(inData, label[l])
        if newGain > bestGain:
            bestGain = newGain
            bestAttr = label[l] 
     
    return bestGain, bestAttr
    
    
    
#working as intended  
#print(calcInfoGain(data, "type") )
 
#this is passed the attribute index and the desired attribute being looked for
#for example: 4, "some"gives all of the data that matches that there are some
#patrons for the restdata.txt example set 
def getListFromAttr(attrIndex, attr, inData):
    outData = inData.copy()
    retList = []
    for d in outData[:]:
        if d[attrIndex] == attr:
            retList.append(d)
            outData.remove(d)
    return retList, outData
#print(getListFromAttr(4, "some"))
  
#goes through a parts the data based on whether it splits evenly or not
#those that do not end up in a category that splits evenly, ends up under
#the unsorted key 
def partitionData(inData, attr):
    workingData = inData.copy()
    dataParts = {} #going to be a dict because there may be multiples
    attributeIndex = label.index(attr) 
    dataResults = getNumRes(inData, attr) 
    
    for d in dataResults:
        if d == "total":
            continue
        if len(dataResults[d]) == 1:
            resList, workingData = getListFromAttr(attributeIndex, d, workingData)
            dataParts[d] = resList
            
    dataParts["unsorted"] = workingData
        
    return dataParts 

class Node:
    def __init__(self, attribute, branches, dataPart):
        self.attribute = attribute
        self.branches = branches
        self.dataPart = dataPart
        
class Leaf:
    def __init__(self, inData):
        self.predictions = getRes(inData)


def buildTree(inData):
    
    gain, attr = findBestAttribute(inData)
    
    if gain == 0:
        return Leaf(inData)
        
    partData = partitionData(inData, attr)
    
    branches = []
    for p in partData:
        branches.append(buildTree(partData[p]))
        
    return Node(attr, branches, partData)

def printTree(node, space=""):
    if isinstance(node, Leaf):
        print(space + "Predict", node.predictions)
        return
    print(space + str(node.attribute))
    
    i = 0
    for d in node.dataPart:
        print(space + "    -" + d)
        printTree(node.branches[i], space + "           ")
        i+=1
        


printTree(buildTree(data))







