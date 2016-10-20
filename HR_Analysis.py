from lxml import etree
import matplotlib.pyplot as plt
# import tkinter

class garmin:

    def get_file(self, filename='activity_1321393768.tcx'):
        self.filename = filename
        # root = tkinter.Tk()
        # root.withdraw() # we don't want a full GUI, so keep the root window from appearing
        # root.update()
        # self.filename = tkinter.tkfiledialog.askopenfilename() # show an "Open" dialog box and return the path to the selected file

    def parse_file(self):
        tree = etree.parse(self.filename)
        root = tree.getroot()
        xmlstr = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
        points = tree.findall('//'+xmlstr+'Trackpoint')
        self.distance = [r.find(xmlstr+'DistanceMeters').text for r in points]
        self.hr = [r.find(xmlstr+'HeartRateBpm')[0].text for r in points]
        self.speed = [r.find(xmlstr+'Extensions')[0][0].text for r in points]
        self.pace = [float(curr)*3600/1000 for curr in self.speed]
        self.time = range(0,len(self.distance))

    def plot_data(self):
        plt.figure(1)
        plt.plot(self.time,self.hr)
        plt.figure(2)
        plt.plot(self.time,self.speed)
        plt.figure(3)
        plt.plot(self.hr,self.pace)
        plt.show()

if __name__ == '__main__':
    myData = garmin()
    print("Getting file...")
    myData.get_file()
    print("Parsing file...")
    myData.parse_file()
    print("Plotting data...")
    myData.plot_data()
    # myData.plotData()
