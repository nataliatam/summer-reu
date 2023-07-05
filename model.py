import random
import math
import matplotlib.pyplot as plt

first = 50
second = 70
third = 40
fourth = 65

wlR = 4

Lx = []
Ly = []
wirelessX = []
wirelessY = []
finalLeavesX = [] 
finalLeavesY = [] 
finalLeaves = []
numUEs = 20
sharingUEs = 0
numWireless = 0


def findShared(xlower, xupper, ylower, yupper):
    global sharingUEs, numWireless
    quadrantX = []
    quadrantY = []

    # Adds all UEs in quadrant into temporary list
    for i in range(len(Lx)):
        if xlower<= Lx[i] <= xupper and ylower <= Ly[i] <= yupper:
            quadrantX.append(Lx[i])
            quadrantY.append(Ly[i])

    # Puts a wireless cell in between 2 UEs if possible
    for i in range(len(quadrantX)):
        accountedFor = False
        j = i+1
        for j in range(len(quadrantX)):
            if len(quadrantX) == 1:
                Wireless = plt.Circle((quadrantX[i], quadrantY[i]), wlR, fill = False) 
                axes.add_artist(Wireless)
                numWireless += 1
            elif j != i:
                p = [quadrantX[i], quadrantY[i]]
                q = [quadrantX[j], quadrantY[j]]
                if math.dist(p, q) <= 2*wlR:
                    accountedFor = True
                    averageX = (quadrantX[i] + quadrantX[j])/2
                    averageY = (quadrantY[i]+ quadrantY[j])/2

                    addNewWireless(averageX, averageY)
                    finalLeaves.append((averageX, averageY))
                    sharingUEs += 1
            

        # Puts wireless cell around UEs that have no others in range
        if not accountedFor:
                newCell = plt.Circle((quadrantX[i], quadrantY[i]), wlR, fill = False) 
                axes.add_artist(newCell)

                finalLeaves.append((quadrantX[i], quadrantY[i]))
                wirelessX.append(quadrantX[i])
                wirelessY.append(quadrantY[i])
                numWireless += 1
            
    quadrantX.clear()
    quadrantY.clear()

# Helper method to draw wireless cell's range at a point
def addNewWireless(x, y):
    global numWireless
    center = plt.Circle((x, y), 1,  color = 'r')
    axes.add_artist(center)

    newCell = plt.Circle((x, y), wlR, fill = False) 
    axes.add_artist(newCell)

    wirelessX.append(x)
    wirelessY.append(y)
    numWireless += 1




# Helper method to return the nearest point on the "fibre"
def nearestAxis(x, y):
    min = abs(x-first)
    minx = first
    miny = y
    if abs(x-second) < min: 
        min = abs(x-second)
        minx = second
    if abs(y-third) < min: 
        min = abs(y-third)
        minx = x
        miny = third
    if abs(y-fourth) < min: 
        min = abs(y-fourth)
        minx = x
        miny = fourth
    return [minx, miny]


# Creates a line of Wireless cells to the nearest point on the "fibre" 
# for all existing wireless cells
def makeWirelessPath():
    for i in range(len(finalLeaves)):
        min = nearestAxis(finalLeaves[i][0], finalLeaves[i][1])
        if (min[0] == finalLeaves[i][0]):
            if(min[1] >= finalLeaves[i][1]): 
                newY = finalLeaves[i][1]+ wlR
                while newY < min[1]:
                    addNewWireless(finalLeaves[i][0], newY)
                    newY += wlR
            else:
                newY = finalLeaves[i][1] - wlR
                while newY > min[1]:
                    addNewWireless(finalLeaves[i][0], newY)
                    newY -= wlR
        else:
            if(min[0] >= finalLeaves[i][0]): 
                newX = finalLeaves[i][0] + wlR
                while newX < min[0]:
                    addNewWireless(newX, finalLeaves[i][1])
                    newX += wlR
            else:
                newX = finalLeaves[i][0] - wlR
                while newX > min[0]:
                    addNewWireless(newX, finalLeaves[i][1])
                    newX -= wlR


