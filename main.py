import multiprocessing
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import run 
import plot 
import os
from os import listdir
from sklearn.cluster import DBSCAN, cluster_optics_dbscan
from geopy.geocoders import Nominatim

def readin_data(file):
    route = run.run(file)
    route.get_initial_data()
    return route

def cluster_data_DBSCAN(data):
    
    xy_coordinates = [[d.x[0],d.y[0]] for d in data]
    X = np.vstack(np.array(xy_coordinates))

    kms_per_radian = 6371.0088
    epsilon = 0.5 / kms_per_radian
    clust = DBSCAN(eps=epsilon, min_samples=3, algorithm='ball_tree', metric='haversine').fit(np.radians(X))

    groupings = [[] for x in range(min(clust.labels_), max(clust.labels_))]
    for index, d in enumerate(data):
        groupings[clust.labels_[index]].append(d)
    
    return groupings

def get_approximate_locations(data):
    locations = []
    geolocator = Nominatim(user_agent="geoapiExercises")
    for d in data:
        loc = geolocator.reverse(str(d[1]) + ',' + str(d[0]))
        address = loc.raw['address']
        locations.append(address.get('road','') + ' ' + address.get('city','') + ' ' + address.get('state',''))

    return locations


def main():

    pool = multiprocessing.Pool(4)
    runs = pool.map(readin_data, listdir('Data/'))

    clustered_data = cluster_data_DBSCAN(runs)
    approximate_locations = get_approximate_locations([[c[0].x[0], c[0].y[0]] for c in clustered_data])
    combined_data = [[approximate_locations[i], clustered_data[i]] for i in range(len(approximate_locations))]
    combined_data.sort(key = lambda x: len(x[1]), reverse = True)

    for index, cluster in enumerate(combined_data):
        print(str(index+1) + '\t->\t'  + 'Count: '+ str(len(cluster[1])) + '\t| ' + cluster[0])

    quit_loop = True
    while(quit_loop):
        input_index = input("Enter the value you wanted plotted: ")
        input_points_per_frame = input("Enter points per frame (Runs: 5, Walks: 10): ")

        new_plot = plot.plot(combined_data[int(input_index) - 1][1])
        new_plot.build_plot(combined_data[int(input_index) - 1][0], int(input_points_per_frame))

        input_quit = input("Quit? (Y or N): ")
        if input_quit == 'Y':
            quit_loop = False 

if __name__=="__main__":
    main()