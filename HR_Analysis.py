"""
a python script analyzing garmin's .tcx files.
eventually I want to show trends in heart-rate vs. pace.
"""

from lxml import etree
import matplotlib.pyplot as plt

class Garmin:
    """ a class for dealing with garmin's tcx files. """

    def __init__(self, filename='activity_1321393768.tcx'):
        self.filename = filename

    def parse_file(self):
        tree = etree.parse(self.filename)
        xmlstr = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
        points = tree.findall('//'+xmlstr+'Trackpoint')
        self.distance = [r.find(xmlstr+'DistanceMeters').text for r in points]
        self.heart_rate = [r.find(xmlstr+'HeartRateBpm')[0].text for r in points]
        self.speed = [r.find(xmlstr+'Extensions')[0][0].text for r in points]
        self.pace = [float(curr)*3600/1000 for curr in self.speed]
        self.time = range(0, len(self.distance))

    def plot_data(self):
        plt.figure(1)
        plt.plot(self.time, self.heart_rate)
        plt.figure(2)
        plt.plot(self.time, self.speed)
        plt.figure(3)
        plt.plot(self.heart_rate, self.pace)
        plt.show()

if __name__ == '__main__':
    my_data = Garmin()
    print "Getting file..."
    print "Parsing file..."
    my_data.parse_file()
    print "Plotting data..."
    my_data.plot_data()
