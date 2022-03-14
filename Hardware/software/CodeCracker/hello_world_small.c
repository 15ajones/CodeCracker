#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "altera_avalon_pio_regs.h"
#include "altera_avalon_uart.h"
#include "altera_avalon_uart_regs.h"
#include "sys/alt_irq.h"
#include "alt_types.h"
#include "sys/times.h"
#include <stdlib.h>
#include <stdio.h>
#include <sys/alt_stdio.h>
#include <unistd.h>
#include <string.h>

#define OFFSET -32
#define PWM_PERIOD 16
#define LEFTLIM 140
#define RIGHTLIM -140
#define FORWARDLIM -130 //different allowance for forward allowance
#define BACKWARDLIM 130
#define CHARLIM 256	//Maximum character length of what the user places in memory.  Increase to allow longer sequences
#define CLOCKINIT 300000	//Initial speed of the display.  This is a good starting point

/////////////////////////////////////////////////////////////////////////
//////////DISPLAY VARIABLES AND INITIALISATION///////////////////////////

int serverdata; // response from server - we are going to make it an integer for simplicity...
char prevserverdata;
int getActualText();
void clearActualText();
int updateTimer(int tmr);
int updateLocation(int loc, int len);
int getBin(char letter);
int getBinaryLetter(char letter);
void print(int let5, int let4, int let3, int let2, int let1, int let0);
void print_letters(char let5, char let4, char let3, char let2, char let1, char let0);

char enteredText[CHARLIM]; //The text that the user enters
char text[2*CHARLIM];//The text that has been adjusted for the allowed letters
int length;
int location;
int static_flag; //this is gonna be as a response from an input from the database
int admin_flag;
int timer = CLOCKINIT;  //Standard speed for movement

///////////////////////////////////////////////////////////////////////////
/////DISPLAY FUNCTIONS///////

//Does initial setup of display
void initializeDisplay(){
	//These controls determine what functions the display is executing:
	prevserverdata = '0';
	serverdata = 5;   //random number to set server data not eqaualling any of the below...
	//First Turn all six of the seven segment displays off
	print(getBin('!'), getBin('!'), getBin('!'), getBin('!'), getBin('!'), getBin('!'));
}

char updateText(int serverdata){ // in FPGA change this to if there is any new input

	if (serverdata == '2'){ // 2 is the code when "your turn" is sent by the server
		static_flag = 0; //play scrolls through
		enteredText[0] = 'p';
		length = getActualText();
		enteredText[1] = 'l';
		length = getActualText();
		enteredText[2] = 'a';
		length = getActualText();
		enteredText[3] = 'y';
		length = getActualText();
		enteredText[4] = ' ';
		length = getActualText();
		enteredText[5] = ' ';
		length = getActualText();
	}
	if(serverdata == 1){ //if the server isn't telling fpga to play and fpga is the admin, show word "ADMIN"
		static_flag = 1; //admin is shown statically
		enteredText[0] = 'a';
		length = getActualText();
		enteredText[1] = 'd';
		length = getActualText();
		enteredText[2] = 'm';
		length = getActualText();
		enteredText[3] = 'i';
		length = getActualText();
		enteredText[4] = 'n';
		length = getActualText();
		enteredText[5] = ' ';
		length = getActualText();
	}
	else{ //when leds don't show play, if player is not admin, show player number
		//alt_putstr("here :) \n"); for testing
		static_flag = 1;
		enteredText[0] = 'p';
		length = getActualText();
		enteredText[1] = '1';
		length = getActualText();
		enteredText[2] = ' ';
		length = getActualText();
		enteredText[3] = ' ';
		length = getActualText();
		enteredText[4] = ' ';
		length = getActualText();
		enteredText[5] = ' ';
		length = getActualText();
		}
	}
	return &enteredText[0];
}

int getActualText(){
	int idx = 0;	//We need two indicies because the entered and actual text sequences need not be aligned
	char currentLetter; //Keeps track of the character we are wanting to add
	//Go through each letter in the entered text
	for (int i = 0; i <= length; i++){
		currentLetter = enteredText[i];
		if (currentLetter > 96){
			//Gets only the uppercase letter
			currentLetter -= 32;
		}
		switch(currentLetter){
		case 'M':
			//We build the letter "M" from two "n's," so we need to change the index twice in the actual text
			text[idx] = 'N';
			text[idx + 1] = 'N';
			idx += 2;
			break;
		case 'W':
			//We build the letter "W" from two "v's," so we need to change the index twice in the actual text
			text[idx] = 'V';
			text[idx + 1] = 'V';
			idx += 2;
			break;
		default:
			//Copy the new letter into the actual text
			text[idx] = currentLetter;
			idx++;
		}
	}
	return idx;
}


