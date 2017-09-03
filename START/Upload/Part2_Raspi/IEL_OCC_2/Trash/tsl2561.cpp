#include <stdio.h>
#include <inttypes.h>
#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <errno.h>

// ALL COMMAND TSL2561
// Default I2C RPI address in (0x39) = FLOAT ADDR (Slave) Other [(0x49) = VCC ADDR / (0x29) = GROUND ADDR]
#define TSL2561_ADDR_LOW                   (0x29)
#define TSL2561_ADDR_FLOAT                 (0x4d)
#define TSL2561_ADDR_HIGH                   (0x49)
#define TSL2561_CONTROL_POWERON             (0x03)
#define TSL2561_CONTROL_POWEROFF          (0x00)
#define TSL2561_GAIN_0X                        (0x00)   //No gain
#define TSL2561_GAIN_AUTO                (0x01)
#define TSL2561_GAIN_1X                 (0x02)
#define TSL2561_GAIN_16X                  (0x12) // (0x10)
#define TSL2561_INTEGRATIONTIME_13MS          (0x00)   // 13.7ms
#define TSL2561_INTEGRATIONTIME_101MS          (0x01) // 101ms
#define TSL2561_INTEGRATIONTIME_402MS         (0x02) // 402ms
#define TSL2561_READBIT                   (0x01)
#define TSL2561_COMMAND_BIT                (0x80)   //Must be 1
#define TSL2561_CLEAR_BIT                (0x40)   //Clears any pending interrupt (write 1 to clear)
#define TSL2561_WORD_BIT                   (0x20)   // 1 = read/write word (rather than byte)
#define TSL2561_BLOCK_BIT                  (0x10)   // 1 = using block read/write
#define TSL2561_REGISTER_CONTROL           (0x00)
#define TSL2561_REGISTER_TIMING            (0x81)
#define TSL2561_REGISTER_THRESHHOLDL_LOW      (0x02)
#define TSL2561_REGISTER_THRESHHOLDL_HIGH     (0x03)
#define TSL2561_REGISTER_THRESHHOLDH_LOW      (0x04)
#define TSL2561_REGISTER_THRESHHOLDH_HIGH     (0x05)
#define TSL2561_REGISTER_INTERRUPT            (0x06)
#define TSL2561_REGISTER_CRC                  (0x08)
#define TSL2561_REGISTER_ID                   (0x0A)
#define TSL2561_REGISTER_CHAN0_LOW            (0x8C)
#define TSL2561_REGISTER_CHAN0_HIGH           (0x8D)
#define TSL2561_REGISTER_CHAN1_LOW            (0x8E)
#define TSL2561_REGISTER_CHAN1_HIGH           (0x8F)
//Delay getLux function
#define LUXDELAY 500

int getLux(int fd){
  // Enable the device
  wiringPiI2CWriteReg8(fd, TSL2561_COMMAND_BIT, TSL2561_CONTROL_POWERON);
  // Set timing (101 mSec)
  wiringPiI2CWriteReg8(fd, TSL2561_REGISTER_TIMING, TSL2561_GAIN_AUTO);
  //Wait for the conversion to complete
  delay(LUXDELAY);
  //Reads visible + IR diode from the I2C device auto
  uint16_t visible_and_ir = wiringPiI2CReadReg16(fd, TSL2561_REGISTER_CHAN0_LOW);
  // Disable the device
  wiringPiI2CWriteReg8(fd, TSL2561_COMMAND_BIT, TSL2561_CONTROL_POWEROFF);
  return visible_and_ir * 2;
}

void main(){
  int fd = wiringPiI2CSetup(TSL2561_ADDR_FLOAT);
  printf("Lux: %d\n", getLux(fd));
}
