from flask import Flask, render_template, url_for, send_from_directory
import os

app = Flask(__name__)


@app.route("/")
def index():
	#attach profile name
	return render_template("base.html")

	
@app.route("/getSensorColumn")
def sensorColumn():
	#get data from json file and add it to the template
	#look at the sensors folder and add that as well
	return render_template("sensorColumn")

	
@app.route("/addSensor", methods=["POST"])
def addSensor():
	if request is None:
		return render_template("base.json")
	raise NotImplementedError


@app.route("/deleteSensor/<string:pinStr>")
def deleteSensor(pinNum):
	raise NotImplementedError

@app.route("/sendSwitchCommand/<string:pinStr>/<int:on>")
def swndSwitchCommand(pinStr, on):
	
	raise NotImplementedError
	
@app.route("/favicon.ico")
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

def utility_processor():
	def jsonSuccessEval(bool):
		if bool:
			return "true"
		elif not bool:
			return "false"
		else:
			return '"template error"'
		
	return dict(
		jsonSuccessEvaluation=jsonSuccessEval
	)




def start():
	app.run(debug=True)


if __name__ == '__main__':
	start()