//This function updates the timer based on whether the user has toggled a speedup or slowdown
int updateTimer(int tmr){
		return tmr;
}

//This function returns a new Location based on the previous one.
int updateLocation(int loc, int len){
	loc++;   //Move the display forwards if the backwards button is NOT toggled (KEY2)
	return loc;
}

//Gets the binary representation of the character
int getBin(char letter){
	/*Based on the character entered, we convert to binary so the 7-segment knows which lights to turn on.
	The 7-segment has inverted logic so a 0 means the light is on and a 1 means the light is off.
	The rightmost bit starts the index at HEX#[0], and the leftmost bit is HEX#[6], the pattern
	for the 7-segment is shown in the DE0_C5 User Manual*/
	switch(letter){
	case '0':
		return 0b1000000;
	case '1':
		return 0b1111001;
	case '2':
		return 0b0100100;
	case '3':
		return 0b0110000;
	case '4':
		return 0b0011001;
	case '5':
	case '6':
		return 0b0000010;
	case '7':
		return 0b1111000;
	case '8':
		return 0b0000000;
	case '9':
		return 0b0010000;
	case 'A':
		return 0b0001000;
	case 'B'://Lowercase
		return 0b0000011;
	case 'C':
		return 0b1000110;
	case 'D'://Lowercase
		return 0b0100001;
	case 'E':
		return 0b0000110;
	case 'F':
		return 0b0001110;
	case 'G':
		return 0b0010000;
	case 'H':
		return 0b0001001;
	case 'I':
		return 0b1111001;
	case 'J':
		return 0b1110001;
	case 'K':
		return 0b0001010;
	case 'L':
		return 0b1000111;
	case 'N':
		return 0b0101011;
	case 'O':
		return 0b1000000;
	case 'P':
		return 0b0001100;
	case 'Q':
		return 0b0011000;
	case 'R'://Lowercase
		return 0b0101111;
	case 'S':
		return 0b0010010;
	case 'T':
		return 0b0000111;
	case 'U':
		return 0b1000001;
	case 'V':
		return 0b1100011;
	case 'X':
		return 0b0011011;
	case 'Y':
		return 0b0010001;
	case 'Z':
		return 0b0100100;
	default:
		return 0b1111111;
	}
}

//Returns the letter or the upsideDown version of the letter
int getBinaryLetter(char letter){
	int let = getBin(letter);
	return let;
}
//Prints each of the letters out to the screen
void print(int let5, int let4, int let3, int let2, int let1, int let0){
	//Takes the binary value for each letter and places it on each of the six 7-segment displays
	IOWR_ALTERA_AVALON_PIO_DATA(HEX5_BASE, let5);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX4_BASE, let4);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX3_BASE, let3);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX2_BASE, let2);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX1_BASE, let1);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX0_BASE, let0);
	return;
}
//Prints each of the letters out to the screen; takes into account the dancing letters
void print_letters(char let5, char let4, char let3, char let2, char let1, char let0){

	//This is the "main" case, where the full letters are displayed on the display
	IOWR_ALTERA_AVALON_PIO_DATA(HEX5_BASE, getBinaryLetter(let5));
	IOWR_ALTERA_AVALON_PIO_DATA(HEX4_BASE, getBinaryLetter(let4));
	IOWR_ALTERA_AVALON_PIO_DATA(HEX3_BASE, getBinaryLetter(let3));
	IOWR_ALTERA_AVALON_PIO_DATA(HEX2_BASE, getBinaryLetter(let2));
	IOWR_ALTERA_AVALON_PIO_DATA(HEX1_BASE, getBinaryLetter(let1));
	IOWR_ALTERA_AVALON_PIO_DATA(HEX0_BASE, getBinaryLetter(let0));

	return;

}

//////////////////////////////////////////////////////////////////////////
//////////////LED INITIALISING/FUNCTIONS CODE//////////////////////////
alt_8 pwm = 0;
alt_u8 led;
int level;

void led_write(alt_u8 led_pattern) {
    IOWR(LED_BASE, 0, led_pattern);
}

