import random
import math
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, MultiPoint
from shapely.ops import nearest_points as np

first = 50
second = 70
third = 40
fourth = 65
wlR = 4
numUEs = 35
sharingUEs = 0
numWireless = 0

UEList = []
WirelessList = []
finalLeaves = []

'''------------------------------------------------------------------'''
class WirelessCell:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type # types: SHARED/BLUE, PATH, NONE, PURPLE

class UE:
    def __init__(self, x, y, sharing):
        self.x = x
        self.y = y
        self.sharing = False

'''------------------------------------------------------------------

# Helper function adding all points inside a polygon to a working list
def tempListInPolygon(corners[]){
    for i in range(len(WirelessList)):
            if xlower<= WirelessList[i].x <= xupper and ylower <= WirelessList[i].y <= yupper:
                tempquadrant.append(WirelessList[i])
        
        tempquadrant = [*set(tempquadrant)]
}

------------------------------------------------------------------'''

def addWireless(x, y, type):
    temp = WirelessCell(x, y, type)
    WirelessList.append(temp)

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

# Helper method to return the nearest point on the "fibre"
def nearestPoint(x, y):
    p = (x, y)
    math.dist(p, )
   


def drawCells():
    for i in range(len(WirelessList)):
        if (WirelessList[i].type == "SHARED" or WirelessList[i].type == "RED"):
            center = plt.Circle((WirelessList[i].x, WirelessList[i].y), 1, color = 'sandybrown')
            axes.add_artist(center)
            newCell = plt.Circle((WirelessList[i].x, WirelessList[i].y), wlR, fill = False) 
            axes.add_artist(newCell)
        elif(WirelessList[i].type == "PATH"):
            center = plt.Circle((WirelessList[i].x, WirelessList[i].y), 1, color = 'lightcoral')
            axes.add_artist(center)
            newCell = plt.Circle((WirelessList[i].x, WirelessList[i].y), wlR, fill = False) 
            axes.add_artist(newCell)
        elif (WirelessList[i].type == "NONE"):
            newCell = plt.Circle((WirelessList[i].x, WirelessList[i].y), wlR, fill = False) 
            axes.add_artist(newCell)
        elif (WirelessList[i].type == "PURPLE"):
            center = plt.Circle((WirelessList[i].x, WirelessList[i].y), 1,  color = 'purple', fill = False)
            axes.add_artist(center)
            newCell = plt.Circle((WirelessList[i].x, WirelessList[i].y), wlR, fill = False) 
            axes.add_artist(newCell)


'''------------------------------------------------------------------'''

def findShared(xlower, xupper, ylower, yupper):
    global sharingUEs
    tempquadrant = []

    # Adds all UEs in quadrant into temporary list
    for i in range(len(UEList)):
        if xlower<= UEList[i].x <= xupper and ylower <= UEList[i].y <= yupper:
            tempquadrant.append(UEList[i])        
    tempquadrant = [*set(tempquadrant)]
    
     # Puts a wireless cell in between 2 UEs if possible
    for i in range(len(tempquadrant)):
        accountedFor = False
        j = i+1
        for j in range(len(tempquadrant)):
            if len(tempquadrant) == 1:
                break
            elif j != i:
                p = [tempquadrant[i].x, tempquadrant[i].y]
                q = [tempquadrant[j].x, tempquadrant[j].y]
                if math.dist(p, q) <= 2*wlR:
                    accountedFor = True
                    averageX = (tempquadrant[i].x + tempquadrant[j].x)/2
                    averageY = (tempquadrant[i].y + tempquadrant[j].y)/2
                    tempquadrant[i].sharing = True
                    tempquadrant[j].sharing = True

                    addWireless(averageX, averageY, "SHARED")
                    sharingUEs += 1
    
    # Puts wireless cell around UEs that have no others in range
        if not accountedFor:
                addWireless(tempquadrant[i].x , tempquadrant[i].y , "NONE")


def createSharedPaths(xlower, xupper, ylower, yupper):
    global sharingUEs, numWireless
    tempquadrant = []

    # Puts all wireless cell in quadrant into temporary list
    for i in range(len(WirelessList)):
        if xlower<= WirelessList[i].x <= xupper and ylower <= WirelessList[i].y <= yupper:
            tempquadrant.append(WirelessList[i])
    tempquadrant = [*set(tempquadrant)]
    print(tempquadrant)

    for i in range(len(tempquadrant)- 1):
        accountedFor = False
        pX = 0
        pY = 0 
        qX = 0
        qY = 0
        
        mindist = 100
        j = i + 1
        while j < len(tempquadrant):
            p = [tempquadrant[i].x, tempquadrant[i].y]
            # Finds closest pair p and q within certain distances
            if math.dist(p, nearestAxis(tempquadrant[i].x, tempquadrant[i].y)) > 2*wlR:
                q = [tempquadrant[j].x, tempquadrant[j].y]
                distpq = math.dist(p, q)
                if distpq <= 8*wlR and distpq <= mindist and p != q: 
                    mindist = distpq
                    closestCell = tempquadrant[j]
                    pX = p[0]
                    pY = p[1]
                    qX = closestCell.x
                    qY = closestCell.y
                    accountedFor = True
            j += 1

        # If an acceptable close point found, add cell between them
        if accountedFor:
            averageX = (pX + qX)/2
            averageY = (pY+ qY)/2

            addWireless(averageX, averageY, "PURPLE")
            #tempquadrant[i].sharing = True
            #tempquadrant[j].sharing = True
            sharingUEs += 1

            # Process to remove the further of 2 cells from final paths
            dist = []
            dist.append(math.dist((pX, pY), nearestAxis(pX, pY)))
            dist.append(math.dist((qX, qY), nearestAxis(qX, qY)))
            minpos = dist.index(min(dist))
            
            if minpos == 0:
                x = pX
                y = pY
                if (qX, qY) in finalLeaves:
                    finalLeaves.remove((qX, qY))
            else: 
                x = qX
                y = qY
                if (pX, pY) in finalLeaves:
                    finalLeaves.remove((pX, pY))

            center = plt.Circle((x, y), 1,  color = 'purple', fill = False)
            axes.add_artist(center)

            newCell = plt.Circle((x, y), wlR, fill = False) 
            axes.add_artist(newCell)

