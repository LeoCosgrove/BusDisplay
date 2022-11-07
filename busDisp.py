import os
import requests

key = os.getenv('BUSTIME_API_KEY')

# Gets all buses and their predicted arrivals and directions at specified stops
# ex. ['71D', '64'], ['DUE', '5'], ['INBOUND', 'INBOUND']
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
    try:
        raw = requests.get(URL,ploads).json()['bustime-response']['prd']
        routes = [x['rt'] for x in raw]
        times = [x['prdctdn'] for x in raw]
        directions = [x['rtdir'] for x in raw]
    except:
        routes = ['No Arrivals :(']
        times = []
        directions = []

    return routes,times,directions

# Gets certain bus lines and their predicted arrivals and directions at specified stops
# ex. ['71D'], ['DUE'], ['INBOUND']
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
    try:
        raw = requests.get(URL,ploads).json()['bustime-response']['prd']
        routes = [x['rt'] for x in raw]
        times = [x['prdctdn'] for x in raw]
        directions = [x['rtdir'] for x in raw]
    except:
        routes = ['No Arrivals :(']
        times = []
        directions = []
    
    return routes,times,directions

# Gets current server time in 24 hr format ex. 23:24:43
# Usage: time = getTime()
def getTime():
    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/gettime'
    ploads = {'key':key,
            'format':'json'}
        
    # Get XML response and parse
    raw = requests.get(URL,ploads).json()['bustime-response']['tm']

    return raw.split()[1]

# Gets current date ex. 20221031
# Usage: date = getDate()
def getDate():
    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/gettime'
    ploads = {'key':key,
            'format':'json'}
        
    # Get XML response and parse
    raw = requests.get(URL,ploads).json()['bustime-response']['tm']

    return raw.split()[0]

print(getSpecificArrivals(['71B','71D'],['3140','8312']))
print(getAllArrivals(['3140','8312']))