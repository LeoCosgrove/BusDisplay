import adafruit_requests as requests
import board
import busio
from adafruit_esp32spi import adafruit_esp32spi
from digitalio import DigitalInOut
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
import xml.etree.ElementTree as ET

# get wifi details from secrets files
try:
    from secrets import secrets
except ImportError:
    print('WiFi secrets are kept in secrets.py, please add them there!')
    raise

esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue

socket.set_interface(esp)
requests.set_socket(socket, esp)

key = secrets["BUSTIME_API_KEY"]

# Access data through the official Port Authority API
# Gets all buses and their predicted arrivals at specified stops
def getAllArrivalsAPI(stop_numbers):
    # Convert list to csv string
    stop_numbers_string = ','.join(stop_numbers)

    # Build URL for API call
    URL = 'https://truetime.portauthority.org/bustime/api/v3/getpredictions?key='+key+'&rtpidatafeed=Port%20Authority%20Bus&stpid='+stop_numbers_string

    # Get XML response and parse
    XML = requests.get(URL)
    root = ET.fromstring(XML)

    # Extract necessary data from parsed XML
    routes, times = [[],[]]
    for bus in root.findall('prd'):
        routes.append(bus.find('rt').text)
        times.append(bus.find('prdctdn').text)
    
    return routes,times

routes, times = getAllArrivalsAPI(['3140','8312'])
print(routes,times)
