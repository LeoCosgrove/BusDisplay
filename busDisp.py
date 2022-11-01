import os
import xml.etree.ElementTree as ET
import requests
import json

key = os.getenv('BUSTIME_API_KEY')

# Access data through the official Port Authority API
# Gets all buses and their predicted arrivals at specified stops
def getAllArrivalsAPI(stop_numbers):
    # Convert list to csv string
    stop_numbers_string = ','.join(stop_numbers)
    # Build URL for API call
    ploads = {'key':key,'stpid':stop_numbers_string,'format':'json','rtpidatafeed':'Port Authority Bus'}
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions'


    # Get XML response and parse
    raw = requests.get(URL,ploads).json()['bustime-response']['prd']
    print(requests.get(URL,ploads).url)
    routes = [raw[x]['rt'] for x in range(len(raw))]
    times = [raw[x]['prdctdn'] for x in range(len(raw))]

    return routes,times


# Access data through the official Port Authority API
# Gets certain bus lines and their predicted arrivals at specified stops
def getSpecificArrivalsAPI(bus_lines,stop_numbers):
    # Convert list to csv string
    stop_numbers_string = ','.join(stop_numbers)
    bus_lines_string = ','.join(bus_lines)

    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions'
    ploads = {'key':key,'stpid':stop_numbers_string,'format':'json','rtpidatafeed':'Port Authority Bus','rt':bus_lines_string}

    # Get XML response and parse
    raw = requests.get(URL,ploads).json()['bustime-response']['prd']
    print(requests.get(URL,ploads).url)
    routes = [raw[x]['rt'] for x in range(len(raw))]
    times = [raw[x]['prdctdn'] for x in range(len(raw))]

    return routes,times

routes, times = getAllArrivalsAPI(['3140','8312'])
print(routes, times)
routes, times = getSpecificArrivalsAPI(['71B','71D'],['3140','8312'])
print(routes, times)