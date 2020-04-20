

#include <Arduino_LSM9DS1.h> //Include the library for 9-axis IMU
#include <Arduino_LPS22HB.h> //Include library to read Pressure 
#include <Arduino_HTS221.h> //Include library to read Temperature and Humidity 
#include <Arduino_APDS9960.h> //Include library for colour, proximity and gesture recognition

const int ledPin1 = 22;
const int ledPin2 = 23;
const int ledPin3 = 24;


void setup(){

  //pinMode(22, OUTPUT);
  //pinMode(23, OUTPUT);
  //pinMode(24, OUTPUT);
  
  Serial.begin(9600); //Serial monitor to display all sensor values 

  if (!IMU.begin()) //Initialize IMU sensor 
  { Serial.println("Failed to initialize IMU!"); while (1);}

  if (!BARO.begin()) //Initialize Pressure sensor 
  { Serial.println("Failed to initialize Pressure Sensor!"); while (1);}

  if (!HTS.begin()) //Initialize Temperature and Humidity sensor 
  { Serial.println("Failed to initialize Temperature and Humidity Sensor!"); while (1);}

  if (!APDS.begin()) //Initialize Colour, Proximity and Gesture sensor 
  { Serial.println("Failed to initialize Colour, Proximity and Gesture Sensor!"); while (1);}
 }

float accel_x, accel_y, accel_z;
float gyro_x, gyro_y, gyro_z;
float mag_x, mag_y, mag_z;
float pressure;
float temperature, humidity;
int proximity;
int Delay = 100;

void  Magnetometer(int Delay)
{
  //Magnetometer values 
  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(mag_x, mag_y, mag_z);
    Serial.print("Magnetometer = ");Serial.print(mag_x); Serial.print(", ");Serial.print(mag_y);Serial.print(", ");Serial.println(mag_z);
  }
  delay (Delay);
}

void Accelerometer(int Delay)
{
  //Accelerometer values 
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(accel_x, accel_y, accel_z);
    Serial.print("Accelerometer = ");Serial.print(accel_x); Serial.print(", ");Serial.print(accel_y);Serial.print(", ");Serial.println(accel_z);
  }
delay (Delay); 
}

void Gyroscope(int Delay)
{
  //Gyroscope values 
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gyro_x, gyro_y, gyro_z);
    Serial.print("Gyroscope = ");Serial.print(gyro_x); Serial.print(", ");Serial.print(gyro_y);Serial.print(", ");Serial.println(gyro_z);
  }
delay (Delay);
}

void Pressure(int Delay)
{
 //Read Pressure value
  pressure = BARO.readPressure();
  Serial.print("Pressure = ");Serial.println(pressure);
  delay (Delay);  
}

void Temperature(int Delay)
{
  //Read Temperature value
  temperature = HTS.readTemperature();
  Serial.print("Temperature = ");Serial.println(temperature);
  delay (Delay);  
}

void Humidity(int Delay)
{
  //Read Humidity value
  humidity = HTS.readHumidity();
  Serial.print("Humidity = ");Serial.println(humidity);
  delay (Delay);  
}

void Proximity(int Delay)
{
  //Proximity value
  if (APDS.proximityAvailable()) {
    proximity = APDS.readProximity();
    Serial.print("Proximity = ");Serial.println(proximity); 
    }
  delay (Delay);  
}

void Gesture(int Delay)
{
  if (APDS.gestureAvailable()) {
    // a gesture was detected, read and print to serial monitor
    int gesture = APDS.readGesture();

    switch (gesture) {
      case GESTURE_UP:
        Serial.println("Detected UP gesture");
        digitalWrite(ledPin1, HIGH);
        digitalWrite(ledPin2, LOW);
        digitalWrite(ledPin3, LOW);
        //digitalWrite(ledPin1, LOW);
        delay(Delay);
        //digitalWrite(ledPin1, HIGH);
        break;

      case GESTURE_DOWN:
        Serial.println("Detected DOWN gesture");
        digitalWrite(ledPin1, LOW);
        digitalWrite(ledPin2, HIGH);
        digitalWrite(ledPin3, LOW);
        //digitalWrite(ledPin2, LOW);
         delay(Delay);
        //digitalWrite(ledPin2, HIGH);
        break;

      case GESTURE_LEFT:
        Serial.println("Detected LEFT gesture");
        digitalWrite(ledPin1, LOW);
        digitalWrite(ledPin2, LOW);
        digitalWrite(ledPin3, HIGH);
        //digitalWrite(ledPin3, LOW);
         delay(Delay);
        //digitalWrite(ledPin3, HIGH);
        break;

      case GESTURE_RIGHT:
        Serial.println("Detected RIGHT gesture");
        digitalWrite(ledPin1, HIGH);
        digitalWrite(ledPin2, HIGH);
        digitalWrite(ledPin3, LOW);
        //digitalWrite(LED_BUILTIN, HIGH);
        delay(Delay);
        //digitalWrite(LED_BUILTIN, LOW);
        break;

      default:
        // ignore
        break;
    }
  }
  else
  {
    //Serial.println("No Gester");
  }  
}

void loop()
{

  //Magnetometer(Delay);
  //Accelerometer(Delay);
  //Gyroscope(Delay);
  //Pressure(Delay);
  //Temperature(Delay);
  //Humidity(Delay);
  Proximity(Delay);
  
  //Gesture(Delay);
  //delay(20);
  
  //Serial.println("_____________________________________________________"); 
  //delay(Delay);
}
