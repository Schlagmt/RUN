from fileinput import close
import gpxpy 
import gpxpy.gpx 
from datetime import datetime
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

        self.x = []
        self.y = []
        self.elevation = []
        for segment in data.segments:
            for point in segment.points:
                self.x.append(point.longitude)
                self.y.append(point.latitude)
                self.elevation.append(point.elevation)
        print('Processed: ' + self.new_filename)
    
    def create_new_file(self):
        shutil.copy('RawData/' + self.filename, 'CleanData/' + self.new_filename)
        print('RawData/' + self.filename + '\t\t -> \t\tCleanData/' + self.new_filename)