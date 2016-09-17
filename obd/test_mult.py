import obd

obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information

connection = obd.OBD('/dev/ttyUSB0', 115200) # auto-connects to USB or RF port

#cmd = [obd.commands.SPEED, obd.commands.RPM, obd.commands.INTAKE_PRESSURE] # select an OBD command (sensor)

#response = connection.query_multi(False, obd.commands.SPEED, obd.commands.RPM) # send the command, and parse the response
#response = connection.query_multi(cmd) # send the command, and parse the response
rpm, speed, intake = connection.query_multi(obd.commands.RPM, obd.commands.SPEED, obd.commands.INTAKE_PRESSURE)

print(rpm.value)
print(speed.value)
print(intake.value)
#print(response.value) # returns unit-bearing values thanks to Pint
#print(response.value.to("volt")) # user-friendly unit conversions
