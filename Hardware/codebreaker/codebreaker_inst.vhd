	component codebreaker is
		port (
			clk_clk                                              : in    std_logic                    := 'X';             -- clk
			reset_reset_n                                        : in    std_logic                    := 'X';             -- reset_n
			hex5_external_connection_export                      : out   std_logic_vector(7 downto 0);                    -- export
			hex4_external_connection_export                      : out   std_logic_vector(7 downto 0);                    -- export
			hex3_external_connection_export                      : out   std_logic_vector(7 downto 0);                    -- export
			hex2_external_connection_export                      : out   std_logic_vector(7 downto 0);                    -- export
			hex1_external_connection_export                      : out   std_logic_vector(7 downto 0);                    -- export
			hex0_external_connection_export                      : out   std_logic_vector(7 downto 0);                    -- export
			accelerometer_spi_0_external_interface_I2C_SDAT      : inout std_logic                    := 'X';             -- I2C_SDAT
			accelerometer_spi_0_external_interface_I2C_SCLK      : out   std_logic;                                       -- I2C_SCLK
			accelerometer_spi_0_external_interface_G_SENSOR_CS_N : out   std_logic;                                       -- G_SENSOR_CS_N
			accelerometer_spi_0_external_interface_G_SENSOR_INT  : in    std_logic                    := 'X';             -- G_SENSOR_INT
			led_external_connection_export                       : out   std_logic_vector(9 downto 0);                    -- export
			button_external_connection_export                    : in    std_logic_vector(3 downto 0) := (others => 'X'); -- export
			switch_external_connection_export                    : in    std_logic_vector(9 downto 0) := (others => 'X')  -- export
		);
	end component codebreaker;

	u0 : component codebreaker
		port map (
			clk_clk                                              => CONNECTED_TO_clk_clk,                                              --                                    clk.clk
			reset_reset_n                                        => CONNECTED_TO_reset_reset_n,                                        --                                  reset.reset_n
			hex5_external_connection_export                      => CONNECTED_TO_hex5_external_connection_export,                      --               hex5_external_connection.export
			hex4_external_connection_export                      => CONNECTED_TO_hex4_external_connection_export,                      --               hex4_external_connection.export
			hex3_external_connection_export                      => CONNECTED_TO_hex3_external_connection_export,                      --               hex3_external_connection.export
			hex2_external_connection_export                      => CONNECTED_TO_hex2_external_connection_export,                      --               hex2_external_connection.export
			hex1_external_connection_export                      => CONNECTED_TO_hex1_external_connection_export,                      --               hex1_external_connection.export
			hex0_external_connection_export                      => CONNECTED_TO_hex0_external_connection_export,                      --               hex0_external_connection.export
			accelerometer_spi_0_external_interface_I2C_SDAT      => CONNECTED_TO_accelerometer_spi_0_external_interface_I2C_SDAT,      -- accelerometer_spi_0_external_interface.I2C_SDAT
			accelerometer_spi_0_external_interface_I2C_SCLK      => CONNECTED_TO_accelerometer_spi_0_external_interface_I2C_SCLK,      --                                       .I2C_SCLK
			accelerometer_spi_0_external_interface_G_SENSOR_CS_N => CONNECTED_TO_accelerometer_spi_0_external_interface_G_SENSOR_CS_N, --                                       .G_SENSOR_CS_N
			accelerometer_spi_0_external_interface_G_SENSOR_INT  => CONNECTED_TO_accelerometer_spi_0_external_interface_G_SENSOR_INT,  --                                       .G_SENSOR_INT
			led_external_connection_export                       => CONNECTED_TO_led_external_connection_export,                       --                led_external_connection.export
			button_external_connection_export                    => CONNECTED_TO_button_external_connection_export,                    --             button_external_connection.export
			switch_external_connection_export                    => CONNECTED_TO_switch_external_connection_export                     --             switch_external_connection.export
		);

