import adafruit_requests as requests
import board
import busio
from adafruit_esp32spi import adafruit_esp32spi
from digitalio import DigitalInOut
import adafruit_esp32spi.adafruit_esp32spi_socket as socket

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

# implement methods here

routes, times = getAllArrivals(['3140','8312'])
print(routes,times)
