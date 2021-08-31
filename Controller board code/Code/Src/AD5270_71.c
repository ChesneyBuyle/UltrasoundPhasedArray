#include "AD5270_71.h"
#include "mux.h"
#include "defines.h"

extern SPI_HandleTypeDef hspi5;

uint8_t cmd_buf[2];
uint8_t testdata;

void AD5270_71_global_init(uint8_t* devices){	
	for (uint8_t i=0; i<NUM_DEVICES; i++){
		uint8_t device = *(devices+i);
		
		// Power up from shutdown
		write_reg_ad5270(device, 0x2400);	
		
		// Allow update of wiper position through SPI - command 7
		write_reg_ad5270(device, 0x1C02);
		
		// HAL_Delay(1);
		
		// Set initial wiper position
		write_RDAC(device, 5000.0); // Set initial wiper position to 10 kOhm		
	}
}
void AD5270_71_init(uint8_t dev){
	// Power up from shutdown
	write_reg_ad5270(dev, 0x2400);
	
	// Allow update of wiper position through SPI - command 7
	write_reg_ad5270(dev, 0x1C02);
	
	//HAL_Delay(1);
	
	// Set initial wiper position
	write_RDAC(dev, 10000.0); // Set initial wiper position to 10 kOhm
	
	// Shut down the potentiometer
	//HAL_Delay(1);
	//write_reg_ad5270(0x2401);
	
}

void write_RDAC(uint8_t dev, float resistance){
	// Calculate wiper value that corresponds with the resistance value
	uint16_t RDAC_value = (uint16_t)((resistance/50000.0)*1024.0);
	
	// Construct the command for changing the wiper position
	uint16_t write_wiper_cmd = WRITE_RDAC << 8 | RDAC_value;
	
	// Allow update of wiper position through SPI - command 7
	write_reg_ad5270(dev, 0x1C02);
	
	// Update the wiper position
	write_reg_ad5270(dev, write_wiper_cmd);
}

void write_reg_ad5270(uint8_t dev, uint16_t command){	
	cmd_buf[0] = (uint8_t) (command & 0xFF);
	cmd_buf[1] = (uint8_t) ((command >> 8) & 0xFF);
	
	//testdata = cmd_buf[0];
	//testdata = cmd_buf[1];
		
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
	HAL_SPI_Transmit(&hspi5, cmd_buf, 1, 100);
	
	// DELETE: DEBUG PURPOSE
	// HAL_GPIO_WritePin(GPIOG, GPIO_PIN_12, GPIO_PIN_SET);
	
	disable_mux();
	
}
