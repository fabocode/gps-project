#include "arduPi.h"
#include "SkyTraqNmeaParser.h"

// The SkyTraqNmeaParser object
SkyTraqNmeaParser parser;
// The SkyTraqNmeaParser result
const GnssData* gdata;
// Notification of SkyTraqNmeaParser
U32 gnssUpdateFlag = 0;

//Callback function for SkyTraqNmeaParser notification
bool GnssUpdated(U32 f, const char* buf, SkyTraqNmeaParser::ParsingType type);
// Display parsing result
bool Display(U32 f, const char* buf, SkyTraqNmeaParser::ParsingType type);
// Show satellites information(from GSV token, and need turn on _SUPPORT_GPS_SATELLITES_, 
// _SUPPORT_GLONASS_SATELLITES_ or _SUPPORT_BEIDOU_SATELLITES_)
void ShowSatellites(const SatelliteInfo* si);

void setup()
{
  //Set callback function for parsing result notification
  parser.SetNotify(GnssUpdated);
  
  //For UART interrupt
  pinMode(2, INPUT);
  digitalWrite(2, LOW);
  
  //NS-HP output NMEA message in 115200 bps
  Serial.begin(115200);
  //attachInterrupt(0, serialInterrupt, CHANGE);

  Serial.println("Init done!=================================");
}
/*
//Set the flag to true to prevent re-entry of interrupt.
volatile boolean inService = false;
void serialInterrupt()
{
 if (inService) 
 {
   return;
 }
 inService = true;

 interrupts();
 while(!Serial.available());
 parser.Encode(Serial.read());

 inService = false;
}
*/
void loop()
{
 if(Serial.available())
   parser.Encode(Serial.read());

 //inService = false;

}

void ShowSatellites(const SatelliteInfo* si)
{
  bool hasTitle = false;
  int max = GnssData::GetMaxSatelliteNum();
  for(int i = 0; i < max; ++i)
  {
    if(si[i].sv == 0)
      break;
    if(!hasTitle)
    {
      printf("PRN \tAZ  \tEL  \tCN0  \tUsed\r\n");
      hasTitle = true;
    }
    printf("%d\t%d\t%d\t%d\t%c\r\n", si[i].sv, si[i].azimuth, si[i].elevation, si[i].cno, (si[i].isInUse) ? 'Y' : 'N');
  }
}

bool GnssUpdated(U32 f, const char* buf, SkyTraqNmeaParser::ParsingType type)
{
  gnssUpdateFlag |= f;
  gdata = parser.GetGnssData();
  Display(f, buf, type);
  //return true to clear the flag in SkyTraqNmeaParseryTraq
  return true;
}

bool Display(U32 f, const char* buf, SkyTraqNmeaParser::ParsingType type)
{
  U32 i = 0;
  const GnssData& gnss = *gdata;

  for(; i < 32; ++i)
  {
    U32 mask = (1 << i);
    switch((mask & f))
    {
    case SkyTraqNmeaParser::NoUpdate:
      //Do nothing
      break;
    case SkyTraqNmeaParser::UpdateDate:
      printf("Date:%04d/%02d/%02d\r\n", gnss.GetYear(), gnss.GetMonth(), gnss.GetDay());
      break;
    case SkyTraqNmeaParser::UpdateTime:
      printf("Time:%02d:%02d:%2.3f\r\n", gnss.GetHour(), gnss.GetMinute(), gnss.GetSecond());
      break;
    case SkyTraqNmeaParser::UpdateLatitude:
      printf("Latitude:%3.7f\r\n", gnss.GetLatitude());
      break;
    case SkyTraqNmeaParser::UpdateLongitude:
      printf("Longitude:%3.7f\r\n", gnss.GetLongitude());
      break;
    case SkyTraqNmeaParser::UpdateAltitude:
      printf("Altitude:%5.1f\r\n", gnss.GetAltitudeInMeter());
      break;
    case SkyTraqNmeaParser::UpdateCourse:
      printf("Course:%3.1f\r\n", gnss.GetCourseInDegree());
      break;
    case SkyTraqNmeaParser::UpdateSpeed:
      printf("Speed:%5.2f km/hr\r\n", gnss.GetSpeedInKmHr());
      break;
    case SkyTraqNmeaParser::UpdateQualitMode:
      printf("Qualit Mode:%d\r\n", gnss.GetQualitMode());
      break;
    case SkyTraqNmeaParser::UpdateNumberOfSv:
      printf("Number Of Sv:%d\r\n", gnss.GetNumberOfSv());
      break;
    case SkyTraqNmeaParser::UpdateHdop:
      printf("HDOP:%3.1f\r\n", gnss.GetHdop());
      break;
    case SkyTraqNmeaParser::UpdatePdop:
      printf("PDOP:%3.1f\r\n", gnss.GetPdop());
      break;
    case SkyTraqNmeaParser::UpdateVdop:
      printf("VDOP:%3.1f\r\n", gnss.GetVdop());
      break;
    case SkyTraqNmeaParser::UpdateNavigationMode:
      printf("Navigation Mode:%d\r\n", gnss.GetNavigationMode());
      break;
    case SkyTraqNmeaParser::UpdateSatelliteInfo:
#if (_SUPPORT_GPS_SATELLITES_)
      ShowSatellites(gnss.GetGpsSatellites());
#endif
#if (_SUPPORT_GLONASS_SATELLITES_)
    (  ShowSatellites(gnss.GetGlonassSatellites());
#endif
#if (_SUPPORT_BEIDOU_SATELLITES_)
      ShowSatellites(gnss.GetBeidouSatellites());
#endif
      break;
    case SkyTraqNmeaParser::UpdateEnuVelocity:
      printf("E-Velocity:%5.2f   N-Velocity:%5.2f   U-Velocity:%5.2f\r\n", gnss.GetEVelocity(), gnss.GetNVelocity(), gnss.GetUVelocity());
      break;
    case SkyTraqNmeaParser::UpdateRtkAge:
      printf("RTK Age:%f\r\n", gnss.GetRtkAge());
      break;
    case SkyTraqNmeaParser::UpdateRtkRatio:
      printf("RTK Ratio:%f\r\n", gnss.GetRtkRatio());
      break;
    case SkyTraqNmeaParser::UpdateEnuProjection:
      printf("E-Projection:%5.2f   N-Projection:%5.2f   U-Projection:%5.2f\r\n", gnss.GetEProjection(), gnss.GetNProjection(), gnss.GetUProjection());
      break;
    case SkyTraqNmeaParser::UpdateBaselineLength:
      printf("RTK Baseline Length:%5.1f\r\n", gnss.GetBaselineLength());
      break;
    case SkyTraqNmeaParser::UpdateBaselineCourse:
      printf("RTK Baseline Course:%3.1f\r\n", gnss.GetBaselineCourse());
      break;
    default:
      break;
    }
  }
  return true;
}

int main() {
  setup();
  while(1) {
    loop();
  }
}


