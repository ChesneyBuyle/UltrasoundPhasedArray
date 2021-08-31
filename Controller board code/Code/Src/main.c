/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "spi.h"
#include "tim.h"
#include "usart.h"
#include "usb_device.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

#include "AD9834.h"
#include "AD5270_71.h"
#include "mux.h"
//#include "matrix.h"
#include "defines.h"
#include "usbd_cdc_if.h"

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

extern TIM_HandleTypeDef htim4;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_SPI1_Init();
  MX_SPI3_Init();
  MX_SPI4_Init();
  MX_SPI5_Init();
  MX_USART3_UART_Init();
  MX_USB_DEVICE_Init();
  MX_TIM4_Init();
  /* USER CODE BEGIN 2 */
	
	uint8_t devices[NUM_DEVICES] = {0x03, 0x0B, 0x01, 0x09, 0x07, 0x05, 0x0F, 0x0D, 0x00, 0x02};
	
	mux_init();
	AD9834_global_init(devices);
	AD5270_71_global_init(devices);

	// Enable timer to generate clock signal (Master clock DDS)
	HAL_TIM_Base_Start(&htim4);
	HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_3);
	
	//AD9834_init();
	//AD5270_71_init();
	
	// matrix_init();

	
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
	
	write_RDAC(0x0D, 15000);
	write_RDAC(0x0F, 15000);
	write_RDAC(0x05, 15000);
	write_RDAC(0x07, 15000);
	write_RDAC(0x09, 15000);
	write_RDAC(0x0B, 15000);
	write_RDAC(0x01, 15000);
	write_RDAC(0x03, 15000);
	write_RDAC(0x00, 15000);
	write_RDAC(0x02, 15000);
	
  while (1)
  {
		uint8_t dataBuffer[PAYLOAD_SIZE];
		
		uint8_t numBytesReceived = 0;
		uint8_t ch;
		
		while (numBytesReceived < PAYLOAD_SIZE){
			// Read bytes one by one from the receive ring buffer
			if (CDC_Read_FS(&ch, 1) == 0){
				dataBuffer[numBytesReceived++] = ch;
			}
		}
		
		// 
		uint8_t command = dataBuffer[COMMAND_PAYLOAD_OFFSET];
		
		switch(command){
			
			// Change settings specific speaker element
			case CHANGE_SPEAKER_SETTING:
			{
				uint8_t dev = dataBuffer[DEV_PAYLOAD_OFFSET];
				uint16_t frequency = dataBuffer[FREQ_MSB_PAYLOAD_OFFSET] << 8 | dataBuffer[FREQ_LSB_PAYLOAD_OFFSET];
				uint16_t phase = dataBuffer[PHASE_MSB_PAYLOAD_OFFSET] << 8 | dataBuffer[PHASE_LSB_PAYLOAD_OFFSET];
				uint16_t amplitude = dataBuffer[AMP_MSB_PAYLOAD_OFFSET] << 8 | dataBuffer[AMP_LSB_PAYLOAD_OFFSET];
					
				AD9834_set(dev, 0, frequency, phase);
				write_RDAC(dev, amplitude);
				
				// Send 'OK' if command is received
				uint8_t resp[11];
				sprintf(resp, "OK DEV(%d)\n", dev);
				CDC_Transmit_FS(resp, sizeof(resp));
			}
				break;
			
			// Disable (sleep) specific speaker element
			case DISABLE_SPEAKER:
			{
				uint8_t dev = dataBuffer[DEV_PAYLOAD_OFFSET];
				AD9834_disable(dev);
			}
				break;
			case CHANGE_SPEAKER_VGA:
			{
				uint8_t dev = dataBuffer[DEV_PAYLOAD_OFFSET];
				uint16_t frequency = dataBuffer[FREQ_MSB_PAYLOAD_OFFSET] << 8 | dataBuffer[FREQ_LSB_PAYLOAD_OFFSET];
				uint16_t phase = dataBuffer[PHASE_MSB_PAYLOAD_OFFSET] << 8 | dataBuffer[PHASE_LSB_PAYLOAD_OFFSET];
				uint16_t amplitude = dataBuffer[AMP_MSB_PAYLOAD_OFFSET] << 8 | dataBuffer[AMP_LSB_PAYLOAD_OFFSET];	
				
				write_RDAC(dev, amplitude);
				
				// Send 'OK' if command is received
				uint8_t resp[11];
				sprintf(resp, "OK DEV(%d)\n", dev);
				CDC_Transmit_FS(resp, sizeof(resp));				
			}
				break;
			case CHANGE_SPEAKER_FREQUENCY:
			{
				uint8_t dev = dataBuffer[DEV_PAYLOAD_OFFSET];
				uint16_t frequency = dataBuffer[FREQ_MSB_PAYLOAD_OFFSET] << 8 | dataBuffer[FREQ_LSB_PAYLOAD_OFFSET];
				uint16_t phase = dataBuffer[PHASE_MSB_PAYLOAD_OFFSET] << 8 | dataBuffer[PHASE_LSB_PAYLOAD_OFFSET];
				uint16_t amplitude = dataBuffer[AMP_MSB_PAYLOAD_OFFSET] << 8 | dataBuffer[AMP_LSB_PAYLOAD_OFFSET];	
				
				setFrequencyRegister(dev, 0, frequency);
				
				// Send 'OK' if command is received
				uint8_t resp[11];
				sprintf(resp, "OK DEV(%d)\n", dev);
				CDC_Transmit_FS(resp, sizeof(resp));				
			}
				break;
			case CHANGE_SPEAKER_PHASE:
			{
				uint8_t dev = dataBuffer[DEV_PAYLOAD_OFFSET];
				uint16_t frequency = dataBuffer[FREQ_MSB_PAYLOAD_OFFSET] << 8 | dataBuffer[FREQ_LSB_PAYLOAD_OFFSET];
				uint16_t phase = dataBuffer[PHASE_MSB_PAYLOAD_OFFSET] << 8 | dataBuffer[PHASE_LSB_PAYLOAD_OFFSET];
				uint16_t amplitude = dataBuffer[AMP_MSB_PAYLOAD_OFFSET] << 8 | dataBuffer[AMP_LSB_PAYLOAD_OFFSET];	
			
				setPhaseRegister(dev, 0, phase);
				
				// Send 'OK' if command is received
				uint8_t resp[11];
				sprintf(resp, "OK DEV(%d)\n", dev);
				CDC_Transmit_FS(resp, sizeof(resp));				
			}
				break;
			default:
				break;
		}

		// HAL_Delay(10);
//		
//		/*
//		uint8_t test = 0;
//		uint8_t testBuffer[4] = {0};
//		
//		uint8_t numBytes = 0;
//		bool endCharacter = false;
//		
//		while (numBytes < 4 && !endCharacter){
//			if (CDC_Read_FS(&test, 1) == 0){
//				testBuffer[numBytes] = test;
//				numBytes++;
//				
//				if (test == '\n'){
//					endCharacter = true;
//				}
//			}
//		}
//			
//		CDC_Transmit_FS(testBuffer, sizeof(testBuffer));	
//		HAL_Delay(1000);
//		*/		
//		
//		/*	
//		if (CDC_Read_FS(&test, 1) == 0){
//			uint8_t buffer[] = "Hello, World!\r\n";
//			CDC_Transmit_FS(buffer, sizeof(buffer));
//						
//		}
//		HAL_Delay(1000);	
//		*/

//	setFrequencyRegister(0x0D, 0, 40000);
//	setFrequencyRegister(0x0F, 0, 40000);
//	setFrequencyRegister(0x05, 0, 40000);
//	setFrequencyRegister(0x07, 0, 40000);
//	setFrequencyRegister(0x09, 0, 40000);
//	setFrequencyRegister(0x0B, 0, 40000);
//	setFrequencyRegister(0x01, 0, 40000);
//	setFrequencyRegister(0x03, 0, 40000);
//	setFrequencyRegister(0x00, 0, 40000);
//	setFrequencyRegister(0x02, 0, 40000);
//	
//	setPhaseRegister(0x03, 0, 0);

//	HAL_Delay(2000);
//	
//	setPhaseRegister(0x01, 0, 90);
//	setPhaseRegister(0x09, 0, 90);
//	setPhaseRegister(0x0B, 0, 90);
//	setPhaseRegister(0x05, 0, 90);
//	setPhaseRegister(0x07, 0, 90);
//	setPhaseRegister(0x0D, 0, 90);
//	setPhaseRegister(0x0F, 0, 90);
//	setPhaseRegister(0x00, 0, 90);
//	setPhaseRegister(0x02, 0, 90);
//	HAL_Delay(2000);
//	setPhaseRegister(0x01, 0, 0);
//	setPhaseRegister(0x09, 0, 0);
//	setPhaseRegister(0x0B, 0, 0);
//	setPhaseRegister(0x05, 0, 0);
//	setPhaseRegister(0x07, 0, 0);
//	setPhaseRegister(0x0D, 0, 0);
//	setPhaseRegister(0x0F, 0, 0);
//	setPhaseRegister(0x00, 0, 0);
//	setPhaseRegister(0x02, 0, 0);
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInitStruct = {0};

  /** Supply configuration update enable
  */
  HAL_PWREx_ConfigSupply(PWR_LDO_SUPPLY);
  /** Configure the main internal regulator output voltage
  */
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE3);

  while(!__HAL_PWR_GET_FLAG(PWR_FLAG_VOSRDY)) {}
  /** Initializes the CPU, AHB and APB busses clocks
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI|RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_BYPASS;
  RCC_OscInitStruct.HSIState = RCC_HSI_DIV1;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLM = 1;
  RCC_OscInitStruct.PLL.PLLN = 24;
  RCC_OscInitStruct.PLL.PLLP = 2;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  RCC_OscInitStruct.PLL.PLLR = 2;
  RCC_OscInitStruct.PLL.PLLRGE = RCC_PLL1VCIRANGE_3;
  RCC_OscInitStruct.PLL.PLLVCOSEL = RCC_PLL1VCOWIDE;
  RCC_OscInitStruct.PLL.PLLFRACN = 0;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB busses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2
                              |RCC_CLOCKTYPE_D3PCLK1|RCC_CLOCKTYPE_D1PCLK1;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.SYSCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB3CLKDivider = RCC_APB3_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_APB1_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_APB2_DIV1;
  RCC_ClkInitStruct.APB4CLKDivider = RCC_APB4_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInitStruct.PeriphClockSelection = RCC_PERIPHCLK_USART3|RCC_PERIPHCLK_SPI5
                              |RCC_PERIPHCLK_SPI4|RCC_PERIPHCLK_SPI3
                              |RCC_PERIPHCLK_SPI1|RCC_PERIPHCLK_USB;
  PeriphClkInitStruct.Spi123ClockSelection = RCC_SPI123CLKSOURCE_PLL;
  PeriphClkInitStruct.Spi45ClockSelection = RCC_SPI45CLKSOURCE_D2PCLK1;
  PeriphClkInitStruct.Usart234578ClockSelection = RCC_USART234578CLKSOURCE_D2PCLK1;
  PeriphClkInitStruct.UsbClockSelection = RCC_USBCLKSOURCE_PLL;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Enable USB Voltage detector
  */
  HAL_PWREx_EnableUSBVoltageDetector();
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     tex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
