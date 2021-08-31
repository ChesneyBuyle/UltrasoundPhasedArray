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
 *         File: AD9834.c
 *      Created: 2020-04-29
 *       Author: Chesney Buyle
 *      Version: 1.0
 *
 *  Description: Analog Devices AD9834 SPI Digital DDS
 *
 *  Commissiond by KU Leuven
 *
 *  License L (optionally)
 */

#ifndef AD9834_H
#define AD9834_H

#include "spi.h"
#include "stm32h7xx_hal.h"

#define REG_FREQ1   0x8000
#define REG_FREQ0   0x4000
#define REG_PHASE0  0xC000
#define REG_PHASE1  0xE000

#define REG_B28     0x2000
#define REG_HLB     0x1000
#define REG_FSEL    0x0800
#define REG_PSEL    0x0400
#define REG_PINSW   0x0200
#define REG_RESET   0x0100
#define REG_SLEEP1  0x0080
#define REG_SLEEP12 0x0040
#define REG_OPBITEN 0x0020
#define REG_SIGNPIB 0x0010
#define REG_DIV2    0x0008
#define REG_MODE    0x0002

void AD9834_global_init(uint8_t* devices);
void AD9834_init(uint8_t dev);
void AD9834_set(uint8_t dev, uint8_t reg, float frequency, float phase);
void AD9834_start(void);
void AD9834_disableAll(void);
void AD9834_disable(uint8_t dev);
void setFrequencyRegister(uint8_t dev, uint8_t reg, float frequency);
void setPhaseRegister(uint8_t dev, uint8_t reg, float phase);
void write_reg_ad9834(uint8_t dev, uint16_t command);

	
#endif