void led_response(char check){
    if(check == 'y'){
        IOWR(LED_BASE, 0, 256);
    }else{
        IOWR(LED_BASE, 0, 16);
    }

}



void convert_read(alt_32 acc_read, int * level, alt_u8 * led) {
    acc_read += OFFSET;
    alt_u8 val = (acc_read >> 6) & 0x07;
    * led = (8 >> val) | (8 << (8 - val));
    * level = (acc_read >> 1) & 0x1f;
}

///////////Accelerometer reading DIRECTIONS/////////

const int FLATLOW = {-60};
const int FLATHIGH = {60};

int is_flat(alt_32 reading){
    if((reading < -60) || (reading > 60)){
        return 0;
    }else{
        return 1;
    }
}

////////////////////////////////////////////////

void sys_timer_isr() {
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);

    if (pwm < abs(level)) {

        if (level < 0) {
            led_write(led << 1);
        } else {
            led_write(led >> 1);
        }

    } else {
        led_write(led);
    }

    if (pwm > PWM_PERIOD) {
        pwm = 0;
    } else {
        pwm++;
    }

}

void timer_init(void * isr) {

    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0003);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0x0900);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0x0000);
    alt_irq_register(TIMER_IRQ, 0, isr);
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0007);

}

/////////////////////////////////////
///////////USELESS FIR//////////////
/////////////////////////////////////

//alt_32 FIR(alt_32 xn)
//{
//  // filter coefficients
//  //static float h[5] = {-0.0694, 0.1533,0.4369, 0.4369, 0.1533, -0.0694};
//  static float h[30] = {-0.0012, 0.0031, 0.0034, -0.0060, -0.0077, 0.0096, 0.0151, -0.0135, -0.0276, 0.0173, 0.0496, -0.0205, -0.0971, 0.0226, 0.3152, 0.4766, 0.3152, 0.0226, -0.0971, -0.0205, 0.0496, 0.0173, -0.0276, -0.0135, 0.0151, 0.0096, -0.0077, -0.0060, 0.0034, 0.0031, -0.0012};
//  // filter gain if applicable
//  static alt_32 hg = 1;
//
//  // delay line of time samples
//  static alt_32 xv[30] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
//
//  // filter output
//  alt_32 yn = 0;
//
//  // implementation of delay line
//  xv[29] = xv[28];
//  xv[28] = xv[27];
//  xv[27] = xv[26];
//  xv[26] = xv[25];
//  xv[25] = xv[24];
//  xv[24] = xv[23];
//  xv[23] = xv[22];
//  xv[22] = xv[21];
//  xv[21] = xv[20];
//  xv[20] = xv[19];
//  xv[19] = xv[18];
//  xv[18] = xv[17];
//  xv[17] = xv[16];
//  xv[16] = xv[15];
//  xv[15] = xv[14];
//  xv[14] = xv[13];
//  xv[13] = xv[12];
//  xv[12] = xv[11];
//  xv[11] = xv[10];
//  xv[10] = xv[9];
//  xv[9] = xv[8];
//  xv[8] = xv[7];
//  xv[7] = xv[6];
//  xv[6] = xv[5];
//  xv[5] = xv[4];
//  xv[4] = xv[3];
//  xv[3] = xv[2];
//  xv[2] = xv[1];
//  xv[1] = xv[0];
//  xv[0] = xn;
//
//  // convolve delay line by
//  // filter coefficients
//  for(int i=0;i<30;i++)
//  {
//    yn += h[i]*xv[i];
//  }
//  // apply gain
//  yn = hg*yn;
//  return yn;
//}

//////////////////////////////////////////////////
////////////////////////////////////////////////// END OF LED CODE...

///////////////////////////////
////////////MAIN///////////////
///////////////////////////////

