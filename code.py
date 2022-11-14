import board
import config
import time
from adafruit_datetime import date
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.matrixportal import MatrixPortal
from adafruit_display_text import label
import gc
import displayio
import framebufferio
import rgbmatrix

# Get wifi details and api key from secrets.py file
try:
    from secrets import secrets
    key = secrets.get('BUSTIME_API_KEY')
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# Initialize board
mp = MatrixPortal(status_neopixel=board.NEOPIXEL,debug=False)
displayio.release_displays()

# Define matrix pins and objects
matrix = rgbmatrix.RGBMatrix(
    width=64,
    height=32,
    bit_depth=3,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2,
    ],
    addr_pins=[board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE,
)
display = framebufferio.FramebufferDisplay(matrix)
font = bitmap_font.load_font("5x7.bdf")
colors = [0xFF0000, 0xFF7500]
offTimeWD = int(config.offTimeWDstr.replace(":",""))
onTimeWD = int(config.onTimeWDstr.replace(":",""))
offTimeWE = int(config.offTimeWEstr.replace(":",""))
onTimeWE = int(config.onTimeWEstr.replace(":",""))

# Display setup message
setupGroup = displayio.Group()
setupMsg = "Setting up..."
setupMsg_area = label.Label(font,text=setupMsg,color=0xFFFFFF)
setupMsg_area.x = 0
setupMsg_area.y = 4
setupGroup.append(setupMsg_area)
display.show(setupGroup)

# Gets current server time in 24 hr format ex. 23:24:43
# Usage: time = getTime()
def getTime() -> str:
    # Build URL for API call
    URL = 'http://truetime.portauthority.org/bustime/api/v3/gettime?format=json&key='+key
    
    # Get XML response and parse
    response = mp.network.fetch(URL).json()['bustime-response']['tm']

    return response.split()[1]

# Gets current date ex. 20221031
# Usage: date = getDate()
def getDate() -> str:
    # Build URL for API call
    URL = 'http://truetime.portauthority.org/bustime/api/v3/gettime?format=json&key='+key

    # Get XML response and parse
    response = mp.network.fetch(URL).json()['bustime-response']['tm']

    return response.split()[0]

# Gets certain bus lines and their predicted arrivals and stops
# ex. ['71D'], ['DUE'], ['INBOUND']
# Usage: routes, times, stops = getSpecificArrivals(['71B','71D'],['3140','8312'])
def getSpecificArrivals(busLines:list[str], stopNumbers:list[str]) -> tuple[list[str],list[str],list[str]]:
    # Convert list to csv string
    stopNumString = ','.join(stopNumbers)
    busLineString = ','.join(busLines)

    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions?format=json&key='+key
    URL += "&stpid=" + stopNumString
    URL += "&rtpidatafeed=" "Port Authority Bus"
    URL += "&rt=" + busLineString
    URL += "&top=3"

    # Get XML response and parse
    try:
        response = mp.network.fetch(URL).json()['bustime-response']['prd']
        routes = [x['rt'] for x in response]
        times = [x['prdctdn'] for x in response]
        stops = [x['stpid'] for x in response]
    except:
        routes = []
        times = []
        stops = []

    return routes, times, stops

# Gets all bus lines and their predicted arrivals and stops
# ex. ['71D'], ['DUE'], ['INBOUND']
# Usage: routes, times, stops = getAllArrivals(['3140','8312'])
def getAllArrivals(stopNumbers:list[str]) -> tuple[list[str],list[str],list[str]]:
    # Convert list to csv string
    stopNumString = ','.join(stopNumbers)

    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions?format=json&key='+key
    URL += "&stpid=" + stopNumString
    URL += "&rtpidatafeed=" "Port Authority Bus"
    URL += "&top=3"

    # Get XML response and parse
    try:
        response = mp.network.fetch(URL).json()['bustime-response']['prd']
        routes = [x['rt'] for x in response]
        times = [x['prdctdn'] for x in response]
        stops = [x['stpid'] for x in response]
    except:
        routes = []
        times = []
        stops = []

    return routes, times, stops

# Refresh the arrivals and print to LED matrix
def updateText() -> None:
    textGroup = displayio.Group()
    header = "LN  STOP  MIN"
    headerArea = label.Label(font,text=header,color=colors[0])
    headerArea.x = 0
    headerArea.y = 4
    textGroup.append(headerArea)

    # Get data from api call
    if config.getAllLines:
        routes, times, stops = getAllArrivals(config.stopsToShow)
    else:
        routes, times, stops = getSpecificArrivals(config.linesToShow,config.stopsToShow)

    if len(routes) == 0:
        # Add route to display (left aligned)
        noRouteMsg = "No arrivals"
        noRouteArea = label.Label(font,text=noRouteMsg,color=colors[1])
        noRouteArea.x = 0
        noRouteArea.y = 12
        textGroup.append(noRouteArea)

    for i in range(len(routes)):
        # Add route to display (left aligned)
        route = routes[i]
        routeArea = label.Label(font,text=route,color=colors[1])
        routeArea.x = 0
        routeArea.y = 4+(i+1)*8
        textGroup.append(routeArea)

        # Add destination to display
        stop = "    "+stops[i]
        stopArea = label.Label(font,text=stop,color=colors[1])
        stopArea.x = 0
        stopArea.y = 4+(i+1)*8
        textGroup.append(stopArea)
        
        # Add time to display (right aligned)
        time = times[i]
        timeArea = label.Label(font,text=time,color=colors[1],anchor_point=(1.0,0.0),anchored_position=(65,1+(i+1)*8))
        textGroup.append(timeArea)

    display.show(textGroup)

# Returns whether the screen should be on based on network time
def shouldBeOn() -> bool:
    today = getDate()
    year = today[:4]
    month = today[4:6]
    day = today[6:8]
    todayDate = date(int(year),int(month),int(day))
    dayNum = todayDate.isoweekday()

    if(config.fridayIsWeekend):
        weekday = dayNum <= 4
    else:
        weekday = dayNum <= 5

    currentTime = int(getTime().replace(":",""))
    
    if(weekday):
        shouldBeOn = currentTime in range(onTimeWD,offTimeWD)
    else:
        shouldBeOn = currentTime in range(onTimeWE,offTimeWE)

    return shouldBeOn
    
# Clear the screen
def blankScreen() -> None:
    textGroup = displayio.Group()
    display.show(textGroup)

# Main loop
while True:
    try:
        if(shouldBeOn()):
            updateText()
        else:
            blankScreen()
    except:
        print("Error, retrying")
        continue

    gc.collect()
    time.sleep(15)