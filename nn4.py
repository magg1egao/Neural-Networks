import sys; args=sys.argv[1:]
parseList = open(args[0],'r').read().splitlines()
import random, math, re

weightsInd = {}
propWeightsLengthsInd=[]
iter=0
for p in parseList:
    temp = re.findall(r'-?\d*\.?\d+',p)
    if temp:
        temp2 = [float(t) for t in temp]
        weightsInd[iter] = temp2
        propWeightsLengthsInd.append(len(temp2))
        iter+=1

inputtxt = args[1]
decipher = inputtxt[7:9]
if decipher=="<=": 
    inequality = "<="
    rSquared = float(inputtxt[9:])
elif decipher==">=": 
    inequality = ">="
    rSquared = float(inputtxt[9:])
elif decipher[0]==">": 
    inequality = ">"
    rSquared = float(inputtxt[8:])
else: 
    inequality = "<"
    rSquared = float(inputtxt[8:])

nodesInd = {i:[] for i in range(len(weightsInd)+1)}
propNodeLengthsInd = [2]

for w in propWeightsLengthsInd:
    propNodeLengthsInd.append(w//propNodeLengthsInd[-1])

propNodeLengthsTot = [3]
for l in propNodeLengthsInd[1:-1]:
    propNodeLengthsTot.append(2*l)
propNodeLengthsTot.extend([1,1])


def func(num):return 1/(1+math.exp(-num))
def derivative(num):return num*(1-num)

weightTot = {i:[] for i in range(len(propNodeLengthsTot)-1)}

initialWeights = weightsInd[0]
temp3 = []
for i in range(0,len(initialWeights),2):
    curr =initialWeights[i:i+2]
    temp3.extend([curr[0],0,curr[1]])
for i in range(0,len(initialWeights),2):
    curr =initialWeights[i:i+2]
    temp3.extend([0,curr[0],curr[1]])
weightTot[0]=temp3

for i in range(1,len(weightTot)-2):
    currWeights = weightsInd[i]
    length = len(currWeights)
    currNodeLength = propNodeLengthsInd[i]
    nextNodeLength = propNodeLengthsInd[i+1]
    temp4 = []
    for j in range(0,length,currNodeLength):
        temp4.extend(currWeights[j:j+currNodeLength]+[0]*currNodeLength)
    for k in range(0,length,currNodeLength):
        temp4.extend([0]*currNodeLength+currWeights[k:k+currNodeLength])
    weightTot[i] = temp4

weightTot[len(weightTot)-2] = weightsInd[len(weightsInd)-1]*2
if inequality[0] == "<":
    weightTot[len(weightTot)-1] = [(1+math.e)/2]
else: weightTot[len(weightTot)-1] = [(1+math.e)/(2*math.e)]

change = weightTot[len(weightTot)-2]
new = []
if inequality[0] == "<":
    for c in change:
        new.append(-c/rSquared)
else:
    for c in change:
        new.append(c/rSquared)
weightTot[len(weightTot)-2] = new

def printWeights(weights):
    toprint=""
    for i in weights:
        for j in weights[i]: 
            toprint+= str(j)+" "
        toprint+="\n"
    print(toprint)

x=""
for k in propNodeLengthsTot: x+= str(k)+" "
print("Layer counts "+x)
printWeights(weightTot)

#Maggie Gao, pd 6, 2023