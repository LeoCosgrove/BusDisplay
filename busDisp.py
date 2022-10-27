from time import time
import urllib.request
import re
import numpy as np

show_all_lines = 'off'
bus_line = ['71B','71D']
stop_number = ['3140','8312']
direction = 'INBOUND'
extracted_data, line_data, clean_data, line_data, time_data = [[],[],[],[],[]]

# Scrape Port Authority website for departures and clean up into useable data
for x in range(len(bus_line)):
    URL = 'https://truetime.portauthority.org/bustime/wireless/html/eta.jsp?route=Port+Authority+Bus%3A'+bus_line[x]+\
    '&direction=Port+Authority+Bus%3A'+direction+'&id=Port+Authority+Bus%3A'+stop_number[x]+'&showAllBusses='+show_all_lines

    with urllib.request.urlopen(URL) as response:
        html = response.read().decode('utf-8')

    extracted_data = re.findall('(?<=<strong class="larger">).*?(?=</strong>)',html)
    clean_data = [x.replace('&nbsp;', '').replace('#','').replace('MIN','').replace('DUE','0') for x in extracted_data]

    line_data += clean_data[::2]
    time_data += clean_data[1::2]

# Convert time strings into ints for sorting
time_data_int = [eval(x) for x in time_data]

# Sort both lists by arrival time
try:
    time_data_sorted, line_data_sorted = map(list, zip(*sorted(zip(time_data_int,line_data), reverse=False)))
except:
    time_data_sorted, line_data_sorted = [[],['None :(']]

print(line_data_sorted)
print(time_data_sorted)