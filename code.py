import board
import busio
import time
from digitalio import DigitalInOut
import neopixel
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
    key = secrets.get('BUSTIME_API_KEY')
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

# Define pins
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.2
) 

# Set up wifi connection
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

# Gets current server time in 24 hr format ex. 23:24:43
# Usage: time = getTime()
def getTime():
    # Build URL for API call
    URL = 'http://truetime.portauthority.org/bustime/api/v3/gettime?format=json&key='+key
    
    # Get XML response and parse
    raw = wifi.get(URL).json()['bustime-response']['tm']

    return raw.split()[1]

# Gets current date ex. 20221031
# Usage: date = getDate()
def getDate():
    # Build URL for API call
    URL = 'http://truetime.portauthority.org/bustime/api/v3/gettime?format=json&key='+key

    # Get XML response and parse
    raw = wifi.get(URL).json()['bustime-response']['tm']

    return raw.split()[0]

while True:
    print(getTime())
    time.sleep(2)
