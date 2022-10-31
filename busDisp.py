import os
import urllib.request as UL
import xml.etree.ElementTree as ET

key = os.getenv('BUSTIME_API_KEY')

# Access data through the official Port Authority API (reccomended)
# Gets all buses and their predicted arrivals at specified stops
def getAllArrivalsAPI(stop_numbers):
    # Convert list to csv string
    stop_numbers_string = ','.join(stop_numbers)

    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions?key='+key+'&rtpidatafeed=Port%20Authority%20Bus&stpid='+stop_numbers_string

    # Get XML response and parse
    XML = UL.urlopen(URL).read()
    root = ET.fromstring(XML)

    # Extract necessary data from parsed XML
    routes, times = [[],[]]
    for bus in root.findall('prd'):
        routes.append(bus.find('rt').text)
        times.append(bus.find('prdctdn').text)
    
    return routes,times
    

# Access data through the official Port Authority API (reccomended)
# Gets certain bus lines and their predicted arrivals at specified stops
def getSpecificArrivalsAPI(bus_lines,stop_numbers):
    # Convert list to csv string
    stop_numbers_string = ','.join(stop_numbers)
    bus_lines_string = ','.join(bus_lines)

    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions?key='+key+'&rtpidatafeed=Port%20Authority%20Bus&stpid='+stop_numbers_string\
        +'&rt='+bus_lines_string

    # Get XML response and parse
    XML = UL.urlopen(URL).read()
    root = ET.fromstring(XML)

    # Extract necessary data from parsed XML
    routes, times = [[],[]]
    for bus in root.findall('prd'):
        routes.append(bus.find('rt').text)
        times.append(bus.find('prdctdn').text)
    
    return routes,times

routes, times = getSpecificArrivalsAPI(['71B','71D'],['3140','8312'])
routes, times = getAllArrivalsAPI(['3140','8312'])
print(routes,times)