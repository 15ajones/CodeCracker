#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define SendKey 0  //Button to send data Flash BTN on NodeMCU

//initialising for the string
const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data


//WIFI initialising
WiFiUDP Udp;
// port to listen packets to
unsigned int localUdpPort = 11000;


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
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED){
    delay(500);
    Serial.print(".");
    }
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
  
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());  
    Serial.print("Open Telnet and connect to IP:");
    Serial.print(WiFi.localIP());
    Serial.print(" on port ");
    Serial.println(localUdpPort);
    
    //listening for packets
    Udp.begin(localUdpPort);
}

    

void loop() {
    
    int index = 0;
    //buffer for incoming messages
    char packetBuffer[256];
    delay(10);
    if (Udp.parsePacket()) {
      int len = Udp.read(packetBuffer, 255);
      if (len > 0) {
        packetBuffer[len] = 0;
        //print packetBuffer
        Serial.println(packetBuffer); 
        //showing where the packet came from
        Serial.print("Received packet from ");
        IPAddress remoteIp = Udp.remoteIP();
        Serial.print(remoteIp);
        Serial.print(", port ");
        Serial.println(Udp.remotePort());
        //sending stuff
        //sending JTAG stuff
        if(strcmp(packetBuffer, "your turn")==0){
           //resetting the previous receivedChars
           memset(receivedChars,0,strlen(receivedChars));
           //printing what was sent by client
           Serial.println(packetBuffer);
           //only send data once it has reached at least 4 characters.
           delay(1000);
           while(strlen(receivedChars)< 4){
              recvWithEndMarker();
             //showNewData();
           }
           Serial.print("FPGA UART: ");
           Serial.println(receivedChars);
           Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
           Udp.write(receivedChars);
           Udp.endPacket();
        }
      }
    }
    


//    Serial.println("Sent a hi");

  
    
        //Send Data to connected client
//        while(Serial.available()>0)
//        {
//          client.write(Serial.read());
//        }
//      }

    }







//Receiving functions from UART//

void recvWithEndMarker() {
    static byte ndx = 0;
    char endMarker = '\n';
    char rc;
    boolean newData = false;
    
    
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

//void showNewData() {
//    if (newData == true) {
//        Serial.print("FPGA UART: ");
//        Serial.println(receivedChars);
//        newData = false;
//    }
//}
