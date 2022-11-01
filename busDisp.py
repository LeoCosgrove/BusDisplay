from msilib.schema import Directory
import os
import requests

key = os.getenv('BUSTIME_API_KEY')

# Access data through the official Port Authority API
# Gets all buses and their predicted arrivals and directions at specified stops
# Usage: routes, times, directions = getAllArrivals(['3140','8312'])
def getAllArrivals(stop_numbers):
    # Convert list to csv string
    stop_numbers_string = ','.join(stop_numbers)

    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions'
    ploads = {'key':key,
            'stpid':stop_numbers_string,
            'format':'json',
            'rtpidatafeed':'Port Authority Bus'}

    # Get XML response and parse
    raw = requests.get(URL,ploads).json()['bustime-response']['prd']
    routes = [x['rt'] for x in raw]
    times = [x['prdctdn'] for x in raw]
    directions = [x['rtdir'] for x in raw]

    return routes,times,directions


# Access data through the official Port Authority API
# Gets certain bus lines and their predicted arrivals and directions at specified stops
# Usage: routes, times, directions = getSpecificArrivals(['71B','71D'],['3140','8312'])
def getSpecificArrivals(bus_lines,stop_numbers):
    # Convert list to csv string
    stop_numbers_string = ','.join(stop_numbers)
    bus_lines_string = ','.join(bus_lines)

    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions'
    ploads = {'key':key,
            'stpid':stop_numbers_string,
            'format':'json',
            'rtpidatafeed':'Port Authority Bus',
            'rt':bus_lines_string}

    # Get XML response and parse
    raw = requests.get(URL,ploads).json()['bustime-response']['prd']
    routes = [x['rt'] for x in raw]
    times = [x['prdctdn'] for x in raw]
    directions = [x['rtdir'] for x in raw]

    return routes,times,directions


def getTime():
    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/gettime'
    ploads = {'key':key,
            'format':'json'}
        
    # Get XML response and parse
    raw = requests.get(URL,ploads).json()['bustime-response']['tm']

    return raw.split()[1]

def getDate():
    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/gettime'
    ploads = {'key':key,
            'format':'json'}
        
    # Get XML response and parse
    raw = requests.get(URL,ploads).json()['bustime-response']['tm']

    return raw.split()[0]

print(getDate())