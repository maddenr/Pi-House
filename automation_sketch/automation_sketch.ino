// Define Analog Pins here
#define Indoor_Thermister 0
#define Outdoor_Thermister 1

//Define Digital Pins here
#define Socket1_ON 2
#define Socket2_ON 3
#define Socket3_ON 4
#define Socket1_OFF 6
#define Socket2_OFF 7
#define Socket3_OFF 8
#define Human_Sensor1 13

//Define Flags here
#define Socket1_flag 49    //0010
#define Socket2_flag 50    //0100
#define Socket3_flag 51    //1000
#define ON 5  //0001
#define OFF 0 //0000
#define NO_COMMAND -1

#define INVALID_TEMP_SAMPLE 99999
//Prototyping
void sampleThermisterReading(int* thermisterSamplePtr, int RawADC);
double ThermisterReading(int RawADC);
void sendSwitchCommand(int pin, boolean turnOn);

//define global vars
unsigned long time;
double indoorThermisterSample = INVALID_TEMP_SAMPLE;
boolean humanDetected = false;

void setup(){
  pinMode(Socket1_ON, OUTPUT);
  pinMode(Socket2_ON, OUTPUT);
  pinMode(Socket3_ON, OUTPUT);
  pinMode(Socket1_OFF, OUTPUT);
  pinMode(Socket2_OFF, OUTPUT);
  pinMode(Socket3_OFF, OUTPUT);
  pinMode(Human_Sensor1, INPUT);
  Serial.begin(19200);
  Serial.println("::");
  time=millis();
}

void loop(){
  String responseTemplate = "{  }";
  if(Serial.available()>0){
    byte command = Serial.read();
    Serial.println(command, DEC);
    switch(command){
      case Socket1_flag + OFF:
         Serial.println("Switch1_off");
         sendSwitchCommand(Socket1_OFF, true);
         return;
       case Socket1_flag + ON:
         Serial.println("Switch1_on");
         sendSwitchCommand(Socket1_ON, true);
         return;
       case Socket2_flag + OFF:
         Serial.println("Switch2_off");
         sendSwitchCommand(Socket2_OFF, true);
         return;
       case Socket2_flag + ON:
         Serial.println("Switch2_on");
         sendSwitchCommand(Socket2_ON, true);
         return;
       case Socket3_flag + OFF:
         Serial.println("Switch3_off");
         sendSwitchCommand(Socket3_OFF, true);
         return;
       case Socket3_flag + ON:
         Serial.println("Switch3_on");
         sendSwitchCommand(Socket3_ON, true);
         return;
       case 13: //newline key
         return;
       default:
       Serial.println("yellow?");
       return;
    }
  }
  //thermister sampling
  sampleThermisterReading(&indoorThermisterSample, analogRead(Indoor_Thermister));
  if(digitalRead(Human_Sensor1) == 1){
    humanDetected = true;
  }
  
  if (millis() - time >10000){
    time=millis();
    Serial.print("{");
    Serial.print("\"A00\":");
    Serial.print(indoorThermisterSample, DEC);
    Serial.print(",");
    Serial.print("\"D13\":");
    Serial.print(humanDetected ? "true" : "false");
//    Serial.println(",");
    Serial.println("}");
    if(humanDetected){ //assume it was reported
     humanDetected = false; 
    }
  }
}


void sampleThermisterReading(double *thermisterSamplePtr, int RawADC){
  double Temp = ThermisterReading(RawADC);
  if(*thermisterSamplePtr == INVALID_TEMP_SAMPLE){
    *thermisterSamplePtr = Temp;
  }
  else if(*thermisterSamplePtr/Temp > 0.75 && Temp / *thermisterSamplePtr > 0.75){ //check if samples are close
    *thermisterSamplePtr = Temp;
  }
  else {
   *thermisterSamplePtr = INVALID_TEMP_SAMPLE; 
  }
}

double ThermisterReading(int RawADC) {
  double Temp;
  // See http://en.wikipedia.org/wiki/Thermistor for explanation of formula
  Temp = log(((10240000/RawADC) - 10000));
  Temp = 1 / (0.001129148 + (0.000234125 * Temp) + (0.0000000876741 * Temp * Temp * Temp));
  Temp = Temp - 273.15;           // Convert Kelvin to Celcius
  return Temp;
}

void sendSwitchCommand(int pin, boolean turnOn){
  digitalWrite(pin, turnOn? HIGH : LOW);
  delay(500);
  digitalWrite(pin, !turnOn? HIGH : LOW);
}

