import serial
from time import sleep
from os.path import isfile
import json
from threading import Thread
from os import remove
import smtplib
from email.mime.text import MIMEText
import sys

def sendEmailAlert(emailAddress):
	sender = "rm0100101@gmail.com"
	msg = MIMEText("A trip sensor was set off!")
	msg['Subject'] = 'Alert!'
	msg['To'] = emailAddress
	msg['From'] = sender
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(sender, "0104721376")
	server.sendmail(sender, [emailAddress], msg.as_string())
	server.quit()


def arduinoCommunication():
	import serial
	try:
		arduino = serial.Serial("/dev/ttyACM0", 19200, timeout=1)
		while True:
			if isfile("switchAction.txt"):
				with open("switchAction.txt", "r") as file:
					arduino.write(file.read().strip())
				remove("switchAction.txt")
			
			arduinoText = arduino.readline().strip()
			if arduinoText:
				try:
					arduinoData = json.loads(arduinoText)
					#alerting subprocess
					if isfile("alerts.txt") and arduinoData['D13']:
						with open("alerts.txt", "r") as file:
							sendEmailAlert(file.read().strip())
					with open("sensorData.json", "w+") as file:#w+
						print "Writing: %s" % arduinoText
						file.write(arduinoText)
				except Exception as e:
					print "Bad JSON: %s" % e
			else:
				sleep(1)
				continue
	except Exception as e:
		arduino.close()
		print "Exiting ArduinoCommunicationThread...\n***\t\t***\n%s" % e
	return

def serverStart():
	import piServer
	try:
		piServer.start()
	except Exception as e:
		print "Exiting ServerThread...\n***\t\t***\n%s" % e

if __name__ == '__main__':
	ArduinoCommunicationThread = Thread(target=arduinoCommunication)
	ServerThread = Thread(target=serverStart)
	try:
		ArduinoCommunicationThread.start()
		ServerThread.start()
	except KeyboardInterrupt:
		print "Exiting the program"
		ArduinoCommunicationThread.stop()
		ServerThread.stop()
	ArduinoCommunicationThread.join()
	ServerThread.join()
