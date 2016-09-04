# RasPegacy
Another Boring, RPi Car Data Display... Designed for use with 05-09 Subaru Legacies with OEM Navigation

# Hardware System Components (as designed)
1. Raspberry Pi A+
2. SeeedStudio RTC Module (DS3231)
3. Sparkfun Barometric Pressure Breakout (BMP180)
4. Microchip ADC (MCP3208)
5. Honeywell PX2 Series Pressure Transducer (PX2AN1XX100PSACX)
6. Adafruit 3-Axis Accelerometer Breakout (LIS3DH)
7. ScanTool OBDLink SX (USB type OBD-II reader)

# Software System Components (as designed)
1. Raspbian OS
2. info-beamer Digital Signage (https://info-beamer.com/)
3. Python (Overhead Handler)
4. LUA (info-beamer "node" scripting)
5. Ploticus (used to create .png graphing files [is unusably slow ATM]) (http://ploticus.sourceforge.net/doc/welcome.html)

# External Python Modules Used
1. Adafruit BMP085: https://github.com/adafruit/Adafruit_Python_BMP
2. Brendan-w's fork of pyOBD: https://github.com/brendan-w/python-OBD
3. Matt Dyson's LIS3DH (see Issue #4): https://github.com/mattdy/python-lis3dh
