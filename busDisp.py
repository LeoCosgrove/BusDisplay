import urllib.request
import re

show_all_lines = 'on'
direction = 'INBOUND'

def getArrivals(bus_lines,stop_numbers):
    extracted_data, line_data, clean_data, time_data = [[],[],[],[]]

    # Scrape Port Authority website for departures and clean up into useable data
    for x in range(len(bus_lines)):
        URL = 'https://truetime.portauthority.org/bustime/wireless/html/eta.jsp?route=Port+Authority+Bus%3A'+bus_lines[x]+\
        '&direction=Port+Authority+Bus%3A'+direction+'&id=Port+Authority+Bus%3A'+stop_numbers[x]+'&showAllBusses='+show_all_lines

        with urllib.request.urlopen(URL) as response:
            html = response.read().decode('utf-8')

        extracted_data = re.findall('(?<=<strong class="larger">).*?(?=</strong>)',html)
        clean_data = [x.replace('&nbsp;', '').replace('#','').replace('MIN','').replace('DUE','0') for x in extracted_data]

        line_data += clean_data[::2]
        time_data += clean_data[1::2]

    # Convert time strings into ints for sorting
    time_data_int = [eval(x) for x in time_data]

    # Sort both lists by arrival time
    # Handle case of no buses coming
    try:
        time_data_sorted, line_data_sorted = map(list, zip(*sorted(zip(time_data_int,line_data), reverse=False)))
    except ValueError:
        time_data_sorted, line_data_sorted = [[],['None :(']]

    return line_data_sorted, time_data_sorted

apt_lines, apt_times = getArrivals(['71B','71D'],['3140','8312'])

# Replace 0 with DUE
apt_times = [x if x != 0 else 'DUE' for x in apt_times]

print(apt_lines)
print(apt_times)