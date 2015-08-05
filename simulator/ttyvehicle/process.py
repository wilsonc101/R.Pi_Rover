#!/usr/bin/python -B
import xml.etree.ElementTree as ET

from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--filepath", dest="filepath", help="Path to GPX file", metavar="FILEPATH")
(options, args) = parser.parse_args()

FILEPATH = options.filepath
OUTPUT_FILEPATH = FILEPATH.split(".gpx")[0] + ".py"


with open(FILEPATH) as gpx_data:
    xml_data = ET.XML(gpx_data.read())


python_datafile = open(OUTPUT_FILEPATH, 'w')



count = 0
for item in xml_data.iter("{http://www.topografix.com/GPX/1/1}rtept"):
    if count == 0:
        python_datafile.write("gps_cords = [(" + item.get("lat") + "," + item.get("lon") + "),\n")
    else:
        python_datafile.write("             (" + item.get("lat") + "," + item.get("lon") + "),\n")

    count += 1

python_datafile.close()
       
    
