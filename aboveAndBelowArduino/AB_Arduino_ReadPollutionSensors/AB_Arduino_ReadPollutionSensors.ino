/******************************************************************************
  Example combining Environmental breakout board and novaPM sensor SDS011
  
  Based on Example2_BME280Compensation from the CCS811 Library
  Compensating the CCS811 with humidity readings from the BME280
  https://github.com/sparkfun/SparkFun_CCS811_Arduino_Library

  Based on "novaPM" library we created based on Hackair Library 
  
******************************************************************************/
#include <Wire.h>
#include <SparkFunBME280.h> //Click here to get the library: http://librarymanager/All#SparkFun_BME280
#include <SparkFunCCS811.h> //Click here to get the library: http://librarymanager/All#SparkFun_CCS811
#include <novaPM.h> //Custom Library for the SDS011 novaPM sensor

#define CCS811_ADDR 0x5B //Default I2C Address
//#define CCS811_ADDR 0x5A //Alternate I2C Address

#define PIN_NOT_WAKE 5

//Global sensor objects
CCS811 myCCS811(CCS811_ADDR);
BME280 myBME280;
novaPM novaPMsensor;

struct pollutionData {
  float pm25;   /**< Amount of PM2.5 */
  float pm10;   /**< Amount of PM1.0 */
  float co2;
  float tvoc;
  float tempC;
  float tempF;
  float humidityRH;
  float pressurePa;
  float pressureInHg;
  float altitudeM;
  float altitudeF;
  int error;    /**< Error status */
};

struct pollutionData savedData;


void setup()
{
  Serial.begin(115200);
  //Serial.println();
  //Serial.println("Apply BME280 data to CCS811 for compensation.");

  // Initialize the BME280 & CCS811 sensors
  setupEnvComboSensors();

  // Initialize the novaPMsensor
  novaPMsensor.begin();
}

void loop()
{

  struct novaPMData data;
  novaPMsensor.readData(data);
  // If it was invalid, print error
  if (data.error != 0) {
    //Serial.println("Error!");
  } else {
    // Save the values to savedData
    savedData.pm25 = data.pm25;
    savedData.pm10 = data.pm10;
    // Print the values to serial
    /*Serial.print("PM2.5: ");
    Serial.println(data.pm25);
    Serial.print("PM10: ");
    Serial.println(data.pm10);
    Serial.print("Temp: ");
    Serial.println(data.tamper);
    Serial.println("---");*/
  }

  //Check to see if data is available
  if (myCCS811.dataAvailable())
  {
    //Calling this function updates the global tVOC and eCO2 variables
    myCCS811.readAlgorithmResults();

    float BMEtempC = myBME280.readTempC();
    float BMEhumid = myBME280.readFloatHumidity();

    /*Serial.print("Applying new values (deg C, %): ");
    Serial.print(BMEtempC);
    Serial.print(",");
    Serial.println(BMEhumid);
    Serial.println();*/

    //This sends the temperature data to the CCS811
    myCCS811.setEnvironmentalData(BMEhumid, BMEtempC);

    novaPMsensor.humidityCompensation(data, BMEhumid);

    //printInfoSerial fetches the values of tVOC and eCO2
    //printInfoSerial();

    //Fetch values and save them in savedData;
    saveEnvComboData();

  }
  else if (myCCS811.checkForStatusError())
  {
    //If the CCS811 found an internal error, print it.
    //printSensorError();
  }

  printInfoSerial();
  

  delay(2500); //Wait for next reading
}

//---------------------------------------------------------------
void saveEnvComboData(){
  savedData.co2 = myCCS811.getCO2();
  savedData.tvoc = myCCS811.getTVOC();
  savedData.tempC = myBME280.readTempC();
  savedData.tempF = myBME280.readTempF();
  savedData.humidityRH = myBME280.readFloatHumidity();
  savedData.pressurePa = myBME280.readFloatPressure();
  savedData.pressureInHg = (myBME280.readFloatPressure() * 0.0002953);
  savedData.altitudeM = myBME280.readFloatAltitudeMeters();
  savedData.altitudeF = myBME280.readFloatAltitudeFeet(); 
}



void printInfoSerial()
{
  Serial.println();
  Serial.print("&,pm25=");
  Serial.print(savedData.pm25,2);
  Serial.print(",pm10=");
  Serial.print(savedData.pm10,2);
  Serial.print(",co2=");
  Serial.print(savedData.co2); //ppm
  Serial.print(",tvoc=");
  Serial.print(savedData.tvoc); //ppb
  Serial.print(",tempC=");
  Serial.print(savedData.tempC,2); 
  Serial.print(",tempF=");
  Serial.print(savedData.tempF,2); 
  Serial.print(",humidityRH=");
  Serial.print(savedData.humidityRH,2); //%
  Serial.print(",pressurePa=");
  Serial.print(savedData.pressurePa,2); //Pa
  Serial.print(",pressureInHg=");
  Serial.print(savedData.pressureInHg,2); //InHg
  Serial.print(",altitudeM=");
  Serial.print(savedData.altitudeM,2); //m
  Serial.print(",altitudeF=");
  Serial.print(savedData.altitudeF,2); //ft
  Serial.print(",");
  Serial.println("#");
}

void setupEnvComboSensors(){
  Wire.begin();

  //This begins the CCS811 sensor and prints error status of .beginWithStatus()
  CCS811Core::CCS811_Status_e returnCode = myCCS811.beginWithStatus();
  //Serial.print("CCS811 begin exited with: ");
  //Serial.println(myCCS811.statusString(returnCode));

  //For I2C, enable the following and disable the SPI section
  myBME280.settings.commInterface = I2C_MODE;
  myBME280.settings.I2CAddress = 0x77;

  //Initialize BME280
  //For I2C, enable the following and disable the SPI section
  myBME280.settings.commInterface = I2C_MODE;
  myBME280.settings.I2CAddress = 0x77;
  myBME280.settings.runMode = 3; //Normal mode
  myBME280.settings.tStandby = 0;
  myBME280.settings.filter = 4;
  myBME280.settings.tempOverSample = 5;
  myBME280.settings.pressOverSample = 5;
  myBME280.settings.humidOverSample = 5;

  //Calling .begin() causes the settings to be loaded
  delay(10); //Make sure sensor had enough time to turn on. BME280 requires 2ms to start up.
  myBME280.begin();
}

//printSensorError gets, clears, then prints the errors
//saved within the error register.
void printSensorError()
{
  uint8_t error = myCCS811.getErrorRegister();

  if (error == 0xFF) //comm error
  {
    Serial.println("Failed to get ERROR_ID register.");
  }
  else
  {
    Serial.print("Error: ");
    if (error & 1 << 5)
      Serial.print("HeaterSupply");
    if (error & 1 << 4)
      Serial.print("HeaterFault");
    if (error & 1 << 3)
      Serial.print("MaxResistance");
    if (error & 1 << 2)
      Serial.print("MeasModeInvalid");
    if (error & 1 << 1)
      Serial.print("ReadRegInvalid");
    if (error & 1 << 0)
      Serial.print("MsgInvalid");
    Serial.println();
  }
}
