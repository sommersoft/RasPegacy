#!/usr/bin/env python3
# RasPegacy - A Raspberry Pi Based System
# Author: Michael Schroeder (Code Borrows Cited in-line)
# LICENSE: UNDECIDED (Apache or MIT most likely)


#Imports
import spidev, time

#Setup spidev to talk to MCP3208
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 15600
spi.mode = 0b01
spi.bits_per_word = 8

#Function to read data from the MCP3208
#Original function was written by Jeremy Blythe, and can be found at: https://github.com/jerbly/Pi
#I changed the xfer bytes construction to work the the 12bit MCP3204/MCP3208 (MCP32xx).
#Current version only works with single-ended samples; differential is not constructed.
def readMCP(channel):
    #if ((channel > 3) or (channel < 0)):   #MCP3204
    if ((channel > 7) or (channel < 0)):   #MCP3208
        return -1

    #Construct the xfer bytes. MCP32xx pads Byte1 with 5 zeroes before the start bit
    #SNG/DIFF & D2 bits trail the start bit, and D1 & D0 bits are the first two bits of Byte2
    #All bits after D0 are "Don't Care" bits.
    byt1 = 6 if channel < 4 else 7   #Only for MCP3208; MCP3204 lists bit D2 as "Don't Care"
    byt2 = {0: '0', 1: '64', 2: '128', 3: '192', 4: '0', 5: '64', 6: '128', 7: '192'}

    #Take 10 samples to get an average, and send the smoothed out
    smooth = []
    for i in range(10):
        #r = spi.xfer2([byt1, int(byt2[channel]), 0])
        r = spi.xfer2([ (24 + channel) << 2, 0, 0])
        adcout = (r[1] << 4) | (r[2] >> 4)
        #The MCP32xx responds with samples starting at the 5th bit in Byte2, so we & and shift
        #accordingly.
        #adcout = ((r[1]&5) << 8) + r[2]
        smooth.append(adcout)
        time.sleep(0.001)
    tadaa = sum(smooth) / len(smooth)
    #print smooth, tadaa

    return tadaa

def testSPI():
#Read MCP3208 (SPI, 12bit base resolution)
    #Read pressure signal.  Sensor is a Honeywell PX2 Sealed Gauge, 250PSIG operating pressure, 3.3v supply (Vss),
    #with a Full Signal Scale ("FSS") of 10% - 90% Vss (0.33v - 2.97v). 
    
    #Voltage equation is based on line slope intercep (y=mx+b). y=output, m = slope (scale), x=input (signal)
    #and b=offset. So, y=94.69(signal) + (-31.25)

    #Since this is a Sealed Gauge, with a reference of 1atmA (14.7psi), the PSIG equation includes
    #the barometric sensor value (BMP180 above) to offset the atmospheric pressure if used above sea-level.

    while True:
        try:
            opress_raw = readMCP(0)
            #if opress_raw < 409: opress_raw = 409
            opress_volt =  (opress_raw / 3685.5) * 2.97
            opress_PSIG = round((opress_volt * 94.7) - 31.25, 0)
            opress_needle = opress_PSIG / 250

            print ("%4d/3685.5 => %5.3f V => %d => %5.3f" % (opress_raw, opress_volt, opress_PSIG, opress_needle))

            time.sleep(0.05)

        except KeyboardInterrupt or SystemExit:
            break

##Main script init
if __name__ == "__main__":
    testSPI()