def removeRedundant(xlower, xupper, ylower, yupper):
    global sharingUEs, numWireless
    quadrantX = []
    quadrantY = []
    quadrant = []

    # Puts all wireless cell coordinates into temporary lists
    for i in range(len(wirelessX)):
        if xlower<= wirelessX[i] <= xupper and ylower <= wirelessY[i] <= yupper:
            if quadrant.count([wirelessX[i], wirelessY[i]]) > 0:
                break
            else:
                quadrantX.append(wirelessX[i])
                quadrantY.append(wirelessY[i])
                quadrant.append([wirelessX[i], wirelessY[i]])
   
    
    for i in range(len(quadrantX)- 1):
        accountedFor = False
        pX = 0
        pY = 0 
        qX = 0
        qY = 0
        
        mindist = 100
        j = i + 1
        while j < len(quadrantX):
            p = [quadrantX[i], quadrantY[i]]
            # Finds closest pair p and q within certain distances
            if math.dist(p, nearestAxis(quadrantX[i], quadrantY[i])) > 0*wlR:
                q = [quadrantX[j], quadrantY[j]]
                distpq = math.dist(p, q)
                if distpq <= 8*wlR and distpq <= mindist and p != q: 
                    mindist = distpq
                    pX = quadrantX[i] 
                    pY = quadrantY[i] 
                    qX = quadrantX[j] 
                    qY = quadrantY[j] 
                    accountedFor = True
            j += 1

        # If an acceptable close point found, add cell between them
        if accountedFor:
            averageX = (pX + qX)/2
            averageY = (pY+ qY)/2

            center = plt.Circle((averageX, averageY), 1,  color = 'purple', fill = False)
            axes.add_artist(center)

            newCell = plt.Circle((averageX, averageY), wlR, fill = False) 
            axes.add_artist(newCell)
            numWireless += 1
            sharingUEs += 1

            # Process to remove the further of 2 cells from final paths
            dist = []
            dist.append(math.dist((pX, pY), nearestAxis(pX, pY)))
            dist.append(math.dist((qX, qY), nearestAxis(qX, qY)))
            minpos = dist.index(min(dist))
            
            if minpos == 0:
                x = pX
                y = pY
                '''print(minpos)
                print("Q:", (qX, qY))
                print(finalLeaves)'''
                if (qX, qY) in finalLeaves:
                    for i in range(finalLeaves.count((qX, qY))):
                        finalLeaves.remove((qX, qY))
                        #print("removed", (qX, qY))
            else: 
                x = qX
                y = qY
                '''print(minpos)
                print("P:", (pX, pY))
                print(finalLeaves)'''
                if (pX, pY) in finalLeaves:
                    for i in range(finalLeaves.count((pX, pY))):
                        finalLeaves.remove((pX, pY))
                        #print("removed", (pX, pY))

            center = plt.Circle((x, y), 1,  color = 'purple', fill = False)
            axes.add_artist(center)

            newCell = plt.Circle((x, y), wlR, fill = False) 
            axes.add_artist(newCell)

        


figure, axes = plt.subplots()
for x in range(numUEs):
    a = random.randint(1, 99)
    Lx.append(a)
    b = random.randint(1, 99)
    Ly.append(b)
    Drawing_colored_circle = plt.Circle((a,b), 1)
    axes.add_artist(Drawing_colored_circle)

 
plt.plot([first, first], [0,100], 'g', linewidth=3, markersize=5)
plt.plot([second,second], [0,100], 'g', linewidth=3, markersize=5)
plt.plot([0,100], [third,third], 'g', linewidth=3, markersize=5)
plt.plot([0,100], [fourth,fourth], 'g', linewidth=3, markersize=5)
Wired = plt.Circle((20, 40), 3, fill = False) 

findShared(0, first, fourth, 100)
removeRedundant(0, first, fourth, 100)

findShared(first, second, fourth, 100)
removeRedundant(first, second, fourth, 100)

findShared(second, 100, fourth, 100)
removeRedundant(second, 100, fourth, 100)


findShared(0, first, third, fourth)
removeRedundant(0, first, third, fourth)


findShared(first, second, third, fourth)
removeRedundant(first, second, third, fourth)

findShared(second, 100, third, fourth)
removeRedundant(second, 100, third, fourth)

findShared(0, first, 0, third)
removeRedundant(0, first, 0, third)

findShared(first, second, 0, third)
removeRedundant(first, second, 0, third)

findShared(second, 100, 0, third)
removeRedundant(second, 100, 0, third)
print(finalLeaves)

makeWirelessPath()

print("---------------------------------------------------------------")
print("Metrics:")
print("Number of UEs:", numUEs)
print("Number of Cells: ", numWireless)
print("Number of UEs sharing a path: ", sharingUEs)
area = numWireless * wlR * wlR * math.pi
print("Area Coverage: ", area)
print("Fractional Area Coverage: ", (area)/ (100 * 100))




axes.set_aspect('1')

plt.xlim(0, 100)
plt.ylim(0, 100)
plt.title( 'Cell Towers' )
plt.show()
