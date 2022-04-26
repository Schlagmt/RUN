import multiprocessing
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import run 
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

    fig = plt.figure()

    minXs = []
    minYs = []
    maxXs = []
    maxYs = []
    lengths = []
    for r in runs:

        minXs.append(min(r.x))
        minYs.append(min(r.y))
        maxXs.append(max(r.x))
        maxYs.append(max(r.y))
        lengths.append(len(r.x))

        # plt.scatter(x,y,color='r', s=0)
        # plt.plot(r.x,r.y,color='b',linewidth=1)
        # print('Plotting: ' + r.name)

    ax1 = plt.axes(xlim=(min(minXs) - .001, max(maxXs) + .001), ylim=(min(minYs) - .001, max(maxYs) + .001))
    line, = ax1.plot([], [], lw=2)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Title')

    lines = []
    for index in range(len(runs)):
        lobj = ax1.plot([],[],lw=1,color='b')[0]
        lines.append(lobj)

    def init():
        for line in lines:
            line.set_data([],[])
        return lines

    Xs = [[] for x in runs]
    Ys = [[] for x in runs]

    frames_per_frame = 5

    def animate(i):

        for index in range(len(runs)):
            Xs[index] = runs[index].x[:i*frames_per_frame]
            Ys[index] = runs[index].y[:i*frames_per_frame]

        #for index in range(0,1):
        for lnum,line in enumerate(lines):
            line.set_data(Xs[lnum], Ys[lnum]) # set data for each line separately. 

        return lines

    plt.gca().set_facecolor('xkcd:black')
    
    plt.gca().set_aspect('equal', adjustable='box')
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=max(lengths)//frames_per_frame, interval=1, blit=True)

    plt.show()

if __name__=="__main__":
    main()