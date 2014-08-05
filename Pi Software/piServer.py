from flask import Flask, render_template, url_for, send_from_directory, request, redirect
from os.path import isfile
from time import sleep
import os
import json
app = Flask(__name__)


@app.route("/")
def index():
	return render_template("base.html")

	
@app.route("/getSensorColumn")
def sensorColumn():
	#get data from json file and add it to the template
	#look at the sensors folder and add that as well
	switch = []
	temp = []
	trip = []
	for fileName in os.listdir("./sensors"):
		tmp = {"pinStr":fileName[:3], "type":fileName[3:]}
		with open("./sensors/"+fileName) as file:
				tmp["label"] = file.read().strip()
		if fileName[3:] == "temp":
			temp.append(tmp)
		elif fileName[3:] == "switch":
			switch.append(tmp)
		elif fileName[3:] == "trip":
			trip.append(tmp)
	with open("sensorData.json", "r") as file:
		sensorData = json.loads(file.read().strip())
	alertAddress = ""
	if isfile("alerts.txt"):
		with open("alerts.txt", "r") as file:
			alertAddress = file.read().strip()

	return render_template("SensorsColumn.html",
		switch=switch, temp=temp, trip=trip,
		slen=len(switch), tlen=len(temp), rlen=len(trip), sensorData=sensorData, alertAddress=alertAddress)

	
@app.route("/addSensor", methods=["POST"])
def addSensor():
	if request is None:
		return render_template("base.json", status=False)
	with open("./sensors/"+request.form['pinStr'].upper()+request.form['type'], "w+") as file:
		file.write(request.form['sensorLabel'])
	return redirect("/")


@app.route("/deleteSensor/<string:pinStr>")
def deleteSensor(pinNum):
	for file in os.listdir("./sensors"):
		if file.startswith(pinStr):
			remove("./sensors/"+file)
			return render_template("base.json", status=True)
	return render_template("base.json", status=False)

@app.route("/sendSwitchCommand/<string:pinStr>/<int:on>")
def swndSwitchCommand(pinStr, on):
	if isfile("switchAction.txt"):
		sleep(2)
	if pinStr == "D02" or pinStr == "D06":
		command = 1
	elif pinStr == "D03" or pinStr == "D07":
		command = 2
	elif pinStr == "D04" or pinStr == "D08":
		command = 3
	else:
		command = 0
	print str(command)
	if not command:
		return render_template("base.json", status=False)
	
	command = command + (5*on)
	with open("switchAction.txt", "w+") as file:
		file.write(str(command))
	
	return render_template("base.json", status=True)
	
@app.route("/alertAddress", methods=["POST"])
def alertAddress():
	if request is None:
		return render_template("base.json", status=False)
	with open("alerts.txt", "w+") as file:
		file.write(request.form['alertAddress'].strip())
	return redirect("/")
			
@app.route("/favicon.ico")
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.context_processor
def utility_processor():
	def jsonSuccessEval(bool):
		if bool:
			return "true"
		elif not bool:
			return "false"
		else:
			return '"template error"'
	def resolveWasTripped(bool):
		if bool:
			return "True"
		else:
			return "False"
	
	
	return dict(
		jsonSuccessEvaluation=jsonSuccessEval,
		resolveWasTripped=resolveWasTripped
	)




def start():
	app.run("0.0.0.0")


if __name__ == '__main__':
	start()
