import sys; args=sys.argv[1:]
import random, math

inputtxt = args[0]
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

nodes = {i:[] for i in range(5)}
propNodeLengths = [3,3,2,1,1]

weights = {i:[] for i in range(len(propNodeLengths)-1)} #0,1,...
for i in range(len(weights)-1): #random weights
    for r in range(propNodeLengths[i]*propNodeLengths[i+1]): weights[i].append(random.random())
for i in range(propNodeLengths[-1]): weights[len(weights)-1].append(random.random())

def func(num):return 1/(1+math.exp(-num))
def derivative(num):return num*(1-num)

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

def inputFunc(num):
    if inequality=="<":
        return True if num<rSquared else False
    if inequality==">":
        return True if num>rSquared else False
    if inequality=="<=":
        return True if num<=rSquared else False
    if inequality==">=":
        return True if num>=rSquared else False        

count=0
nodesLength = len(nodes)
while True:
    if count%100000==0: 
        x=""
        for k in propNodeLengths: x+= str(k)+" "
        print("Layer counts "+x)
        printWeights(weights)

    x,y = random.uniform(-1.5, 1.5),random.uniform(-1.5, 1.5)

    feedForward([x,y])
    output = nodes[nodesLength-1][0]
    
    inequalityResult = inputFunc(x**2+y**2)

    if (inequalityResult and output<0.5) or (not inequalityResult and output>=0.5):
        if inequalityResult: propOutput=0.85
        else: propOutput=0.15
        error = {i:[] for i in range(0,nodesLength)} #on paper output and last node are different, not here

        for i in range(len(nodes[nodesLength-2])): #second to last node error
            xVal = nodes[nodesLength-2][i]
            weightFinal = weights[nodesLength-2][i]
            deriv = derivative(xVal) #E final
            error[nodesLength-2].append((propOutput-(xVal*weightFinal))*weightFinal*deriv)

        for i in reversed(range(1,nodesLength-2)): #thru node layers backwards
            nextError = error[i+1]
            currweights = weights[i]
            jump = len(currweights)/len(nextError)
            for j in range(len(nodes[i])): #thru each node in that layer
                xVal = nodes[i][j]
                deriv = derivative(xVal)
                wE = 0
                
                for n in range(len(nextError)): #iter thru next layer nodes
                    wE += (nextError[n] * currweights[int(j+(n*jump))])

                error[i].append(wE*deriv)

        partials = {l:[] for l in range(len(weights))}
        #final layer partial
        for k in range(len(weights[len(weights)-1])): #for how many weights there r
            xVal = nodes[len(weights)-1][k]
            weightFinal = weights[len(weights)-1][k]
            partials[len(partials)-1].append((propOutput-(xVal*weightFinal))*xVal)

        #other layers
        for i in range(len(weights)-1):
            currNodes = nodes[i]
            nextError = error[i+1]

            iter = len(currNodes)
            for j in range(len(weights[i])):
                xVal = currNodes[j%iter]
                eNextVal = nextError[j//iter]

                partials[i].append(xVal*eNextVal)

        for i in range(len(weights)):
            for j in range(len(weights[i])):
                weights[i][j]+= partials[i][j]*0.1
    count+=1

#Maggie Gao, pd 6, 2023