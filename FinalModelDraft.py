''' 
NextG Networks Model Project
Author: Natalia Tam
Github Repo: https://github.com/nataliatam/summer-reu/tree/main
'''

import random
import math
import requests

'''------------------------------------------------------------------'''

latlon_meter_conversion = 111139 # 1 degree = 111,139m
wlR = 100 / latlon_meter_conversion # radius of wireless cell in meters
numUEs = 5 # number of UEs

UEList = [] # The list of all the UEs and their data
WirelessList = [] # List of all the wireless cells and their data
finalLeaves = [] # List of the cells that connect directly back to fiber

'''------------------------------------------------------------------'''

# Wireless Cell Object Class
class WirelessCell:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type # types: SHARED/BLUE, PATH, NONE, PURPLE
        self.closestRoadPoint = (0, 0)
        self.closestRoadDistance = 0
    
    def setClosestRoadPoint(self, x, y):
        self.closestRoadPoint = (x, y)
    
    # String method for printing Wireless cell info
    def __str__(self):
        return f"(x, y): ({self.x}, {self.y}); Type: {self.type} \n Closest Road Point: {self.closestRoadPoint}; Closest Road Distance: {self.closestRoadDistance}"
        
# UE Object Class
class UE:
    def __init__(self, x, y, sharing):
        self.x = x
        self.y = y
        self.sharing = False # True/False if UE is sharing a path

    # String method for printing UE info
    def __str__(self):
        return f"(x, y): ({self.x}, {self.y}); Shared: {self.sharing}"
        
    
'''------------------------------------------------------------------'''

# Creates Wireless object given (x, y, and type of cell); adds it to running list
def addWireless(x, y, type):
    temp = WirelessCell(x, y, type)
    WirelessList.append(temp)
    return temp

# Determines if any 2 UEs are within the reach of 1 Wireless Cell from 
# each other. If so, a Wireless Cell is placed in between the 2. If not, 
# a cell is placed around the 1 UE (that is not within reach of sharing)
def findShared(xlower, xupper, ylower, yupper):
    tempquadrant = []

    # Adds all UEs in quadrant into temporary list (Lines 60-63)
    # (The use of this temporary list is just to help the program run 
    # faster/do less comparisions if we were working with a bigger 
    # parcel of land. It's not really necessary in our case)
    for i in range(len(UEList)):
        if xlower<= UEList[i].x <= xupper and ylower <= UEList[i].y <= yupper:
            tempquadrant.append(UEList[i])        
    tempquadrant = [*set(tempquadrant)]
    
     # Puts a wireless cell in between 2 UEs if possible to create a shared path
    for i in range(len(tempquadrant)):
        accountedFor = False
        j = i+1
        for j in range(len(tempquadrant)):
            if len(tempquadrant) == 1:
                break
            elif j != i:
                p = [tempquadrant[i].x, tempquadrant[i].y] # (x,y) of UE1
                q = [tempquadrant[j].x, tempquadrant[j].y] # (x,y) of UE2

                # If UE1 and UE2 are within range of 1 cell, places a
                # new shared cell in between them
                if math.dist(p, q) <= 2*wlR: 
                    accountedFor = True
                    averageX = (tempquadrant[i].x + tempquadrant[j].x)/2
                    averageY = (tempquadrant[i].y + tempquadrant[j].y)/2
                    tempquadrant[i].sharing = True
                    tempquadrant[j].sharing = True

                    addWireless(round(averageX, 7), round(averageY,7) , "SHARING UE")
    
    # Puts Wireless Cell around UEs that have no others in range
        if not accountedFor:
                addWireless(tempquadrant[i].x , tempquadrant[i].y , "DEFAULT UE")


'''------------------------------------------------------------------'''

# Determines which pairs of cells are within reasonable distance to
# share a path. Then, proceeds determine which cell in the pair is 
# closer to fiber, adding that cell to the "finalLeaves" list.

def createSharedPaths(xlower, xupper, ylower, yupper):
    # Puts all wireless cell in quadrant into temporary list
    # (The use of this temporary list is just to help the program run 
    # faster/do less comparisions if we were working with a bigger 
    # parcel of land. It's not really necessary in our case)
    tempquadrant = []
    for i in range(len(WirelessList)):
        if xlower<= WirelessList[i].x <= xupper and ylower <= WirelessList[i].y <= yupper:
            tempquadrant.append(WirelessList[i])
    tempquadrant = [*set(tempquadrant)]

    # Compares every pair of current cells placed
    for i in range(len(tempquadrant)- 1):
        accountedFor = False
        pX = 0
        pY = 0 
        qX = 0
        qY = 0
        
        mindist = 100
        j = i + 1
        while j < len(tempquadrant):
            p = [tempquadrant[i].x, tempquadrant[i].y] # Cell1

            # Finds closest pair Cell1 and Cell1 that is further than range
            # of 1 cell to fiber, but within 3 cell hops
            if tempquadrant[i].closestRoadDistance > 2*wlR:
                q = [tempquadrant[j].x, tempquadrant[j].y] # Cell2
                distpq = math.dist(p, q)
                if distpq <= 6*wlR and distpq <= mindist and p != q: 
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
            cell = addWireless(averageX, averageY, "SHARED PATH")

            # OSRM API endpoint and Adding Closest Road Info to new shared cell
            # Code adapted from @aichakaba
            osrm_endpoint = "http://router.project-osrm.org"
            distance = round(get_distance_to_nearest_road(cell, osrm_endpoint), 2)
            cell.closestRoadDistance = distance
            location = get_nearest_roadpoint(cell, osrm_endpoint)
            cell.setClosestRoadPoint(location[1], location[0])

            tempquadrant[i].sharing = True
            closestCell.sharing = True

            # Process to remove the further of 2 cells from finalLeaves 
            # list to ensure that only the closer 1 has direct path to fiber
            distP = tempquadrant[i].closestRoadDistance
            distQ = closestCell.closestRoadDistance
            
            if distP < distQ:
                if closestCell in finalLeaves:
                    finalLeaves.remove(closestCell)
            else: 
                if tempquadrant[i] in finalLeaves:
                    finalLeaves.remove(tempquadrant[i])


