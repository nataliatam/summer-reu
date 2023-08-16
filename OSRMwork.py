#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 12:17:14 2023

@author: aichakaba and Natalia Tam
"""

import random
import requests

def generate_random_points(n, min_lat, max_lat, min_lon, max_lon):
    points = []
    for _ in range(n):
        lat = random.uniform(min_lat, max_lat)
        lon = random.uniform(min_lon, max_lon)
        points.append((round(lat, 7), round(lon, 7)))
    return points

def get_distance_to_nearest_road(origin, osrm_endpoint):
    url = f"{osrm_endpoint}/nearest/v1/driving/{origin[1]},{origin[0]}"
    response = requests.get(url)
    data = response.json()
    return data['waypoints'][0]['distance']

def get_nearest_roadpoint(origin, osrm_endpoint):
    url = f"{osrm_endpoint}/nearest/v1/driving/{origin[1]},{origin[0]}"
    response = requests.get(url)
    data = response.json()
    return data['waypoints'][0]['location']

def main():
    # boundaries of the parcel of land
    min_lat, max_lat = 40.333, 40.345
    min_lon, max_lon = -74.667, -74.657

    # Random points within the parcel of land
    N = 5  # Number of points 
    random_points = generate_random_points(N, min_lat, max_lat, min_lon, max_lon)

    # OSRM API endpoint
    osrm_endpoint = "http://router.project-osrm.org"

    # Calculate the distance to the nearest road for each point
    distances_to_roads = []
    points_on_roads = []
    for point in random_points:
        distance = get_distance_to_nearest_road(point, osrm_endpoint)
        distances_to_roads.append(round(distance,2))
        location = get_nearest_roadpoint(point, osrm_endpoint)
        points_on_roads.append(location)


    # Output the distances to the closest roads for each point
    for i, point in enumerate(random_points):
        print(f"Point {i+1} (Lat: {point[0]}, Lon: {point[1]}):") 
        print(f"\tDistance to the nearest road: {distances_to_roads[i]} meters")
        print(f"\tPoint on nearest road: (Lat: {points_on_roads[i][1]}, Lon: {points_on_roads[i][0]})\n")

if __name__ == "__main__":
    main()