import serial
import time
import msvcrt

arduino = serial.Serial(2, 19200, timeout=1)
time.sleep(2)
print "open serial..."

#while 1:
command = 0b00000001
arduino.write(str(command) +"\n")
time.sleep(5)

while 1:
	print arduino.read()