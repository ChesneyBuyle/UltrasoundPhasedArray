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
 *      Created: 2020-07-30
 *       Author: Chesney Buyle
 *      Version: 1.0
 *
 *  Description: multiplexer
 *
 *  Commissiond by KU Leuven
 *
 *  License L (optionally)
 */
 
#ifndef MUX_H
#define MUX_H

#include "spi.h"
#include "stm32h7xx_hal.h"
#include <stdbool.h>

void mux_init(void);
void enable_mux(void);
void disable_mux(void);
void set_mux(uint8_t ctrl);
bool isBitSet(uint8_t b, uint8_t pos);

#endif
