"""
a python script analyzing garmin's .tcx files.
eventually I want to show trends in heart-rate vs. pace.
"""

from lxml import etree
import matplotlib.pyplot as plt

def parse_file(filename='activity_1321393768.tcx'):
    """ function parse_file(filename).
        returns time, heart rate and pace from the tcx file."""

    # tree = etree.parse(filename)
    tree = getattr(etree, 'parse')(filename)
    xmlstr = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
    points = tree.findall('//'+xmlstr+'Trackpoint')
    # dist = [r.find(xmlstr+'DistanceMeters').text for r in points]
    heart = [int(r.find(xmlstr+'HeartRateBpm')[0].text) for r in points]
    speed = [float(r.find(xmlstr+'Extensions')[0][0].text) for r in points]
    pace = [float(curr)*3600/1000 for curr in speed]
    time = range(0, len(speed))
    return (time, heart, pace)

def smoothing(time, heart, pace):
    """ function smoothing(t, HR, pace).
        keeping only the points which have a stable pace for a minute."""

    heart_filt = []
    pace_filt = []
    for ind in range(60, len(time)):
        segment = (heart[(ind-60):ind])
        if (max(segment)-min(segment)) < 15:
            print "got one!"
            heart_filt.append(heart[ind-30]) # TODO improvement: use the average
            pace_filt.append(pace[ind-30])
    return (heart_filt, pace_filt)


def plot_data(heart_filt, pace_filt):
    """ plotting the filtered data. """

    plt.figure(1)
    plt.plot(heart_filt, pace_filt)
    plt.show()

def main():
    """ putting it all together... """
    (time, heart_rate, pace) = parse_file()
    (hr_filt, v_filt) = smoothing(time, heart_rate, pace)
    plot_data(hr_filt, v_filt)

if __name__ == '__main__':
    main()
