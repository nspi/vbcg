// Needed variables
String  inputString = "";            // Incoming data
String  command = "";                // Potential command
boolean stringComplete = 0;          // Is string complete?
int     outputPin = 2;               // Number of used i/o pin

// Initialization
void setup() 
{  
  // Initialize serial port
  Serial.begin(9600, SERIAL_8N1); 
  // Send message 
  Serial.println("Device ready");
  // Reserve space for variables
  inputString.reserve(100);  command.reserve(100);
  // Initialize digital output
  pinMode(outputPin, OUTPUT);
}

// The main loop
void loop() 
{
  // Check if arrived command is valid  
  if (stringComplete) 
  {
    command = inputString;
    
    //Valid command "ON": Set output pin high
    if(command == "T") 
    {
      // Apply voltage over i/o port
      digitalWrite(outputPin, HIGH);
      // Wait for 15ms
      delay(15);
      // Disable i/o port
      digitalWrite(outputPin, LOW);
      // Send message
      Serial.println("Trigger sent");  
    }
    else 
    {
      Serial.println("Unknown command. Possible command: T");
    }
 
    // Reset everything
    inputString = "";
    command = "";
    stringComplete = false;
  }
}



/* SerialEvent function.  modified from public domain source code
 from arduino examples: http://www.arduino.cc/en/Tutorial/SerialEvent*/
void serialEvent() {
  while (Serial.available()) {
    // get data
    char inChar = (char)Serial.read(); 

    if (!((inChar == '\n') || (inChar == '\r'))) 
    {
    inputString += inChar; 
    } 
    else 
    {
    stringComplete = true;
    }
  }
}


