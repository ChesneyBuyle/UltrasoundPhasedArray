#include "AD9834.h" 
#include "mux.h"
#include "defines.h"

extern SPI_HandleTypeDef hspi4;

uint8_t testDataGen;

void AD9834_global_init(uint8_t* devices){
	// Set frequency register to FREQ0 and phase register to PHASE0
	HAL_GPIO_WritePin(GPIOE, FSELECT_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOA, PSELECT_Pin, GPIO_PIN_RESET);
	
	for (uint8_t i=0; i<NUM_DEVICES; i++){
		// Wake up the DDS (ACTIVE HIGH)
		HAL_GPIO_WritePin(SLEEP_GPIO_Port, SLEEP_Pin, GPIO_PIN_RESET);

		// Keep the DDS in reset to change internal settings (ACTIVE HIGH)
		HAL_GPIO_WritePin(RESET_GPIO_Port, RESET_Pin, GPIO_PIN_SET);
		
		write_reg_ad9834(*(devices+i), REG_B28|REG_PINSW);
		
		AD9834_set(*(devices+i), 0, 10000, 0);
		
		// Disable reset
		HAL_GPIO_WritePin(RESET_GPIO_Port, RESET_Pin, GPIO_PIN_RESET);
	}
}

void AD9834_init(uint8_t dev){
	// Set frequency register to FREQ0 and phase register to PHASE0
	HAL_GPIO_WritePin(GPIOE, FSELECT_Pin, GPIO_PIN_RESET);
	HAL_GPIO_WritePin(GPIOA, PSELECT_Pin, GPIO_PIN_RESET);
	
	// Wake up the DDS (ACTIVE HIGH)
	HAL_GPIO_WritePin(SLEEP_GPIO_Port, SLEEP_Pin, GPIO_PIN_RESET);
	
	// Keep the DDS in reset to change internal settings (ACTIVE HIGH)
	HAL_GPIO_WritePin(RESET_GPIO_Port, RESET_Pin, GPIO_PIN_SET);
	
	AD9834_set(dev, 0, 1000, 0);
	
	// Disable reset
	HAL_GPIO_WritePin(RESET_GPIO_Port, RESET_Pin, GPIO_PIN_RESET);
}

void AD9834_set(uint8_t dev, uint8_t reg, float frequency, float phase){
	// Keep the DDS in reset to change internal settings (ACTIVE HIGH)
	HAL_GPIO_WritePin(RESET_GPIO_Port, RESET_Pin, GPIO_PIN_SET);
	
	write_reg_ad9834(dev, REG_B28|REG_PINSW);
	
	//HAL_Delay(1);
	
	setFrequencyRegister(dev, reg, frequency);
	
	//HAL_Delay(1);
	
	setPhaseRegister(dev, reg, phase);
	
		// Disable reset
	HAL_GPIO_WritePin(RESET_GPIO_Port, RESET_Pin, GPIO_PIN_RESET);
}

void AD9834_start(void){
	// Start producing waveform by setting RESET LOW (ACTIVE HIGH)
	HAL_GPIO_WritePin(RESET_GPIO_Port, RESET_Pin, GPIO_PIN_SET);
}

void AD9834_disableAll(void){
	// Power down all DDSs: active high
	HAL_GPIO_WritePin(SLEEP_GPIO_Port, SLEEP_Pin, GPIO_PIN_SET);
}

void AD9834_disable(uint8_t dev){
	// SLEEP12 for specific device
	write_reg_ad9834(dev, REG_SLEEP12);
}

void setPhaseRegister(uint8_t dev, uint8_t reg, float phase){
	// Calculate the phase register control bits
	uint16_t phase_reg = (uint16_t)((phase/360)*4096);
	
	// ternary-operator : condition ? value_if_true : value_if_false 
	uint16_t cmd_phase = (reg?REG_PHASE1:REG_PHASE0) | (phase_reg & 0x0FFF);
	
	// Write control bits to the frequency registers (FREQ0 or FREQ1)
	write_reg_ad9834(dev, cmd_phase);
	
	HAL_GPIO_WritePin(RESET_GPIO_Port, RESET_Pin, GPIO_PIN_SET);
	HAL_Delay(1);
	HAL_GPIO_WritePin(RESET_GPIO_Port, RESET_Pin, GPIO_PIN_RESET);
}

void setFrequencyRegister(uint8_t dev, uint8_t reg, float frequency){
	uint32_t frequency_value = (uint32_t) ((frequency*0x10000000)/1000000);
	
	// ternary-operator : condition ? value_if_true : value_if_false 
	uint16_t cmd_LSB = ((reg?REG_FREQ1:REG_FREQ0) | (frequency_value & 0x3FFF));
	uint16_t cmd_MSB = ((reg?REG_FREQ1:REG_FREQ0) | ((frequency_value >> 14) & 0x3FFF));
	
	write_reg_ad9834(dev, cmd_LSB);
	write_reg_ad9834(dev, cmd_MSB);
	
	HAL_GPIO_WritePin(RESET_GPIO_Port, RESET_Pin, GPIO_PIN_SET);
	HAL_Delay(1);
	HAL_GPIO_WritePin(RESET_GPIO_Port, RESET_Pin, GPIO_PIN_RESET);
	
}

void write_reg_ad9834(uint8_t dev, uint16_t command){
	uint8_t cmd_buf[2];
	
	cmd_buf[0] = command & 0xFF;
	cmd_buf[1] = (command >> 8) & 0xFF;
	
	//set_mux(0x03);
	//set_mux(0x0B);
	//set_mux(0x09);
	//set_mux(0x01);
	
	set_mux(dev);
	enable_mux();
	
	//Temporary testing HAL_Delay(1);
	
	// DELETE: DEBUG PURPOSE
	// HAL_GPIO_WritePin(GPIOG, GPIO_PIN_12, GPIO_PIN_RESET);
	
	// Transmit data
	HAL_SPI_Transmit(&hspi4, cmd_buf, 1, 100);
	
	// DELETE: DEBUG PURPOSE
	// HAL_GPIO_WritePin(GPIOG, GPIO_PIN_12, GPIO_PIN_SET);
	
	disable_mux();
}
