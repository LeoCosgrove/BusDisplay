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
off_time_weekday = int(config.off_time_weekday_str.replace(":",""))
on_time_weekday = int(config.on_time_weekday_str.replace(":",""))
off_time_weekend = int(config.off_time_weekend_str.replace(":",""))
on_time_weekend = int(config.on_time_weekend_str.replace(":",""))

# Display setup message
setup_group = displayio.Group()
setup_msg = "Setting up..."
setup_msg_area = label.Label(font,text=setup_msg,color=0xFFFFFF)
setup_msg_area.x = 0
setup_msg_area.y = 4
setup_group.append(setup_msg_area)
display.show(setup_group)

# Gets current server time in 24 hr format ex. 23:24:43
# Usage: time = _get_time()
def _get_time() -> str:
    # Build URL for API call
    URL = 'http://truetime.portauthority.org/bustime/api/v3/_get_time?format=json&key='+key
    
    # Get XML response and parse
    response = mp.network.fetch(URL).json()['bustime-response']['tm']

    return response.split()[1]

# Gets current date ex. 20221031
# Usage: date = _get_date()
def _get_date() -> str:
    # Build URL for API call
    URL = 'http://truetime.portauthority.org/bustime/api/v3/_get_time?format=json&key='+key

    # Get XML response and parse
    response = mp.network.fetch(URL).json()['bustime-response']['tm']

    return response.split()[0]

# Gets certain bus lines and their predicted arrivals and stops
# ex. ['71D'], ['DUE'], ['INBOUND']
# Usage: routes, times, stops = _get_specific_arrivals(['71B','71D'],['3140','8312'])
def _get_specific_arrivals(bus_lines:list[str], stop_numbers:list[str]) -> tuple[list[str],list[str],list[str]]:
    # Convert list to csv string
    stop_num_str = ','.join(stop_numbers)
    bus_line_str = ','.join(bus_lines)

    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions?format=json&key='+key
    URL += "&stpid=" + stop_num_str
    URL += "&rtpidatafeed=" "Port Authority Bus"
    URL += "&rt=" + bus_line_str
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
# Usage: routes, times, stops = _get_all_arrivals(['3140','8312'])
def _get_all_arrivals(stop_numbers:list[str]) -> tuple[list[str],list[str],list[str]]:
    # Convert list to csv string
    stop_num_str = ','.join(stop_numbers)

    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions?format=json&key='+key
    URL += "&stpid=" + stop_num_str
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
def _update_text() -> None:
    text_group = displayio.Group()
    header = "LN  STOP  MIN"
    header_area = label.Label(font,text=header,color=colors[0])
    header_area.x = 0
    header_area.y = 4
    text_group.append(header_area)

    # Get data from api call
    if config.get_all_lines:
        routes, times, stops = _get_all_arrivals(config.stops_to_show)
    else:
        routes, times, stops = _get_specific_arrivals(config.lines_to_show,config.stops_to_show)

    if len(routes) == 0:
        # Add route to display (left aligned)
        no_route_msg = "No arrivals"
        no_route_area = label.Label(font,text=no_route_msg,color=colors[1])
        no_route_area.x = 0
        no_route_area.y = 12
        text_group.append(no_route_area)

    for i in range(len(routes)):
        # Add route to display (left aligned)
        route = routes[i]
        route_area = label.Label(font,text=route,color=colors[1])
        route_area.x = 0
        route_area.y = 4+(i+1)*8
        text_group.append(route_area)

        # Add destination to display
        stop = "    "+stops[i]
        stop_area = label.Label(font,text=stop,color=colors[1])
        stop_area.x = 0
        stop_area.y = 4+(i+1)*8
        text_group.append(stop_area)
        
        # Add time to display (right aligned)
        time = times[i]
        time_area = label.Label(font,text=time,color=colors[1],anchor_point=(1.0,0.0),anchored_position=(65,1+(i+1)*8))
        text_group.append(time_area)

    display.show(text_group)

# Returns whether the screen should be on based on network time
def _should_be_on() -> bool:
    today = _get_date()
    year = today[:4]
    month = today[4:6]
    day = today[6:8]
    today_date = date(int(year),int(month),int(day))
    day_num = today_date.isoweekday()

    if(config.friday_is_weekend):
        weekday = day_num <= 4
    else:
        weekday = day_num <= 5

    current_time = int(_get_time().replace(":",""))
    
    if(weekday):
        should_be_on = current_time in range(on_time_weekday,off_time_weekday)
    else:
        should_be_on = current_time in range(on_time_weekend,off_time_weekend)

    return should_be_on
    
# Clear the screen
def _blank_screen() -> None:
    text_group = displayio.Group()
    display.show(text_group)

# Main loop
while True:
    try:
        if(_should_be_on()):
            _update_text()
        else:
            _blank_screen()
    except:
        print("Error, retrying")
        continue

    gc.collect()
    time.sleep(15)