/*  ____  ____      _    __  __  ____ ___
 * |  _ \|  _ \    / \  |  \/  |/ ___/ _ \
 * | | | | |_) |  / _ \ | |\/| | |  | | | |
 * | |_| |  _ <  / ___ \| |  | | |__| |_| |
 * |____/|_| \_\/_/   \_\_|  |_|\____\___/
 *                           research group
 *                             dramco.be/
 *
 *  KU Leuven - Technology Campus Gent,
 *  Gebroeders De Smetstraat 1,
 *  B-9000 Gent, Belgium
 *
 *         File: AD5270_71.c
 *      Created: 2020-04-29
 *       Author: Chesney Buyle
 *      Version: 1.0
 *
 *  Description: Analog Devices AD5270 SPI Digital Potentiometer
 *
 *  Commissiond by KU Leuven
 *
 *  License L (optionally)
 */

#ifndef AD5270_H
#define AD5270_H

#include "spi.h"
#include "stm32h7xx_hal.h"

#define MAX_RESISTANCE 50000 // in Ohm

typedef enum {
	NO_OP               =  0x00,    ///< No data
  NO_OP_cmd           =  0x0000,  ///< 16 bit no data
  WRITE_RDAC          =  0x04,    ///< Write to the RDAC Register
  READ_RDAC           =  0x08,    ///< Read from the RDAC Register
  STORE_50TP          =  0x0C,    ///< Write from RDAC to memory
  SW_RST              =  0x10,    ///< Software reset to last memory location
  READ_50TP_CONTENTS  =  0x14,    ///< Read the last memory contents
  READ_50TP_ADDRESS   =  0x18,    ///< Read the last memory address
  WRITE_CTRL_REG      =  0x1C,    ///< Write to the control Register
  READ_CTRL_REG       =  0x20,    ///< Read from the control Register
  SW_SHUTDOWN         =  0x24,    ///< Software shutdown (0) - Normal, (1) - Shutdown
  HI_Zupper           =  0x80,    ///< Get the SDO line ready for High Z
  HI_Zlower           =  0x01,    ///< Puts AD5270 into High Z mode
  HI_Z_Cmd            =  0x8001   ///< Puts AD5270 into High Z mode*/
} AD5270Commands_t;

void AD5270_71_global_init(uint8_t* devices);
void AD5270_71_init(uint8_t dev);
void write_RDAC(uint8_t dev, float resistance);
void write_reg_ad5270(uint8_t dev, uint16_t command);

#endif
