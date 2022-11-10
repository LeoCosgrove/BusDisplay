import board
import time
from adafruit_matrixportal.matrixportal import MatrixPortal

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
    key = secrets.get('BUSTIME_API_KEY')
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Set up board
mp = MatrixPortal(status_neopixel=board.NEOPIXEL,debug=False)

# Gets current server time in 24 hr format ex. 23:24:43
# Usage: time = getTime()
def getTime():
    # Build URL for API call
    URL = 'http://truetime.portauthority.org/bustime/api/v3/gettime?format=json&key='+key
    
    # Get XML response and parse
    raw = mp.network.fetch(URL).json()['bustime-response']['tm']

    return raw.split()[1]

# Gets current date ex. 20221031
# Usage: date = getDate()
def getDate():
    # Build URL for API call
    URL = 'http://truetime.portauthority.org/bustime/api/v3/gettime?format=json&key='+key

    # Get XML response and parse
    raw = mp.network.fetch(URL).json()['bustime-response']['tm']

    return raw.split()[0]

# Gets all buses and their predicted arrivals and directions at specified stops
# ex. ['71D', '64'], ['DUE', '5'], ['INBOUND', 'INBOUND']
# Usage: routes, times, directions = getAllArrivals(['3140','8312'])
def getAllArrivals(stop_numbers):
    # Convert list to csv string
    stop_numbers_string = ','.join(stop_numbers)

    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions?format=json&key='+key
    URL += "&stpid=" + stop_numbers_string
    URL += "&rtpidatafeed=" "Port Authority Bus"

    # Get XML response and parse
    try:
        raw = mp.network.fetch(URL).json()['bustime-response']['prd']
        routes = [x['rt'] for x in raw]
        times = [x['prdctdn'] for x in raw]
        directions = [x['rtdir'] for x in raw]
    except:
        routes = []
        times = []
        directions = []

    return routes, times, directions


# Gets certain bus lines and their predicted arrivals and directions at specified stops
# ex. ['71D'], ['DUE'], ['INBOUND']
# Usage: routes, times, directions = getSpecificArrivals(['71B','71D'],['3140','8312'])
def getSpecificArrivals(bus_lines, stop_numbers):
    # Convert list to csv string
    stop_numbers_string = ','.join(stop_numbers)
    bus_lines_string = ','.join(bus_lines)

    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions?format=json&key='+key
    URL += "&stpid=" + stop_numbers_string
    URL += "&rtpidatafeed=" "Port Authority Bus"
    URL += "&rt=" + bus_lines_string

    # Get XML response and parse
    try:
        raw = mp.network.fetch(URL).json()['bustime-response']['prd']
        routes = [x['rt'] for x in raw]
        times = [x['prdctdn'] for x in raw]
        directions = [x['rtdir'] for x in raw]
    except:
        routes = []
        times = []
        directions = []

    return routes, times, directions

# Colors for header and arrivals
colors = [0xFF0000, 0xFF00FF]
FONT = '/IBMPlexMono-Medium-24_jep.bdf'

mp.add_text(
    text_font=FONT,
    text_position=(
        (mp.graphics.display.width // 2),
        (mp.graphics.display.height // 2),
    ),
    scrolling=True,
)

mp.set_text('hello world',0)

while True:
    print(getAllArrivals(['3140','8312']))
    print(getSpecificArrivals(['71B','71D'],['3140','8312']))
    time.sleep(1)