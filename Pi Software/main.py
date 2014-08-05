import serial
from time import sleep
from os.path import isfile
import json
from threading import Thread
import smtplib
from email.mime.text import MIMEText


def arduinoCommunication():
	import serial
	try:
		arduino = serial.Serial(2, 19200, timeout=1)
		while True:
			arduinoText = arduino.readline().strip()
			if not arduinoText:
				sleep(1)
				continue
			try:
				json.loads(arduinoText)
				#alerting subprocess
				#if isfile("alerts.txt"):
				#	for contant in explode(file.read())
				#		send email
				with open("sensorData.json", "w+") as file:#w+
					print "Writing: %s" % blah
					file.write(arduinoText)	
			except Exception:
				print "Bad JSON"
			if isfile("switchAction.txt"):
				with open("switchAction.txt", "r") as file:
					arduino.write(file.read().trim())
	except Exception:
		arduino.close()
		print "Exiting ArduinoCommunicationThread...\n***\t\t***\n%s" % Exception
	return

def serverStart():
	import piServer
	try:
		piServer.start()
	except Exception:
		print "Exiting ServerThread...\n***\t\t***\n%s" % Exception

if __name__ == '__main__':
	ArduinoCommunicationThread = Thread(target=arduinoCommunication)
	ServerThread = Thread(target=serverStart)
	try:
		ArduinoCommunicationThread.start()
		ServerThread.start()
	except Exception:
		print "Exiting the program"
		ArduinoCommunicationThread.stop()
		ServerThread.stop()
	ArduinoCommunicationThread.join()
	ServerThread.join()		