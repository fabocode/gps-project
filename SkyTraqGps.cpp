#include "arduPi.h"
#include "SkyTraqNmeaParser.h"

// The SkyTraqNmeaParser object
SkyTraqNmeaParser parser;

// The SkyTraqNmeaParser result
const GnssData* gdata;

// Notification flag of SkyTraqNmeaParser
U32 gnssUpdateFlag = 0;

// New variables to test
U16 _year; // actual date
U16 _month; // actual date
U16 _day; // actual date
U16 _hours; // real time
U16 _minutes; // real time
D64 _seconds; // real time
D64 _latitude; // coordinates
D64 _longitude; // coordinates
D64 _speed_in_mph; // speed in the ground (Knots to MPH converted)

struct gpsdata {
    // rmc as prefix reference
    U16 year; // actual date
    U16 month; // actual date
    U16 day; // actual date
    U16 hours; // real time
    U16 minutes; // real time
    D64 seconds; // real time
    D64 latitude; // coordinates
    D64 longitude; // coordinates
    D64 speed_in_mph; // speed in the ground (Knots to MPH converted)
}RMC;

//Callback function for SkyTraqNmeaParser notification
bool GnssUpdated(U32 f, const char* buf, SkyTraqNmeaParser::ParsingType type);

void setup() {
  //Set callback function for parsing result notification
  parser.SetNotify(GnssUpdated);
  
  //NMEA message baudrate to initiate: 115200 bps
  Serial.begin(115200);

  Serial.println("GPS Ready.........................");
}

// Arduino like void loop routine
void loop() {
 // Starts reading UART Serial data, and send it to the GPS library parser to update variables in the process 
 if(Serial.available())
 {
   parser.Encode(Serial.read());
   printf("Date:%04d/%02d/%02d\r\n", _year, _month, _day);
   printf("Time:%02d:%02d:%2.3f\r\n", RMC.hours, RMC.minutes, RMC.seconds);
   printf("Latitude:%3.7f\r\n", RMC.latitude);
   printf("Longitude:%3.7f\r\n", RMC.longitude);
   printf("Speed:%5.2f Mph\r\n", RMC.speed_in_mph);
   delay(10);
 }
}

//Once the code gets here (calledback from GPS library parser), it will update global variables mainly
bool GnssUpdated(U32 f, const char* buf, SkyTraqNmeaParser::ParsingType type) {
  gdata = parser.GetGnssData();
  const GnssData& gnss = *gdata;
  //struct gpsdata RMC;
  // Get parameters and save it into structure variables                    
  _year = gnss.GetYear();
  _month = gnss.GetMonth();
  _day = gnss.GetDay();
  //printf("Date:%04d/%02d/%02d\r\n", RMC.year, RMC.month, RMC.day);
  
  RMC.hours = gnss.GetHour();
  RMC.minutes = gnss.GetMinute();
  RMC.seconds = gnss.GetSecond();
  //printf("Time:%02d:%02d:%2.3f\r\n", RMC.hours, RMC.minutes, RMC.seconds);
  
  RMC.latitude = gnss.GetLatitude();
  //printf("Latitude:%3.7f\r\n", RMC.latitude);
  
  RMC.longitude = gnss.GetLongitude();  
  //printf("Longitude:%3.7f\r\n", RMC.longitude);
  
  RMC.speed_in_mph = gnss.GetSpeedInMph();
  //printf("Speed:%5.2f Mph\r\n", RMC.speed_in_mph);
  
  //return true to clear the flag in the GPS library parser
  return true;
}

// Main routine
int main() {
  setup();
  while(1) {
    loop();
  }
}

extern "C"
{
	void setup_exp() {
		setup();
	}
	
	void loop_exp() {
		loop();
	}
	
	U16 year_exp() {
		gdata = parser.GetGnssData();
  		const GnssData& gnss = *gdata;
		return gnss.GetYear();
	}
	
	U16 month_exp() {
		gdata = parser.GetGnssData();
  		const GnssData& gnss = *gdata;
		return gnss.GetMonth();
	}
	
	U16 day_exp() {
		gdata = parser.GetGnssData();
  		const GnssData& gnss = *gdata;
		return gnss.GetDay();
	}
	
	U16 hours_exp() {
		gdata = parser.GetGnssData();
  		const GnssData& gnss = *gdata;
		return gnss.GetHour();
	}
	
	U16 minutes_exp() {
		gdata = parser.GetGnssData();
  		const GnssData& gnss = *gdata;
		return gnss.GetMinute();
	}
	
	D64 seconds_exp() {
		gdata = parser.GetGnssData();
  		const GnssData& gnss = *gdata;
		return gnss.GetSecond();
	}
	
	D64 latitude_exp() {
		gdata = parser.GetGnssData();
  		const GnssData& gnss = *gdata;
		return gnss.GetLatitude();
	}
	
	D64 longitude_exp() {
		gdata = parser.GetGnssData();
  		const GnssData& gnss = *gdata;
		return gnss.GetLongitude();
	}
	D64 speed_in_mph_exp() {
		gdata = parser.GetGnssData();
  		const GnssData& gnss = *gdata;
		return gnss.GetSpeedInMph();
	}
}