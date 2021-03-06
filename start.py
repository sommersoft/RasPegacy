#!/usr/bin/env python2
# RasPegacy - A Raspberry Pi Based System
# Author: Michael Schroeder (Code Borrows Cited in-line)
# LICENSE: UNDECIDED (Apache or MIT most likely)

import RPi.GPIO as GPIO
import socket
import random
import json
import time
import spidev
import subprocess
import sys
import Adafruit_BMP.BMP085 as BMP085
from multiprocessing import Process

# init constant value dict
cvalues = {"c_temp": None, "maf": None, "tps": None,
           "temp": None, "sbar_msg": None, "calc_load": None, "iat": None}

# Setup sock for UPD updates
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Setup BMP180 (aka BMP085)
BMPsensor = BMP085.BMP085(mode=BMP085.BMP085_HIGHRES)

# Setup spidev to talk to MCP3208
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000  #MCP3208 datasheet states to maintain at least 10kHz sample rate
spi.mode = 0b01
spi.bits_per_word = 8

# Create value lists for ploticus
li_boost = ['boost']
li_opress = ['opress']
#li_val1 = ['val1']
#acel_X = [''] # might move accelerometer vals
#acel_Y = [''] # to cvalues **kwarg list
#acel_Z = ['']

# Pin Assignments
btnCenter = 19
btnUp = 20
btnDown = 13
btnLeft = 16
btnRight = 12

