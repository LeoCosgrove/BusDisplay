from time import time
import urllib.request
import re
import numpy as np

bus_line = ['71B','71D']
stop_number = ['3140','8312']
direction = 'INBOUND'
extracted_data, line_data, clean_data, line_data, time_data = [[],[],[],[],[]]

# Scrape Port Authority website for departures and clean up into useable data
for x in range(len(bus_line)):
    URL = 'https://truetime.portauthority.org/bustime/wireless/html/eta.jsp?route=Port+Authority+Bus%3A'+bus_line[x]+\
    '&direction=Port+Authority+Bus%3A'+direction+'&id=Port+Authority+Bus%3A'+stop_number[x]+'&showAllBusses=on'

    print(URL)

    with urllib.request.urlopen(URL) as response:
        html = response.read().decode('utf-8')

    extracted_data = re.findall('(?<=<strong class="larger">).*?(?=</strong>)',html)
    clean_data = [x.replace('&nbsp;', '').replace('#','').replace('MIN','') for x in extracted_data]

    line_data += clean_data[::2]
    time_data += clean_data[1::2]

# Sort both lists by arrival time
time_data_s, line_data_s = map(list, zip(*sorted(zip(time_data,line_data), reverse=True)))
print(line_data_s)
print(time_data_s)

#format: 8&nbsp;MIN
#if no buses are scheduled, extracted_time = None
#if due, instead of 8&nbsp;MIN, it is DUE
