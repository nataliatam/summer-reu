import random
import math
from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt
#import requests

'''------------------------------------------------------------------'''

wlR = 4
numUEs = 35

UEList = []
WirelessList = []
finalLeaves = []


'''------------------------------------------------------------------'''
class WirelessCell:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.point = Point(x, y)
        self.type = type # types: SHARED/BLUE, PATH, NONE, PURPLE

class UE:
    def __init__(self, x, y, sharing):
        self.x = x
        self.y = y
        self.point = Point(x, y)
        self.sharing = False

'''------------------------------------------------------------------'''

def addWireless(x, y, type):
    temp = WirelessCell(x, y, type)
    WirelessList.append(temp)

def findShared(xlower, xupper, ylower, yupper):
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
    
    # Puts wireless cell around UEs that have no others in range
        if not accountedFor:
                addWireless(tempquadrant[i].x , tempquadrant[i].y , "NONE")


'''------------------------------------------------------------------'''

def generateRandomUEs(min_lat, max_lat, min_lon, max_lon):
    lat = round(random.uniform(min_lat, max_lat),7)
    lon = round(random.uniform(min_lon, max_lon),7)
    randomUE = UE(lat,lon, False)
    return randomUE

'''# Given point and endpoint, returns distance to the nearest road
def get_distance_to_nearest_road(origin, osrm_endpoint):
    url = f"{osrm_endpoint}/nearest/v1/driving/{origin[1]},{origin[0]}"
    response = requests.get(url)
    data = response.json()
    return data['waypoints'][0]['distance']

# Given point and endpoint, returns coordinate of nearest road
def get_nearest_roadpoint(origin, osrm_endpoint):
    url = f"{osrm_endpoint}/nearest/v1/driving/{origin[1]},{origin[0]}"
    response = requests.get(url)
    data = response.json()
    return data['waypoints'][0]['location']

------------------------------------------------------------------'''

def main():

    # boundaries of the parcel of land
    min_lat, max_lat = 40.333, 40.345
    min_lon, max_lon = -74.667, -74.657

    for x in range(numUEs):
        randomUE = generateRandomUEs(min_lat, max_lat, min_lon, max_lon)
        UEList.append(randomUE)
    
    findShared(min_lat, max_lat, min_lon, max_lon)
    print('-----------------------------------------------------------')
    '''print(UEList)
    print(WirelessList)'''

if __name__ == "__main__":
    main()