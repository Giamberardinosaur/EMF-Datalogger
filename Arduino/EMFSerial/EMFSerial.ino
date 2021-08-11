x#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

#define EMF_PIN A0

long lastTime = 0;

SoftwareSerial mySerial(8, 7);
Adafruit_GPS gps(&mySerial);

void setup() {
  Serial.begin(115200);
  analogReference(INTERNAL);
  pinMode(EMF_PIN, INPUT);

  gps.begin(9600);
  gps.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  gps.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
  gps.sendCommand(PGCMD_ANTENNA);

  delay(100);
}

void loop() {
  char c = gps.read();
  if (gps.newNMEAreceived()) {
    gps.parse(gps.lastNMEA());
  }
  float lat = gps.latitudeDegrees;
  float lon = gps.longitudeDegrees;
    
  if (millis()-lastTime > 700) {
    lastTime = millis();
    float power = analogRead(EMF_PIN);
    power = min(power, 2000);
 
    char output[32] = {};
    if (gps.fix) {
      
      //"-Wl,-u,vfprintf -lprintf_flt -lm" compiler options REQUIRED for the following line to work
      // if you get ? instead of numbers this is why
      sprintf(output, "#%4i,%+8.6f,%+8.6f\n", int(power), lat, lon);
      
    } else {
      sprintf(output, "#%4i,       nan,       nan\n", int(power));
    }

    Serial.print(output);
  }
}
