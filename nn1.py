import sys; args=sys.argv[1:]
weightsText = open(args[0],'r').read().splitlines()
print(weightsText)
import math

weights = {}
temp = 1
for line in weightsText:
    weights[temp] = [float(n) for n in line.split(" ")]
    temp+=1
print(weights)
transferfunc = args[1]

nodes = {i:[] for i in range(len(weights)+1)}
length = len(args)
for i in range(2,length):
    nodes[0].append(float(args[i]))
print(nodes)

def func(num):
    if transferfunc == "T1":return num
    if transferfunc=="T2": return num if num>0 else 0
    if transferfunc=="T3": return 1/(1+math.exp(-num))
    if transferfunc=="T4": return (2/(1+math.exp(-num)))-1

for i in range(1,len(weights)): #i is which node working on now
    prevNodes = nodes[i-1]
    currentWeights = weights[i]
    rightLength = len(currentWeights)//len(prevNodes)
    
    for j in range(0,len(currentWeights),len(prevNodes)):
        tempCount = 0.00
        tempIndicate = 0
        for k in range(j,j+len(prevNodes)):
            #print(prevNodes[tempIndicate])
            tempCount=tempCount+currentWeights[k]*prevNodes[tempIndicate]
            tempIndicate+=1
        
        nodes[i].append(float(str(func(tempCount))[0:7]))
        print(nodes)

lastWeights = weights[len(weights)]
print(lastWeights)
secondLastNodes = nodes[len(nodes)-2]
print(secondLastNodes)
for x in range(len(lastWeights)):
    app = float(str(lastWeights[x]*secondLastNodes[x])[0:7])
    if app == -0.0:
        nodes[len(nodes)-1].append(0.0)
    else: nodes[len(nodes)-1].append(app)

ans = ""
for x in nodes[len(nodes)-1]:
    ans += str(x) + " "
print(ans)

#Maggie Gao, pd 6, 2023