from fileinput import close
import gpxpy 
import gpxpy.gpx 
from datetime import datetime
import os
import shutil

class run:
    def __init__(self, file):
        self.filename = file
        gpx_file = open('RawData/' + self.filename, 'r') 
        self.gpx = gpxpy.parse(gpx_file)
        gpx_file.close()

    def get_initial_data(self):
        data = self.gpx.tracks[0]
        self.name = data.name
        self.date_time = data.get_time_bounds().start_time
        self.new_filename = self.name.replace(' ','') + '_' + self.date_time.strftime("%Y-%m-%d_%H-%M-%S") + '.gpx'

        self.route = []
        for segment in data.segments:
            for point in segment.points:
                self.route.append({
                    'x': point.longitude,
                    'y': point.latitude,
                    'elevation': point.elevation
                })
    
    def create_new_file(self):
        if not os.path.exists('CleanData/' + self.new_filename):
            shutil.copy('RawData/' + self.filename, 'CleanData/' + self.new_filename)
            print('RawData/' + self.filename + '\t\t -> \t\tCleanData/' + self.new_filename)