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

def remove_outlier_data(data):
    
    x_list_mean = []
    y_list_mean = []
    x_list = []
    y_list = []
    for d in data:
        x_list.extend(d.x)
        y_list.extend(d.y)
        x_list_mean.append(np.mean(d.x))
        y_list_mean.append(np.mean(d.y))

    x_mean = np.mean(x_list_mean)
    y_mean = np.mean(y_list_mean)

    x_standard_deviation = np.std(x_list)
    y_standard_deviation = np.std(y_list)

    data_without_outlier = []
    for index, d in enumerate(data):
        if not ((x_list_mean[index] > x_mean + 2*x_standard_deviation or x_list_mean[index] < x_mean - 2*x_standard_deviation) or (y_list_mean[index] > y_mean + 2*y_standard_deviation or y_list_mean[index] < y_mean - 2*y_standard_deviation)):
            data_without_outlier.append(d)

    return data_without_outlier

def main():

    pool = multiprocessing.Pool(4)
    runs = pool.map(readin_data, listdir('RawData/'))

    type_names = set(([r.name for r in runs]))
    type_values = []
    temp_data = runs
    for type_name in type_names:
        temp_count = 0
        for index, r in enumerate(temp_data):
            if (r.name == type_name):
                temp_count += 1

        type_values.append({
            'type_name': type_name,
            'count': temp_count
        })
    type_values.sort(key = lambda x : x['count'], reverse=True)
    for index, type_value in enumerate(type_values):
        print(str(index+1) + '\t->\t'  + 'Count: '+ str(type_value['count']) + '\t| ' + type_value['type_name'])

    quit_loop = True
    while(quit_loop):
        input_index = input("Enter the value you wanted plotted: ")
        values_to_be_plotted = [r for r in runs if r.name == (type_values[int(input_index)-1])['type_name']]
        input_points_per_frame = input("Enter points per frame (Runs: 5, Walks: 10): ")

        values_to_be_plotted_minus_outlier = remove_outlier_data(values_to_be_plotted)
        plot_outlier = 'Y'
        if (len(values_to_be_plotted) - len(values_to_be_plotted_minus_outlier) > 0):
            print('There are ' + str(len(values_to_be_plotted) - len(values_to_be_plotted_minus_outlier)) + ' courses considered outlier')
            plot_outlier = input('Include outlier? (Y or N): ')

        if (plot_outlier == 'Y'):
            new_plot = plot.plot(values_to_be_plotted)
            new_plot.build_plot((type_values[int(input_index)-1])['type_name'], int(input_points_per_frame))
        else:
            new_plot = plot.plot(values_to_be_plotted_minus_outlier)
            new_plot.build_plot((type_values[int(input_index)-1])['type_name'], int(input_points_per_frame))

        input_quit = input("Quit? (Y or N): ")
        if input_quit == 'Y':
            quit_loop = False 

if __name__=="__main__":
    main()