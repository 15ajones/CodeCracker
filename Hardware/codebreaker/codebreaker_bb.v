
module codebreaker (
	clk_clk,
	reset_reset_n,
	hex5_external_connection_export,
	hex4_external_connection_export,
	hex3_external_connection_export,
	hex2_external_connection_export,
	hex1_external_connection_export,
	hex0_external_connection_export,
	accelerometer_spi_0_external_interface_I2C_SDAT,
	accelerometer_spi_0_external_interface_I2C_SCLK,
	accelerometer_spi_0_external_interface_G_SENSOR_CS_N,
	accelerometer_spi_0_external_interface_G_SENSOR_INT,
	led_external_connection_export,
	button_external_connection_export,
	switch_external_connection_export);	

	input		clk_clk;
	input		reset_reset_n;
	output	[7:0]	hex5_external_connection_export;
	output	[7:0]	hex4_external_connection_export;
	output	[7:0]	hex3_external_connection_export;
	output	[7:0]	hex2_external_connection_export;
	output	[7:0]	hex1_external_connection_export;
	output	[7:0]	hex0_external_connection_export;
	inout		accelerometer_spi_0_external_interface_I2C_SDAT;
	output		accelerometer_spi_0_external_interface_I2C_SCLK;
	output		accelerometer_spi_0_external_interface_G_SENSOR_CS_N;
	input		accelerometer_spi_0_external_interface_G_SENSOR_INT;
	output	[9:0]	led_external_connection_export;
	input	[3:0]	button_external_connection_export;
	input	[9:0]	switch_external_connection_export;
endmodule
