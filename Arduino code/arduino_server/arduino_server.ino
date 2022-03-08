#include <ESP8266WiFi.h>

#define SendKey 0  //Button to send data Flash BTN on NodeMCU

//initialising for the string
const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
boolean newData = false;

//WIFI initialising
int port = 11000; //Port number --- CHANGES DEPENDING ON BOARD
WiFiServer server(port);
int index = 0;
char buffer[1000];

//Server connect to WiFi Network
const char *ssid = "OnePlus7";  //Enter your wifi SSID
const char *password = "arduinotest";  //Enter your wifi Password

int count=0;
//=======================================================================
//                    Power on setup
//=======================================================================
void setup() {
    Serial.begin(9600);
    Serial.println("<Arduino is ready>");

    //WIFI setup...
    pinMode(SendKey,INPUT_PULLUP);  //Btn to send data
    Serial.println();

    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password); //Connect to wifi
    Serial.print("Connecting... "); 
    // Wait for connection  
    Serial.println("Connecting to Wifi");
    while (WiFi.status() != WL_CONNECTED) {   
    delay(500);
    Serial.print(".");
    delay(500);
    }

    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
  
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());  
    server.begin();
    Serial.print("Open Telnet and connect to IP:");
    Serial.print(WiFi.localIP());
    Serial.print(" on port ");
    Serial.println(port);
}

    

void loop() {
    recvWithEndMarker();
    showNewData();

    WiFiClient client = server.available();
    if (client) {
      if(client.connected())
      {
        Serial.println("Client Connected");
      }
      
      while(client.connected()){      
        while(client.available()>0){
          //read data from the connected client
          Serial.write(client.read()); 
          char client_response = client.read();
          while (index < 999){
            buffer[index] =  client_response;
            index++;
            buffer[index] = '\0';
          }
          if(client_response == "your turn"){
            //writing to serial monitor the "your turn"
            Serial.write(client.read());
            //sending FPGA response to client (receivedChars contains this)
            client.write(receivedChars);
            //output what i sent
            Serial.write("Sent message" + receivedChars);
            //receive the passcheckers response
            Serial.write(client.read());
          }
          
        }
        //Send Data to connected client
//        while(Serial.available()>0)
//        {
//          client.write(Serial.read());
//        }
      }
      client.stop();
      Serial.println("Client disconnected");    
    }
}







//Receiving functions from UART//

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;
    
    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (rc != endMarker) {
            receivedChars[ndx] = rc;
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else {
            receivedChars[ndx] = '\0'; // terminate the string
            ndx = 0;
            newData = true;
        }
    }
}

void showNewData() {
    if (newData == true) {
        Serial.print("FPGA UART: ");
        Serial.println(receivedChars);
        newData = false;
    }
}
