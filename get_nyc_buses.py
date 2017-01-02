import pyodbc
import requests
import time
import datetime
from time import gmtime, strftime
from xml.dom.minidom import parse
import xml.dom.minidom

while True:

    # Build file name based on current time
    current_time = time.time()
    file_name = "D:/Python/MyBigBro/Scripts/nyc_buses/" + str(current_time) + ".xml"

    # Get the NYC Buses data
    response = requests.get('http://bustime.mta.info/api/where/vehicles-for-agency/MTA%20NYCT.xml?key=[your bustime api key]')

    # Write to file
    file = open(file_name, "w")
    file.write(response.text)
    file.close()

    # Data seems to update about once every 20 seconds
    time.sleep(20)

    # Parse the XML file dowloaded
    DOMTree = xml.dom.minidom.parse(file_name)
    collection = DOMTree.documentElement
    vehicleStatuses = collection.getElementsByTagName("vehicleStatus")
    for vehicleStatus in vehicleStatuses:
        
        # We are only tracking in_progress buses on the M15 route...
        if vehicleStatus.getElementsByTagName("phase")[0].childNodes[0].data == "in_progress":
            if vehicleStatus.getElementsByTagName("tripId").length > 0:
                if "M15" in str(vehicleStatus.getElementsByTagName("tripId")[0].childNodes[0].data):

                    # Print some vehicle details
                    print "*****Vehicle Status*****"
                    print "vehicleId: %s" % vehicleStatus.getElementsByTagName("vehicleId")[0].childNodes[0].data
                    print "lastLocationUpdateTime: %s" % vehicleStatus.getElementsByTagName("lastLocationUpdateTime")[0].childNodes[0].data
                    print "lat: %s" % vehicleStatus.getElementsByTagName("lat")[0].childNodes[0].data
                    print "lon: %s" % vehicleStatus.getElementsByTagName("lon")[0].childNodes[0].data
                    print "tripId: %s" % vehicleStatus.getElementsByTagName("tripId")[0].childNodes[0].data

                    # Get variable for mybigbro.tv payload
                    XCoord = vehicleStatus.getElementsByTagName("lon")[0].childNodes[0].data
                    YCoord = vehicleStatus.getElementsByTagName("lat")[0].childNodes[0].data
                    DeviceName = vehicleStatus.getElementsByTagName("vehicleId")[0].childNodes[0].data
                    MarkerDateTime = datetime.datetime.fromtimestamp(float(str(vehicleStatus.getElementsByTagName("lastLocationUpdateTime")[0].childNodes[0].data)[:10]))
                    print "MarkerDateTime: %s" % MarkerDateTime

                    # Upload
                    payload = {"MarkerDateTime":str(MarkerDateTime),"XCoord":XCoord,"YCoord":YCoord,"DeviceName":DeviceName}
                    response = requests.post('http://www.mybigbro.tv/api/geomarkers', data=payload)

    continue
            
