import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from datetime import datetime

class plot:
    def __init__(self, runs):
        self.data = runs

        list_of_list_x, list_of_list_y = [], []
        for r in runs:
            list_of_list_x.append(r.x)
            list_of_list_y.append(r.y)

        self.x_min = min(min(list_of_list_x, key=min))
        self.x_max = max(max(list_of_list_x, key=max))
        self.y_min = min(min(list_of_list_y, key=min))
        self.y_max = max(max(list_of_list_y, key=max))
        self.length_max = len(max(list_of_list_x, key=len))

    def build_plot(self, title, points_per_frame):
        fig = plt.figure()
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
        ax1 = plt.axes(xlim=(self.x_min - .001, self.x_max + .001), ylim=(self.y_min - .001, self.y_max + .001))
        line, = ax1.plot([], [], lw=1)
        #plt.axis('off')

        lines = []
        for index in range(len(self.data)):
            lobj = ax1.plot([],[],lw=1,color='b')[0]
            lines.append(lobj)
        def init():
            for line in lines:
                line.set_data([],[])
            return lines

        x_animation_values , y_animation_values = [[] for x in self.data], [[] for x in self.data]
        def animate(i):
            for index in range(len(self.data)):
                x_animation_values[index] = self.data[index].x[:i*points_per_frame]
                y_animation_values[index] = self.data[index].y[:i*points_per_frame]
            for lnum,line in enumerate(lines):
                line.set_data(x_animation_values[lnum], y_animation_values[lnum]) 
            return lines

        plt.gca().set_facecolor('xkcd:black')
        plt.gca().set_aspect('equal', adjustable='box')
        anim = animation.FuncAnimation(fig, animate, init_func=init, frames=self.length_max//points_per_frame, interval=1, blit=True)
        anim.save('Output/' + self.data[0].name.replace(' ','') + '_' + datetime.now().strftime("%Y-%m-%d") + '.gif', writer='imagemagick', fps=30)

        plt.show()
