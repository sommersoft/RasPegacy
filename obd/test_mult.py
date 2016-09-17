import obd, time

obd.logger.setLevel(obd.logging.DEBUG) # enables all debug information

connection = obd.OBD('/dev/ttyUSB0', 115200) # auto-connects to USB or RF port

cmd = [obd.commands.SPEED, obd.commands.RPM, obd.commands.INTAKE_PRESSURE] # select an OBD command (sensor)

#response = connection.query_multi(False, obd.commands.SPEED, obd.commands.RPM) # send the command, and parse the response
#response = connection.query_multi(cmd) # send the command, and parse the response
while True:  
  try:
    rpm, speed, intake = connection.query_multi(*cmd)
    
    print(rpm.value)
    print(speed.value.to('mph'))
    print(intake.value.to('psi'))
    time.sleep(0.5)
    
  except KeyboardInterrupt:
    break
