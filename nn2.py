import sys; args=sys.argv[1:]
inputOutputTxt = open(args[0],'r').read().splitlines()
import math
import random
inputs,outputs = [],[] 
for line in inputOutputTxt:
    split = line.split(" ")
    for i in range(len(split)):
        if split[i]=="=>": 
            arrow = i
            break

    split1 = [int(s) for s in split[0:arrow]]
    inputs.append(split1) #inputs is a list of lists
    split2 = [int(s) for s in split[arrow+1:]]
    outputs.append(split2) # j a list of integers


propNodeLengths = [len(inputs[0])+1,3,len(outputs[0]),len(outputs[0])] #4,3,2,2, ex
#if len(outputs[0])==2: propNodeLengths=[4,3,2,2]
nodes = {i:[] for i in range(len(propNodeLengths))} #0,1...

weights = {i:[] for i in range(len(propNodeLengths)-1)} #0,1,...
for i in range(len(weights)-1): #random weights
    for r in range(propNodeLengths[i]*propNodeLengths[i+1]): weights[i].append(random.random())
for i in range(propNodeLengths[-1]): weights[len(weights)-1].append(random.random())


def func(num):
    return 1/(1+math.exp(-num))
def derivative(num):
    return num*(1-num)
    #return math.exp(-num)/((1+math.exp(-num))**2)
def dotProduct(vector1, vector2):
    toret = []
    for i in range(len(vector1)):
        toret.append(vector1[i]*vector2[i])
    return toret

def feedForward(input): #input will be a list
    nodes[0] = input+[1]
    for t in range(1,len(nodes)):
        nodes[t] = []
    for i in range(1,len(weights)): #i is which node working on now
        prevNodes = nodes[i-1]
        prevWeights = weights[i-1]
        for j in range(0,len(prevWeights),len(prevNodes)): #iterating thru weights by # each node needs
            tempCount = 0.00
            tempIndicate = 0
            for k in range(j,j+len(prevNodes)): #iterating through the weights needed for the node
                tempCount=tempCount+prevWeights[k]*prevNodes[tempIndicate]
                tempIndicate+=1
            
            nodes[i].append(func(tempCount))

    lastWeights = weights[len(weights)-1]
    secondLastNodes = nodes[len(nodes)-2]
    for x in range(len(lastWeights)):
        app = lastWeights[x]*secondLastNodes[x]
        if app == -0.0:
            nodes[len(nodes)-1].append(0.0)
        else: nodes[len(nodes)-1].append(app)


def printWeights(weights):
    toprint=""
    for i in weights:
        for j in weights[i]: 
            toprint+= str(j)+" "
        toprint+="\n"
    print(toprint)
#printWeights(weights)

count = 0
numOfInputs = len(inputs)


while True:
    if count%1000==0: 
        x=""
        for k in propNodeLengths: x+= str(k)+" "
        print("Layer counts "+x)
        printWeights(weights)

    
    #print(weights)
    indicate = count%numOfInputs
    feedForward(inputs[indicate])
    #if count%999==0 or count==0: print(weights) 
    #print(nodes)
    error = {i:[] for i in range(0,len(nodes))} #on paper output and last node are different, not here

    for i in range(len(nodes[len(nodes)-2])): #second to last node error
        propOutput = outputs[indicate][i]
        xVal = nodes[len(nodes)-2][i]
        weightFinal = weights[len(nodes)-2][i]
        #print("xVal")
        #print(xVal)
        deriv = derivative(xVal) #E final
        #print("deriv")
        #print(deriv)
        error[len(nodes)-2].append((propOutput-(xVal*weightFinal))*weightFinal*deriv)

    for i in reversed(range(1,len(nodes)-2)): #thru node layers backwards
        nextError = error[i+1]
        currweights = weights[i]
        #print("nextnode")
        #print(nextNode)
        #print("currweights")
        #print(currweights)
        jump = len(currweights)/len(nextError)
        for j in range(len(nodes[i])): #thru each node in that layer
            #print(j)
            xVal = nodes[i][j]
            #print(xVal)
            deriv = derivative(xVal)
            wE = 0
            
            for n in range(len(nextError)): #iter thru next layer nodes
                #print("nextNode[n]")
                #print(nextError[n])
                #print("currweights[int(j+(n*jump))]")
                #print(currweights[int(j+(n*jump))])
                wE += (nextError[n] * currweights[int(j+(n*jump))])

            error[i].append(wE*deriv)

    #print("error")
    #print(error)
    #partial
    partials = {l:[] for l in range(3)}
    #final layer partial
    for k in range(len(weights[len(weights)-1])): #for how many weights there r
        propOutput = outputs[indicate][k]
        xVal = nodes[len(weights)-1][k]
        weightFinal = weights[len(weights)-1][k]
        partials[len(partials)-1].append((propOutput-(xVal*weightFinal))*xVal)
    #print("nodes")
    #print(nodes)
    #print(weights)

    #other layers
    for i in range(len(weights)-1):
        #currweights = weights[i]
        currNodes = nodes[i]
        #nextNodes = nodes[i+1]
        nextError = error[i+1]
        #print(currweights)
        #print(currNodes)
        #print(nextNodes)
        iter = len(currNodes)
        #print(iter)
        for j in range(len(weights[i])):
            xVal = currNodes[j%iter]
            eNextVal = nextError[j//iter]

            partials[i].append(xVal*eNextVal)

    #print(partials)
    #update weights
    #print(error)
    #print(weights)
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            weights[i][j]+= partials[i][j]*0.1

    #print(nodes)
    #print(weights)
    #print(partials)

    #print(error)
    count+=1

#Maggie Gao, pd 6, 2023