# Setup GPIO 
GPIO.setmode(GPIO.BCM)
GPIO.setup(btnCenter, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btnUp, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btnDown, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btnLeft, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btnRight, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# First things first, get info-beamer running (view selected from main node)
# http://www.info-beamer.com/pi
beam = subprocess.Popen('exec nice -n -5 sudo /home/pi/info-beamer-pi/info-beamer /home/pi/RasPegacy/nodes', shell=True)
while True:
    a = beam.poll()
    if a == None:
        break

def send(data):
    ''' Function to handle socket.sendtos for info-beamer
        Original code from info-beamer '30c3-room' service.py
        https://github.com/dividuum/info-beamer-nodes/30c3-room
    '''
    sock.sendto(data, ('127.0.0.1', 4444))
    #print >>sys.stderr, "SENT >>> ", data
    
# Setup the OBDII connection; wait for a connection
print time.strftime('starting OBD: %H:%M')
import obd
print time.strftime('OBD imported: %H:%M')
send("status_bar/sbar/msg:" + "Initializing OBDII connection...")
obd.logger.setLevel(obd.logging.DEBUG)
print time.strftime('creating OBD object: %H:%M')
obdII = obd.OBD()
print time.strftime('OBD object created: %H:%M')
while not obdII.is_connected():
    try:
        if obdII.status() in ("Not Connected", "ELM Connected"):
            #print obdII.status()
            send("status_bar/sbar/msg:" + "OBDII Connection Failed. Check connections, and restart RasPegacy.")
            time.sleep(10)
            for i in range(5, 0, -1):
                send("status_bar/sbar/msg:" + "RasPegacy will shutdown in {0} seconds.".format(i))
                time.sleep(1)
            spi.close
            beam.terminate()
            exit()
        else:
            continue
    except KeyboardInterrupt:
        spi.close
        obdII.close
        beam.terminate()
        exit()
        
send("status_bar/sbar/msg:" + "OBDII connection established. ECU protocol: " + obdII.protocol_name())

def SendValues(boost, boost_needle, opress, opress_needle, **cvals):
    '''
        Function to send values to info-beamer
    '''
    #print "boost: ", str(boost), " boost needle:", str(boost_needle), " opress:", str(opress), " opress needle:", str(opress_needle)
    # send the current time
    clockmsg = time.strftime('menu/clock/clk:%H:%M')
    send(clockmsg)

    # send the interior temperature
    if cvals["temp"]: send("menu/clock/tmp:" + str(cvals["temp"]))
        
    # send the current status message
    if cvals["sbar_msg"]: send("status_bar/sbar/msg:" + str(cvals["sbar_msg"]))
    
    # send lower values (visible in all views)
    if cvals["c_temp"]: send("lower/set/coolant:" + str(cvals["c_temp"]))
    if cvals["maf"]: send("lower/set/maf:" + str(cvals["maf"]))
    if cvals["tps"]: send("lower/set/tps:" + str(cvals["tps"]))
    if cvals["calc_load"]: send("lower/set/calc_load:" + str(cvals["calc_load"]))
    if cvals["iat"]: send("lower/set/intake:" + str(cvals["iat"]))

    # check which view we're using, so we know how to "send" the data
    with open('/home/pi/RasPegacy/nodes/view.json') as data_file: #, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    result = data["view"]["top"]
    #print('result: ' + result)

    if result == "1": # round gauge view 
        # this view is updated directly to info-beamer by sending UDP packets to the "basic" node
        p = beam.poll()
        if p == None:
            send("gauge/boost/set:" + str(boost).rjust(5))
            send("gauge/boost/needle_rot:" + str(boost_needle))
            send("gauge/opress/set:" + str(opress).rjust(5))
            send("gauge/opress/needle_rot:" + str(opress_needle))
            send("gauge/val1/set:" + ("%2f" % random.random()).rjust(5))
            send("gauge/val1/needle_rot:" + str(random.random()))
        elif p <= 0:
            print ('Display system has stopped working. RasPegacy is shutting down.')
            exit()
    elif result == "2": # graphing view
        """
        this view is updated using ploticus images (PNG)
        http://ploticus.sourceforge.org/
        update value lists (first in first out)
        !! IS CURRENTLY TOO SLOW TO USE !! minplot is in work,
        but only supports SVG files
        """
        if len(li_boost) < 31:
            li_boost.append(boost)
        else:
            del li_boost[1]
            li_boost.append(boost)

        if len(li_opress) < 31:
            li_opress.append(random.randrange(120)) #opress)
        else:
            del li_opress[1]
            li_opress.append(random.randrange(120)) #opress)
        # add val1 updates if used

        # write value lists to file for ploticus and info-beamer
        with open('/home/pi/ploticus/dlog_boost', 'w') as f:
            for s in li_boost:
                f.write("%s\n" % (s))
        with open('/home/pi/ploticus/dlog_opress', 'w') as f:
            for s in li_opress:
                f.write("%s\n" % (s))

        # this might get changed to a UDP send for info-beamer update
        subprocess.Popen('cp /home/pi/ploticus/dlog_boost /home/pi/RasPegacy/nodes/graph/boost.txt', shell=True)

        # run ploticuses
        scrip = '/home/pi/ploticus/boostplot.pl'
        prun = subprocess.Popen('exec nice -n -5 sudo ploticus '
                                + scrip 
                                + ' -png -o /home/pi/RasPegacy/nodes/graph/boost.png', shell=True)

        scrip = '/home/pi/ploticus/opressplot.pl'
        prun2 = subprocess.Popen('exec nice -n -5 sudo ploticus '
                                + scrip
                                + ' -png -o /home/pi/RasPegacy/nodes/graph/opress.png', shell=True)
        while True:
            a = prun2.poll()
            if a == None:
                pass
            else:
                break
    elif result == "3": # this is the blocks view. send straight to info-beamer w/UDP
        p = beam.poll()
        if p == None:
            # make the numbers percentage compatible for the node.lua (x * 100 < .6,.8)
            send("blocks/boost/set:" + str(boost).rjust(5))
            send("blocks/opress/set:" + str(opress).rjust(5))
            send("blocks/val1/set:" + str(random.random()).rjust(5))
        elif p <= 0:
            print ('Display system has stopped working. RasPegacy is shutting down.')
            exit()

def Sense():
    '''
        Function to listen to sensors (BMP180, MCP3208, LIS3DH, ODBII).
        Will not run threaded so that it doesn't interfere with values being sent.
    '''

    try:
        for i in range(3000):
        # Read BMP180 (i2c)
            #C to F: C*1.8+32
            cels = BMPsensor.read_temperature()
            cvalues["temp"] = "%.0f" % (cels * 1.8 +32)
            #print temperature
            pascals = BMPsensor.read_pressure()
            #baro = "%.2f" % (0.000145038 * pascals)
            baro = (0.000145038 * pascals)
            
        # Read LIS3DH (i2c)
            #need to install python library
            
        # Read MCP3208 (SPI, 12bit base resolution)
            ''' Read pressure signal.  Sensor is a Honeywell PX2 Sealed Gauge,
                250PSIG operating pressure, 3.3v supply (Vss), with a Full
                Signal Scale ("FSS") of 10% - 90% Vss 
                (0.33v - 2.97v; 80% swing = 2.64v).
            
                Voltage equation is based on line slope intercept (y=mx+b).
                y=output, m = slope (range), x=input (signal) and b=offset.
                So, y=94.69(signal) + (-31.25)

                Since this is a Sealed Gauge, with a reference of 1atmA (14.7psi),
                the PSISG equation includes the barometric sensor value (BMP180 above)
                to offset the atmospheric pressure if used above sea-level.
            '''
            opress_raw = readMCP(0)
            if opress_raw < 409: opress_raw = 409
            opress_volt =  (opress_raw / 3685.5) * 2.97
            opress_PSIG = round((opress_volt * 94.7) - 31.25, 0)
            opress_final = round(opress_PSIG - (14.7 - baro), 0)   #adjust for current barometric pressure
            opress_needle = opress_final / 250   #get percentage for info-beamer needle

            #print ("%4d/3685.5 => %5.3f V => %d PSI" % (opress_raw, opress_volt, opress_PSIG))


        # Read OBDII signals (USB)
            if obdII.is_connected():
                if cvalues["sbar_msg"] == "OBDII connection lost...":
                    cvalues["sbar_msg"] = "OBDII connection re-established..."
                #elif cvalues["sbar_msg"] = "OBDII connection re-established..."
                else:
                    cvalues["sbar_msg"] = ""
                    
                cmd = (obd.commands.COOLANT_TEMP, obd.commands.MAF, obd.commands.THROTTLE_POS,
                       obd.commands.INTAKE_PRESSURE, obd.commands.ENGINE_LOAD,
                       obd.commands.INTAKE_TEMP)
                coolant, maf, tps, boost_val, calc_load, iat = obdII.query_multi(*cmd)
                '''
                    BOOST
                    needle angle calculation (MIN = baro * -1, MAX = 20): P = [boost - MIN] / [MAX - MIN]
                    example: boost = -5.06, baro = 14.7 || [-5.06 - -14.7](9.64) / [20 - -14.7](34.7) = 0.277 (0.28)
                    info-beamer glRotate would look like this: (-135 + 271 * 0.28) = 38.08
                '''
                #boost = random.randrange(-11, 17)
                boost = "{0:-.2f}".format((boost_val.value.to("psi").magnitude) - baro)
                boost_pre = (boost_val.value.to("psi").magnitude - (baro * -1)) / (20 - (baro * -1))
                #print "boost_pre:(", boost," - ", (baro * -1), " / 20 - ", (baro * -1), " = ", format(boost_pre, '.2f')
                boost_needle = "{0:.2f}".format(boost_pre)

                # coolant temp
                cvalues["c_temp"] = "{0:.0f}F".format(coolant.value.to("degF").magnitude)

                # maf
                cvalues["maf"] = "{0:.2f} g/s".format(maf.value.magnitude)

                # tps
                cvalues["tps"] = "{0:.0g}%".format(tps.value.magnitude)
                
                # calculate load
                cvalues["calc_load"] = "{0:.0g}%".format(calc_load.value.magnitude)
                
                # intake air temp
                cvalues["iat"] = "{0:.0f}F".format(iat.value.to("degF").magnitude)
                
            else:
                cvalues["sbar_msg"] = "OBDII connection lost..."
            
            
        #Send 'em!
            SendValues(boost, boost_needle, opress_final, opress_needle, **cvalues)
            time.sleep(0.5)

    except KeyboardInterrupt:
        btns.join()
        spi.close
        obdII.close
        return
    
    btns.join()
    spi.close
    obdII.close
    exit()

def readMCP(channel):
    '''
        Function to read data from the MCP3208
        Original function was written by Jeremy Blythe, and can
        be found at: https://github.com/jerbly/Pi
        I changed the xfer bytes construction to work the the 12bit
        MCP3204/MCP3208 (MCP32xx). Current version only works with
        single-ended samples; differential is not constructed.
    '''
    #if ((channel > 3) or (channel < 0)):   #MCP3204
    if ((channel > 7) or (channel < 0)):   #MCP3208
        return -1

    '''
        Construct the xfer bytes. MCP32xx pads Byte1 with 5 zeroes
        before the start bit. SNG/DIFF & D2 bits trail the start bit,
        and D1 & D0 bits are the first two bits of Byte2. All bits after
        D0 are "Don't Care" bits.
    '''
    byt1 = 6 if channel < 4 else 7   # Only matters for MCP3208; MCP3204 works w/ both
    byt2 = {0: '0', 1: '64', 2: '128', 3: '192', 4: '0', 5: '64', 6: '128', 7: '192'}

    # Take 10 samples to get an average, and send the smoothed out
    smooth = []
    for i in range(10):
        r = spi.xfer2([byt1, int(byt2[channel]), 0])
        # The MCP32xx responds with samples starting at the 5th bit in Byte2, so we & and shift
        # accordingly.
        adcout = ((r[1]&5) << 8) + r[2]
        smooth.append(adcout)
        time.sleep(0.001)
    tadaa = sum(smooth) / len(smooth)
    #print smooth, tadaa

    return tadaa

def Buttons():
    '''
        Function to listen to button pushes. Will set menu items
        by updating JSON file. Will run threaded for duration
        of program.
    '''
    while True:
        global result
        action = 'action'
        vselected = 'no'
        menu_step1 = ' '
        menu_step2 = ' '
        menu_step3 = ' '
        try:
            if not GPIO.input(btnCenter):
                action = 'select'
            elif not GPIO.input(btnUp):
                action = 'up'
            elif not GPIO.input(btnDown):
                action = 'down'
            elif not GPIO.input(btnLeft):
                action = 'left'
            elif not GPIO.input(btnRight):
                action = 'right'
            else:
                action = 'err0r'
            
            if action != 'err0r' and action != 'action':
                with open('/home/pi/RasPegacy/nodes/menu/menu.json') as menu_file:#, encoding='utf-8') as menu_file:
                    data = json.loads(menu_file.read())
                menu_step1 = data["current"]["step1"]
                if menu_step1 == '0': # step1 '0' = main menu
                    if action == 'right':
                        menu_step1 = '1'
                        menu_step2 = '0'
                        menu_step3 = '0'
                elif menu_step1 == '1': # step1 '1' = 'view'; '2' = 'about'
                    menu_step2 = data["current"]["step2"]
                    if menu_step2 == '0': # step2 '0' = 'view'
                        if action == 'right':
                            menu_step2 = '1'
                        elif action == 'left':
                            menu_step1 = '0'
                    else: # step2 '1' = 'hollow'; '2' = 'glow'; '3' = 'graph'; '4' = blocks
                        menu_step3 = data["current"]["step3"]
                        if menu_step3 == '0': # step3 '1' = blue; '2' = red; '3' = green; '4' = cherry blossom
                            if action == 'down':
                                if int(menu_step2) < 4:
                                    menu_step2 = str(int(menu_step2) + 1)
                            elif action == 'up':
                                if int(menu_step2) > 1:
                                    menu_step2 = str(int(menu_step2) - 1)
                            elif action == 'select':
                                if int(menu_step2) > 2:
                                    if menu_step2 == '3':
                                        whoami = '2'
                                    elif menu_step2 == '4':
                                        whoami = '3'
                                    d_write = {'view':({'top': whoami})}
                                    with open('/home/pi/RasPegacy/nodes/view.json', 'w') as f:
                                        f.write(json.dumps(d_write, sort_keys=False, indent=4))
                                    menu_step1 = '0'
                                    menu_step2 = '0'
                                    menu_step3 = '0'
                            if action == 'right':
                                if int(menu_step2) < 3:
                                    menu_step3 = '1'
                            elif action == 'left':
                                menu_step2 = '0'
                        else:
                            if action == 'down':
                                if int(menu_step3) < 4:
                                    menu_step3 = str(int(menu_step3) + 1)
                            elif action == 'up':
                                if int(menu_step3) > 1:
                                    menu_step3 = str(int(menu_step3) - 1)
                            elif action == 'select':
                                    # write it!
                                    vselected = 'yes'
                                    if int(menu_step1) > 0:
                                        d_write = {'view':({'top': menu_step1, 'mid': menu_step2, 'color': menu_step3})}
                                        with open('/home/pi/RasPegacy/nodes/basic/view.json', 'w') as f:
                                            f.write(json.dumps(d_write, sort_keys=False, indent=4))
                                        d_write = {'view':({'top':'1'})}
                                        with open('/home/pi/RasPegacy/nodes/view.json', 'w') as f:
                                            f.write(json.dumps(d_write, sort_keys=False, indent=4))
                                    menu_step1 = '0'
                                    menu_step2 = '0'
                                    menu_step3 = '0'
                            elif action == 'left':
                                    menu_step3 = '0'
                if menu_step2 == ' 'or menu_step2 == None:
                    menu_step2 = '0'
                if menu_step3 == ' ' or menu_step3 == None:
                    menu_step3 = '0'

                d_write = {'current':({'step1': menu_step1, 'step2': menu_step2, 'step3': menu_step3})}
                #print(json.dumps(d_write, sort_keys=True, indent=4))
                with open('/home/pi/RasPegacy/nodes/menu/menu.json', 'w') as f:
                    f.write(json.dumps(d_write, sort_keys=True, indent=4))

            time.sleep(0.15)

        except KeyboardInterrupt or SystemExit:
            GPIO.cleanup()
            break

##Main script init
if __name__ == "__main__":
    send("status_bar/sbar/msg:" + "Initializing Display & Sensor Array...")
    btns = Process(target=Buttons)
    btns.start()
    Sense()
