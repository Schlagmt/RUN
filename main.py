import multiprocessing
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import run 
import plot 
import os
from os import listdir

def readin_data(file):
    route = run.run(file)
    route.get_initial_data()

    if not os.path.exists('CleanData/' + route.new_filename):
        route.create_new_file()

    return route

def main():

    pool = multiprocessing.Pool(4)
    runs = pool.map(readin_data, listdir('RawData/'))

    type_names = set(([r.name for r in runs]))
    type_values = []
    for type_name in type_names:
        type_values.append({
            'type_name': type_name,
            'count': len([r.name for r in runs if r.name == type_name])
        })
    type_values.sort(key = lambda x : x['count'], reverse=True)
    for index, type_value in enumerate(type_values):
        print(str(index+1) + '\t->\t' + type_value['type_name'] + '\t\tCount: ' + str(type_value['count']))

    quit_loop = True
    while(quit_loop):
        input_index = input("Enter the value you wanted plotted: ")
        values_to_be_plotted = [r for r in runs if r.name == (type_values[int(input_index)-1])['type_name']]

        input_points_per_frame = input("Enter points per frame (Runs: 5, Walks: 10): ")
        new_plot = plot.plot(values_to_be_plotted)
        new_plot.build_plot((type_values[int(input_index)-1])['type_name'], int(input_points_per_frame))
        input_quit = input("Quit? (Y or N): ")
        if input_quit == 'Y':
            quit_loop = False 

if __name__=="__main__":
    main()