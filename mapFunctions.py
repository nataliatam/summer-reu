# Helper function adding all points inside a polygon to a working list
def tempListInPolygon(corners):
    tempquadrant = []
    tempPoly = Polygon(corners)
    for i in range(len(WirelessList)):
        if tempPoly.contains(WirelessList[i].point):
            tempquadrant.add(WirelessList[i])
    tempquadrant = [*set(tempquadrant)]    
    return tempquadrant

'''------------------------------------------------------------------''' 

def findShared(polygon):
    
    # Adds all UEs in quadrant into temporary list
    tempquadrant = tempListInPolygon(polygon)

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



def createSharedPaths(polygon):
    tempquadrant = []
    poly = Polygon(polygon)

    # Adds all UEs in quadrant into temporary list
    tempquadrant = tempListInPolygon(polygon)

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
            point = tempquadrant[i].point
            # Finds closest pair p and q within certain distances
            if poly.exterior.distance(point) > 2*wlR:
                q = [tempquadrant[j].x, tempquadrant[j].y]
                point2 = tempquadrant[j].point
                distpq = point.distance(point2)
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

            # Process to remove the further of 2 cells from final paths
            dist = []
            dist.append(point.distance(poly))
            dist.append(point2.distance(poly))
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
        x = finalLeaves[i][0]
        y = finalLeaves[i][1]
        min = 
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