int main() {

	//Display initialisation//
	initializeDisplay();

	///%Accelerometer initialisations%///
    alt_32 x_read;
    alt_32 y_read;
    alt_32 z_read;
    alt_up_accelerometer_spi_dev * acc_dev;
    acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    if (acc_dev == NULL) { // if return 1, check if the spi ip name is "accelerometer_spi"
        return 1;
    }

    ///%switches and buttons initialisation%///
    timer_init(sys_timer_isr);
    int button_datain;
    int switch_datain;
    char response[100];
    int flicked_switch;

    ///Code///
    while (1) {


    	///Switches code///
     	switch_datain = IORD_ALTERA_AVALON_PIO_DATA(SWITCH_BASE);
    	switch_datain &= (0b1111111111);

    	if(switch_datain != 0){
			flicked_switch = switch_datain;
			while(switch_datain != 0){
				//printf("here \n");
				switch_datain = IORD_ALTERA_AVALON_PIO_DATA(SWITCH_BASE);
				switch_datain &= (0b1111111111);
			}

			if(flicked_switch == 1){
				strcat(response,"1");
				printf("\nResponse: %s\n", response);
			}
			else if(flicked_switch == 2){
				strcat(response,"2");
				printf("\nResponse: %s\n", response);
			}
			else if(flicked_switch == 4){
				strcat(response,"3");
				printf("\nResponse: %s\n", response);
			}
//			else if(flicked_switch == 8){
//				response = '4\0';
//			}
//			else if(flicked_switch == 16){
//				response = '5\0';
//			}
//			else if(flicked_switch == 32){
//				response = '6\0';
//			}
//			else if(flicked_switch == 64){
//				response = '7\0';
//			}
//			else if(flicked_switch == 128){
//				response = '8\0';
//			}
//			else if(flicked_switch == 256){
//				response = '9\0';
//			}
//			else if(flicked_switch == 512){
//				response = '0\0';
//			}
			//printf("response = %d\n", response);

		}


    	////////////////////////////
    	////Accelerometer code//////

    	clock_t exec_t1, exec_t2;
    	exec_t1 = times(NULL);

        alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
        alt_up_accelerometer_spi_read_y_axis(acc_dev, & y_read);
        // alt_up_accelerometer_spi_read_z_axis(acc_dev, & z_read);
        alt_32 FIR_out[3];
        FIR_out[0] = x_read;
        FIR_out[1] = y_read;

        ///DEBUGGING//////
        //printf("FIR out x = %d \n", FIR_out[0]);
        //printf("FIR out y = %d \n", FIR_out[1]);
        //////////////////

        //Left & Right//
        if(FIR_out[0] < RIGHTLIM){
            while(is_flat(FIR_out[0]) == 0){
            	alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
            	FIR_out[0] = x_read;
            }
            strcat(response, "R");
            printf("\nResponse: %s\n", response);

        }else if(FIR_out[0] > LEFTLIM){
            while(is_flat(FIR_out[0]) == 0){
            	alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read);
            	FIR_out[0] = x_read;
            }
            strcat(response, "L");
            printf("\nResponse: %s\n", response);
        }

        //Forward & Backward//
        if(FIR_out[1] < FORWARDLIM){
			while(is_flat(FIR_out[1]) == 0){
				alt_up_accelerometer_spi_read_y_axis(acc_dev, & y_read);
				FIR_out[1] = y_read;
			}
			strcat(response, "F");
            printf("\nResponse: %s\n", response);

		}else if(FIR_out[1] > BACKWARDLIM){
			while(is_flat(FIR_out[1]) == 0){
				alt_up_accelerometer_spi_read_y_axis(acc_dev, & y_read);
				FIR_out[1] = y_read;
			}
			strcat(response, "B");
            printf("\nResponse: %s\n", response);
        }

        ////////////////////////
        //////send button///////
        int pressed=0;
        button_datain = ~IORD_ALTERA_AVALON_PIO_DATA(BUTTON_BASE);
		if((button_datain &= 0b0000000001) && (pressed == 0)){
			pressed = 1;
			strcat(response, "\n");
			int i = 0;
			while (response[i] != '\0'){
				IOWR_ALTERA_AVALON_UART_TXDATA(UART_0_BASE, response[i]);
				i++;
				usleep(10000) ;
			}
			printf("\nSending: %s\n", response);
			memset(response,0,strlen(response));
		}
		//reset button
		button_datain = ~IORD_ALTERA_AVALON_PIO_DATA(BUTTON_BASE);
		if((button_datain &= 0b0000000010) && (pressed==0)){
			pressed = 1;
			//reset response
			memset(response,0,strlen(response));
			printf("Resetting...\n");
		}
		else {
			usleep(50000);
		}

        //printf("<-> %c <->", response[100]);
        convert_read(x_read, & level, & led);



        /////////////////////
		///receiving shit////
		int received;
		received = IORD_ALTERA_AVALON_UART_RXDATA(UART_0_BASE); //watch out this is IORD not IOWR...
		printf("Received character: %d", received);




    }

    return 0;
}