# Creates a line of Wireless cells to the nearest point on the "fibre" 
# for all existing wireless cells
def makeWirelessPath():
    for i in range(len(finalLeaves)):
        min = nearestAxis(finalLeaves[i][0], finalLeaves[i][1])
        if (min[0] == finalLeaves[i][0]):
            if(min[1] >= finalLeaves[i][1]): 
                newY = finalLeaves[i][1] + wlR
                while newY < min[1]:
                    addWireless(finalLeaves[i][0], newY, "PATH")
                    newY += wlR
            else:
                newY = finalLeaves[i][1] - wlR
                while newY > min[1]:
                    addWireless(finalLeaves[i][0], newY, "PATH")
                    newY -= wlR
        else:
            if(min[0] >= finalLeaves[i][0]): 
                newX = finalLeaves[i][0] + wlR
                while newX < min[0]:
                    addWireless(newX, finalLeaves[i][1], "PATH")
                    newX += wlR
            else:
                newX = finalLeaves[i][0] - wlR
                while newX > min[0]:
                    addWireless(newX, finalLeaves[i][1], "PATH")
                    newX -= wlR


def removeCloseRedundants(xlower, xupper, ylower, yupper):
    global sharingUEs, numWireless
    tempquadrant = []

    # Puts all wireless cell in quadrant into temporary list
    for i in range(len(WirelessList)):
        if xlower<= WirelessList[i].x <= xupper and ylower <= WirelessList[i].y <= yupper:
            tempquadrant.append(WirelessList[i])
    tempquadrant = [*set(tempquadrant)]

    for i in range(len(tempquadrant)- 1):
        j = i + 1
        while j < len(tempquadrant):
            p = [tempquadrant[i].x, tempquadrant[i].y]
            q = [tempquadrant[j].x, tempquadrant[j].y]
            # Finds closest pair p and q within certain distances
            if (math.dist(p,q) < .2*wlR) and (tempquadrant[i] in WirelessList):
                WirelessList.remove(tempquadrant[i])
                print("removed")
            j += 1
    

'''maybe have a sharing trait (t/f?) and then count at the end?'''

'''------------------------------------------------------------------'''

figure, axes = plt.subplots()
plt.plot([first, first], [0,100], 'g', linewidth=3, markersize=5)
plt.plot([second,second], [0,100], 'g', linewidth=3, markersize=5)
plt.plot([0,100], [third,third], 'g', linewidth=3, markersize=5)
plt.plot([0,100], [fourth,fourth], 'g', linewidth=3, markersize=5)

for x in range(numUEs):
    a = random.randint(1, 99)
    b = random.randint(1, 99)
    randomUE = UE(a,b, False)
    Drawing_colored_circle = plt.Circle((a,b), 1)
    axes.add_artist(Drawing_colored_circle)
    UEList.append(randomUE)

findShared(0, first, fourth, 100)
findShared(first, second, fourth, 100)
findShared(second, 100, fourth, 100)
findShared(0, first, third, fourth)
findShared(first, second, third, fourth)
findShared(second, 100, third, fourth)
findShared(0, first, 0, third)
findShared(first, second, 0, third)
findShared(second, 100, 0, third)

for i in range(len(WirelessList)):
    finalLeaves.append((WirelessList[i].x, WirelessList[i].y))
finalLeaves = [*set(finalLeaves)]


createSharedPaths(0, first, fourth, 100)
createSharedPaths(first, second, fourth, 100)
createSharedPaths(second, 100, fourth, 100)
createSharedPaths(0, first, third, fourth)
createSharedPaths(first, second, third, fourth)
createSharedPaths(second, 100, third, fourth)
createSharedPaths(0, first, 0, third)
createSharedPaths(first, second, 0, third)
createSharedPaths(second, 100, 0, third)

WirelessList = [*set(WirelessList)]
finalLeaves = [*set(finalLeaves)]

makeWirelessPath()

'''removeCloseRedundants(0, first, fourth, 100)
removeCloseRedundants(first, second, fourth, 100)
removeCloseRedundants(second, 100, fourth, 100)
removeCloseRedundants(0, first, third, fourth)
removeCloseRedundants(first, second, third, fourth)
removeCloseRedundants(second, 100, third, fourth)
removeCloseRedundants(0, first, 0, third)
removeCloseRedundants(first, second, 0, third)
removeCloseRedundants(second, 100, 0, third)'''
WirelessList = [*set(WirelessList)]
drawCells()

shared = 0
for ue in UEList:
    if ue.sharing == True:
        shared += 1

'''------------------------------------------------------------------'''

print("Metrics:")
print("Number of UEs: ", numUEs)
print("Number of Cells: ", len(WirelessList))
print("Number of UEs sharing a path: ", sharingUEs)
print("Num of UEs sharing a path: ", shared)