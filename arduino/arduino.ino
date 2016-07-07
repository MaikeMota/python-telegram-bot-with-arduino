#include <dht11.h>


dht11 sensor;

#define LED_PIN 13

#define ACTIVATE_LED "1"
#define DEACTIVATE_LED "0"
#define TEMP "temp"
void readSensor(){
  int chk = sensor.read(2); // sensor faz a leitura no pino 2
       // Testa se a leitura foi bem sucedida  
       switch(chk) {
             case DHTLIB_OK:
                   // Se a leitura foi bem sucedida, mostra a umidade e temperatura na Serial
                   Serial.print((float)sensor.temperature, 0);
                   Serial.print(";");
                   Serial.println((float)sensor.humidity, 0);
      } 
}

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {

  if(Serial.available()){
    String s = Serial.readString();

    if(s == ACTIVATE_LED){
      digitalWrite(LED_PIN, HIGH);
      Serial.println("LED ligado com sucesso");
    }
    else if(s == DEACTIVATE_LED){
      digitalWrite(LED_PIN, LOW);
      Serial.println("LED desligado com sucesso");
    }else if(s == TEMP){
      readSensor();
    }
  }
  
}
