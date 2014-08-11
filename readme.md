<h1>
Independent Study - Home Automation
</h1>

<h3>
Reference Material
</h3>
The following are reference materials
Thermistor stuff
- Diagram and table lookup method [here](http://playground.arduino.cc/ComponentLib/Thermistor)
- Equation I used to transform voltage to temp in K [here](http://en.wikipedia.org/wiki/Thermistor#Steinhart.E2.80.93Hart_equation)

Remote Power Socket Reverse Engineering
- A guide done by someone with the same chipset I had [here](http://oddwires.co.uk/alarm/hardware/)
- RS2260-R4 pinout and datasheet [here](http://www.dz863.com/datasheet-8368852863-HS2260-R4_Cmos/)

Full Hardware Listing
- [Arduino Starter Kit w/ Breadboard](http://www.amazon.com/gp/product/B0051QHPJM/ref=oh_aui_detailpage_o06_s00?ie=UTF8&psc=1)
- [Raspberry Pi](http://www.amazon.com/RASPBERRY-MODEL-756-8308-Raspberry-Pi/dp/B009SQQF9C/ref=sr_1_1?ie=UTF8&qid=1407779351&sr=8-1&keywords=raspberry+pi+model+b)
- [Remote Controlled Power Socket](http://www.amazon.com/gp/product/B0087DAW46/ref=oh_aui_detailpage_o06_s00?ie=UTF8&psc=1)
- [Thermistors](http://www.amazon.com/gp/product/B0087YI1KW/ref=oh_aui_detailpage_o01_s01?ie=UTF8&psc=1)
- [Resistors](http://www.amazon.com/gp/product/B00B5RJF1M/ref=oh_aui_detailpage_o03_s00?ie=UTF8&psc=1)
- [Human Sensor](http://www.amazon.com/gp/product/B007XQRKD4/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1)
- Plus other random peripherals necessary to make those components work


Software Technologies Documentation
- [Flask](http://flask.pocoo.org/docs/flask-docs.pdf)
- [pySerial](http://pyserial.sourceforge.net/pyserial_api.html)
- [Jinja2](http://jinja.pocoo.org/docs/api/)
<h3>
The Arduino Stuff
</h3>

The arduino is very quick to [setup](http://arduino.cc/en/Guide/HomePage) using the Arduino IDE.
The sketch, the name for an arduino program, has 2 basic parts.
They are
- The setup function
- The loop function

These can be thought of as the initialization section, setup function, used for setting up pins and other overhead only needed once. The second part is the main program loop which will be iterated over repeated. This is where any operations which need to happen at every iteration need go.

My project also has a header section where everything is defined using #define to make things easy to change. In addition, there are helper functions to do things like take a thermister reading sample (because not every reading fromt he hardware is accurate) or send generic switch commands.

Future development would yield some sort of discovery on startup to understand its sensors and communicate that to the software side. Although that was out of scope for a semester project.

<h3>
The Software Side
</h3>
By using a simple flask application and deploying it with their development server (which works fine for low connection numbers and such) works like a charm, simply navigate to the Pu Software folder and type sudo python main.py. For true useage I would deploy it with a real web server like Twisted, Tornado, or Apache. All are relatively simple to use - if you understand twisted's deffered object model. I had to hard code in the comport being used so, make sure to use the top USB slot on the pi. The front end allows you to add sensors to your profile dynamically through a form, as well as add an alerting address. All these things are stored in a sensors folder or in text files in the Pi Software folder. This is because the software is based around 2 Threads, the web server and the Thread polling for valid serial communication from the arduino. This arduino communication thread writes the json data from the arduino (after checking validity) to a sensorData.json file. The file is then used for the information on the front end and to tie sensors to its data (via what is called pinString which is a letter to denote pin type and 2 digit number for the pin number ex. D01 A02).


<h3>
Most of the Dependencies
</h3>

Most of the dependencies can be taken care of by doing

<code>
sudo apt get update && sudo apt-get upgrade
</code>

and

<code>
sudo apt get install python-flask && sudo apt-get install python-serial
</code>

If there are issues with dependencies contact me.