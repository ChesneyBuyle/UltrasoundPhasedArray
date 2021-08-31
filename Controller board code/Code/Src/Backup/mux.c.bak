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
 
 #include "mux.h"
 
 uint8_t test1 = 0;
 uint8_t test2 = 0;
 
 void mux_init(void){
	 // Disable MUX_EN (ACTIVE LOW)	
	 // Disable MUX_EN_B (ACTIVE LOW)
	 HAL_GPIO_WritePin(MUX_EN_GPIO_Port, MUX_EN_Pin, GPIO_PIN_SET);
	 HAL_GPIO_WritePin(MUX_EN_B_GPIO_Port, MUX_EN_B_Pin, GPIO_PIN_SET);
 }
 
 void enable_mux(void){
	 HAL_GPIO_WritePin(MUX_EN_GPIO_Port, MUX_EN_Pin, GPIO_PIN_RESET);
	 HAL_GPIO_WritePin(MUX_EN_B_GPIO_Port, MUX_EN_B_Pin, GPIO_PIN_RESET);
 }
 
 void disable_mux(void){
 	HAL_GPIO_WritePin(MUX_EN_B_GPIO_Port, MUX_EN_B_Pin, GPIO_PIN_SET);
	HAL_GPIO_WritePin(MUX_EN_GPIO_Port, MUX_EN_Pin, GPIO_PIN_SET);
 }
 
 bool isBitSet(uint8_t b, uint8_t pos){
	 return (b & (1 << pos)) != 0;
 }
 
 void set_mux(uint8_t ctrl){
	// Set A2 output of 1:4 MUX HIGH
	HAL_GPIO_WritePin(GPIOD, S0_M4A_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOE, S1_M4A_Pin, GPIO_PIN_SET);
	
	// Set output of 1:16 MUX according to uint8_t ctrl 
	 
	// ternary-operator : condition ? value_if_true : value_if_false 
	
	HAL_GPIO_WritePin(GPIOG, S0_M16_B_Pin, ((ctrl >> 3) & 0x01)?GPIO_PIN_SET:GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOG, S1_M16_B_Pin, ((ctrl >> 2) & 0x01)?GPIO_PIN_SET:GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOD, S2_M16_B_Pin, ((ctrl >> 1) & 0x01)?GPIO_PIN_SET:GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOD, S3_M16_B_Pin, ((ctrl >> 0) & 0x01)?GPIO_PIN_SET:GPIO_PIN_RESET);	
 }
 