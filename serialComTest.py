import serial
from time import sleep
import msvcrt
from os.path import isfile
import json
arduino = serial.Serial(2, 19200, timeout=1)
sleep(2)
print "open serial..."

# while 1:
# command = 0b00000001
# arduino.write(str(command) +"\n")
# sleep(5)

# while 1:
	# print arduino.read()
try:
	while True:
		blah = arduino.readline().strip()
		if blah == "":
			sleep(1)
			continue
		try:
			json.loads(blah)
			#alerting subprocess
			with open("sensorData.json", "a") as file:#w+
				print "Writing: %s" % blah
				file.write(blah)	
		except Exception:
			r= ""
		if isfile("switchAction.txt"):
			with open("switchAction.txt", "r") as file:
				arduino.write(file.read().trim())
except KeyboardInterrupt:
	print "exit"