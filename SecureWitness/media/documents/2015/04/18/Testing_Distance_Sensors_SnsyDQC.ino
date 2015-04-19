#include <SPI.h>
#include <SD.h>

int distancePin = A0;
int photoPin = A1;
int LEDPin = 2;

int index = 0;
const int holderSize = 10;
float holder[holderSize];
File myFile;
int photoConst;
bool personExit = true;
float oldDist = 0;
long time1,time2,time3 = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  Serial.print("Initializing SD card...");
  // On the Ethernet Shield, CS is pin 4. It's set as an output by default.
  // Note that even if it's not used as the CS pin, the hardware SS pin 
  // (10 on most Arduino boards, 53 on the Mega) must be left as an output 
  // or the SD library functions will not work. 
   pinMode(10, OUTPUT);
   
  if (!SD.begin(4)) {
    Serial.println("initialization failed!");
    return;
  }
  Serial.println("initialization done.");
  
  pinMode(LEDPin, OUTPUT);
  photoConst = analogRead(photoPin);
}

void loop() {
  long stuff = millis()-time3;
  Serial.print(stuff);
  Serial.print(" ");
  time3 = millis();
  // put your main code here, to run repeatedly:
  /*int lightSensorValue = analogRead(photoPin);
  Serial.print(personExit);
  Serial.print(" ");
  if((lightSensorValue > photoConst + 30) && personExit)
  {
    Serial.print("ON! ");
    digitalWrite(LEDPin,HIGH);
  }
  else
  {
    digitalWrite(LEDPin,LOW);
  }*/
  
  int heightsensorValue = analogRead(distancePin);
  /*float distance = 9462.0/(heightsensorValue - 16.92);/*heightsensorValue*5.0/1024.0//;
  if((distance < 0) || (distance >= 300))
    return;
  holder[index] = distance;
  index++;
  if(index >= holderSize)
  {
    index = 0;
  }   
  /*if(index == 0)
  {
    
    float average = 0;
    for (int i = 0; i < holderSize; i++)
    {
      average += holder[i];
    }
    average /= holderSize;//
    float average = distance;
    
    if(distance < 100 && oldDist >= 100)
    {
      time1 = millis();
      if(time1 > time2 + 2000)
      {
        time2 = millis();
        personExit = !personExit;
      }
    }
    oldDist = distance;*/
    
    int average = heightsensorValue;
    Serial.println(average);
    
    // open the file. note that only one file can be open at a time,
    // so you have to close this one before opening another.
    myFile = SD.open("3-1-15_1.csv", FILE_WRITE);
  
    // if the file opened okay, write to it:
    if (myFile) {
      Serial.print("Writing to test.txt...");
      myFile.println(average);
      // close the file:
      myFile.close();
      Serial.println("done.");
    } else {
      // if the file didn't open, print an error:
      Serial.println("error opening test.txt");
    }
  //}
}
