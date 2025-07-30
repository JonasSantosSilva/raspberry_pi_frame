# Project title: GPS 0.2
# Code functionality: Handle and store location data.
# Author: Jonas dos Santos Silva
# Start Date: 25/08/2021
# Release Date:

# Sequential Message Identifier Field is not implemented

# ######################################### Imports ####################################################################

import serial
from time import sleep
import datetime
import logging
import webbrowser
# import webbrowser, os, sys

# ######################################### Settings ###################################################################

port = "/dev/ttyS0"
baud = 9600

# ######################################### Global Variables ###########################################################

raw_lat = 0
north_south = 'N'
raw_lon = 0
west_east = 'E'

# ######################################### Functions ##################################################################

def serial_read(ser):
    input_data = ser.read()              # read serial port
    sleep(0.03)
    data_left = ser.inWaiting()             # check for remaining byte
    input_data += ser.read(data_left)
    return input_data


def serial_write_string(ser, string, print_console=False, new_line = True):
    if print_console:
        print(string)
    for x in string:
        ser.write(bytes(x, 'utf-8'))
    if (new_line):
        ser.write(bytes("\n", 'utf-8'))


# helpers
def num(x): 
    try: return int(x)
    except: return 0


# parse code
def parse_gptxt(p):
    logging.info({0:"ERROR",1:"WARNING",2:"NOTICE",7:"USER"}[num(p[3])]+" "+p[4])


def parse_gpgll(p):
    # $GPGLL,Latitude,N,Longitude,E,hhmmss.ss,Valid,Mode*cs<CR><LF>
    if p[6] != "" and (p[6] == "A" or p[6] == "D"):
        logging.info("GLL:")
        logging.info("  lat: "+p[1]+" "+p[2])
        logging.info("  lon: "+p[3]+" "+p[4])
        logging.info("  time: "+p[5])


def parse_rmc(p):
    # $GPRMC,hhmmss,status,latitude,N,longitude,E,spd,cog,ddmmyy,mv,mvE,mode*cs<CR><LF>
    if p[2] == "A": # status valid
        logging.info("RMC:")
        logging.info("  time: "+p[1])
        logging.info("  lat: "+p[3]+" "+p[4])
        logging.info("  lon: "+p[5]+" "+p[6])
        logging.info("  speed: "+p[7]+" knots")
        logging.info("  cog: "+p[8]+" deg")
        logging.info("  date: "+p[9])
        
        global raw_lat
        global north_south
        global raw_lon
        global west_east
        
        raw_lat = p[3]
        print(f"raw_lat: {raw_lat} | type {type(raw_lat)}")
        north_south = p[4]   
        raw_lon = p[5]
        print(f"\t\t\t\t\t\traw_lon: {raw_lon} | type {type(raw_lon)}")
        west_east = p[6]


def parse_gpvtg(p):
    # $GPVTG,cogt,T,cogm,M,sog,N,kph,K,mode*cs<CR><LF>
    if p[7] != "":
        logging.info("VTG:")
        logging.info("  cogt: "+p[1])
        logging.info("  sog: "+p[5]+" knots")
        logging.info("  sog: "+p[7]+" km/h")


def parse_gpgga(p):
    # $GPGGA,hhmmss.ss,Latitude,N,Longitude,E,FS,NoSV,HDOP,msl,m,Altref,m,DiffAge,DiffStation*cs<CR><LF>
    if p[7] != "" and num(p[7]) > 0 and p[6] != "" and num(p[6]) > 0: # fix is valid
        logging.info("GGA:")
        logging.info("  time: "+p[1])
        logging.info("  lat: "+p[2]+" "+p[3])
        logging.info("  lon: "+p[4]+" "+p[5])
        logging.info("  fix: "+p[6])
        logging.info("  sat: "+str(num(p[7])))


def parse_gsa(p):
    # $GPGSA,Smode,FS{,sv},PDOP,HDOP,VDOP*cs<CR><LF>
    if p[2] != "" and num(p[2]) > 1: # fix is valid
        logging.info("GSA:")
        logging.info("  sat: "+str(sum([1 for i in range(12) if p[3+i]!=""])))


def parse_gpgsv(p):
    # $GPGSV,NoMsg,MsgNo,NoSv,{,sv,elv,az,cno}*cs<CR><LF>
    if p[2] != "" and num(p[2]) == 1:
        logging.info("GSV:")
        logging.info("  sat: "+str(num(p[3])))


# known NMEA messages (parameter number, handler f-tion)
messages = {
    "$GPTXT":[5, parse_gptxt],
    "$GPRMC":[12, parse_rmc],
    "$GPVTG":[10, parse_gpvtg],
    "$GPGGA":[15, parse_gpgga],
    "$GPGSA":[18, parse_gsa],
    "$GPGSV":[14, parse_gpgsv],
    "$GPGLL":[8, parse_gpgll],
}


def chksum(inp): # message checksum verification
    if not inp.startswith("$"): return False
    if not inp[-3:].startswith("*"): return False
    payload = inp[1:-3]
    checksum = 0
    for i in range(len(payload)):
        checksum =  checksum ^ ord(payload[i])
    return ("%02X" % checksum) == inp[-2:]


def parse_nmea(parts):
    if len(parts) <= 0: return
    id = parts[0].upper()
    
    if id in messages:
        if len(parts) < messages[id][0]:
            parts.extend(["" for e in range(messages[id][0]-len(parts))])
        messages[id][1](parts)
    else:
        logging.info("Unknown GPS data: "+parts)


def serial_greeting(ser):
    serial_write_string(ser, "")
    serial_write_string(ser, "Project title: GPS1", True)
    serial_write_string(ser, "Code functionality: Handle and store location data.", True)
    serial_write_string(ser, "Date/Time:" + now.strftime("%Y-%m-%d %H:%M:%S") + "\n", True)


def coordinates_for_googlemap():
    global raw_lat
    global north_south
    global raw_lon
    global west_east
    lat = 60 * float("0" + raw_lat[4:10])
    lon = 60 * float("0" + raw_lon[5:11])
    coordinates = f"{raw_lat[0:2]}°{raw_lat[2:4]}'{lat:.1f}\"{north_south} {raw_lon[0:3]}°{raw_lon[3:5]}'{lon:.1f}\"{west_east}"
    return coordinates


def main():
    logging.basicConfig(filename='nmea.log',level=logging.DEBUG,format="%(asctime)s [%(levelname)s] %(message)s")   
    ser = serial.Serial(port, baud)
    # sleep(0.1)
    now = datetime.datetime.now()
    # serial_greeting(ser)
    count = 20
    while count:
        line = ser.readline()
        line = line.strip()
        
        line = line.decode("utf-8") # Jonas
        
        logging.info("Received: " + line)
        
        if not chksum(line):
            logging.error("INVALID checksum: "+line)
        else:
            parse_nmea(line[:-3].split(","))
        count = count - 1
        
    ser.close()
    url_base = "https://www.google.com/maps/place/"
#    location = "-33.907759726570895, 151.22992686943724"
    print("Final Coordinates: ", coordinates_for_googlemap())
    webbrowser.open(url_base + coordinates_for_googlemap(), new=1)


# ######################################### Main Code ##################################################################
if __name__ == "__main__":
    main()
    print("GPS_03.py end")
#     try:
#         main()
#     finally:
#         ser.close()
