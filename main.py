import multiprocessing
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import run 
import plot 
import os
from os import listdir
from sklearn.cluster import OPTICS, cluster_optics_dbscan
from geopy.geocoders import Nominatim

def readin_data(file):
    route = run.run(file)
    route.get_initial_data()

    if not os.path.exists('CleanData/' + route.new_filename):
        route.create_new_file()

    return route

def remove_outlier_data(data):
    
    xy_coordinates = [[d.x[0],d.y[0]] for d in data]
    X = np.vstack(np.array(xy_coordinates))
    clust = OPTICS(min_samples=5, xi=0.01, min_cluster_size=0.05)

    # Run the fit
    clust.fit(X)

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
        locations.append(address.get('county',''))

    return locations


def main():

    pool = multiprocessing.Pool(4)
    runs = pool.map(readin_data, listdir('RawData/'))

    clustered_data = remove_outlier_data(runs)

    approximate_locations = get_approximate_locations([[c[0].x[0], c[0].y[0]] for c in clustered_data])

    for index, cluster in enumerate(clustered_data):
        print(str(index+1) + '\t->\t'  + 'Count: '+ str(len(cluster)) + '\t| ' + approximate_locations[index])

    quit_loop = True
    while(quit_loop):
        input_index = input("Enter the value you wanted plotted: ")
        values_to_be_plotted = clustered_data[int(input_index) - 1]
        input_points_per_frame = input("Enter points per frame (Runs: 5, Walks: 10): ")

        #values_to_be_plotted_minus_outlier = remove_outlier_data(values_to_be_plotted)
        #plot_outlier = 'Y'
        #if (len(values_to_be_plotted) - len(values_to_be_plotted_minus_outlier) > 0):
            #print('There are ' + str(len(values_to_be_plotted) - len(values_to_be_plotted_minus_outlier)) + ' courses considered outlier')
            #plot_outlier = input('Include outlier? (Y or N): ')

        #if (plot_outlier == 'Y'):
        #    new_plot = plot.plot(values_to_be_plotted)
        #    new_plot.build_plot((type_values[int(input_index)-1])['type_name'], int(input_points_per_frame))
        #else:
        new_plot = plot.plot(values_to_be_plotted)
        new_plot.build_plot(approximate_locations[int(input_index)-1], int(input_points_per_frame))

        input_quit = input("Quit? (Y or N): ")
        if input_quit == 'Y':
            quit_loop = False 

if __name__=="__main__":
    main()