# Creates a perpendicular path of Wireless cells to the nearest point on
# the fiber for all cells in the "finalLeaves" list that are not already 
# within range of fiber
def makeWirelessPath(finalLeavesList):
    for cell in finalLeavesList:
        min = cell.closestRoadPoint # coordinate of closest fiber point
        rise = min[1] - cell.y
        run = min[0] - cell.x
        denom = math.sqrt(pow(rise,2) + pow(run,2)) # from pythagorean theorem
        if denom != 0:
            factor = wlR/denom
            newX = cell.x 
            newY = cell.y

            # place cells on path until within the range of fiber
            while abs(newY - min[1]) >= wlR:
                newX = newX + (run * factor) # X-coordinate of cell on path to fiber
                newY = newY + (rise * factor) # Y-coordinate of cell on path to fiber
                addWireless(newX, newY, "PATH")

'----------------------------------------------------------------------'

# Method to generate random UEs within min/max lat and lon
def generateRandomUEs(min_lat, max_lat, min_lon, max_lon):
    lat = round(random.uniform(min_lat, max_lat),7)
    lon = round(random.uniform(min_lon, max_lon),7)
    randomUE = UE(lat,lon, False)
    return randomUE

# Given point and OSRM url endpoint, returns distance to the nearest road
# Method written by @aichakaba
def get_distance_to_nearest_road(origin, osrm_endpoint):
    url = f"{osrm_endpoint}/nearest/v1/driving/{origin.y},{origin.x}"
    response = requests.get(url)
    data = response.json()
    return data['waypoints'][0]['distance']

# Given point and OSRM url endpoint, returns coordinate of nearest road
# Code adapted from @aichakaba
def get_nearest_roadpoint(origin, osrm_endpoint):
    url = f"{osrm_endpoint}/nearest/v1/driving/{origin.y},{origin.x}"
    response = requests.get(url)
    data = response.json()
    return data['waypoints'][0]['location']

'''------------------------------------------------------------------'''

def main():
    global WirelessList

    # boundaries of the parcel of land (currently set to Princeton's campus)
    min_lat, max_lat = 40.333, 40.345
    min_lon, max_lon = -74.667, -74.657

    # Generate 'numUEs' random UEs and append to running UE list
    for x in range(numUEs):
        randomUE = generateRandomUEs(min_lat, max_lat, min_lon, max_lon)
        UEList.append(randomUE)
    
    # Places initial Wireless Cells on singular UEs or between pairs of UEs within 1 cell's reach
    findShared(min_lat, max_lat, min_lon, max_lon)
    WirelessList = list(set(WirelessList)) # Intended to remove duplicate cells
    finalLeaves = WirelessList # Copies all current wireless cells into preliminary finalLeaves list

    # OSRM API endpoint
    osrm_endpoint = "http://router.project-osrm.org"

    # Calculate the distance to the nearest road for each Wireless Cell
    for cell in WirelessList:
        distance = round(get_distance_to_nearest_road(cell, osrm_endpoint), 2)
        cell.closestRoadDistance = distance
        location = get_nearest_roadpoint(cell, osrm_endpoint)
        cell.setClosestRoadPoint(location[1], location[0])

    print('---------------TESTING: PRINTS ALL UES AND THEIR INFO-------------')
    
    for x in UEList:
        print(x)
    
    print('\n -----------------------------------------------------------')
    print('-----------TESTING: PRINTS ALL FINAL LEAF CELLS AND THEIR INFO-----------')

    # Places cells to be shared between pairs of reasonably distanced cells
    createSharedPaths(min_lat, max_lat, min_lon, max_lon)

    finalLeaves = list(set(finalLeaves)) # intended to remove duplicates
    for x in finalLeaves:
        print(x)
        print('\n')
    
    # Final step: places direct path of wireless cells to fiber from all
    # cells in "finalLeaves" list (that aren't already in range of fiber)
    makeWirelessPath(finalLeaves)

    print('-----------------------------------------------------------')
    print('-----------TESTING: PRINTS ALL CELLS AND THEIR INFO---------')

    for x in WirelessList:
        print(x)
        print('\n')

    print('-----------------------------------------------------------')
    print('--------------------------METRICS:------------------------')

    print("Metrics:")
    print("Number of UEs: ", numUEs)
    print("Number of Cells: ", len(WirelessList))


if __name__ == "__main__":
    main()