#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

int offset = 100; // low pressure calibration
int span = 929;   // high pressure calibration
float Vin = 4.85;   // 4.8 volts - USB powered
float R1 = 2000;   // Temperature resistor value

float A = 1.234166184e-03, B = 2.712699866e-04, C = 0.9289862476e-07; // Steinhart-Hart and Hart Coefficients

void setup() {
  Serial.begin(9600); // Pornim comunicarea cu Laptopul

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    for (;;);
  }
}

void loop() {
  // --- CALCUL PRESIUNE ---
  float pressure = map(analogRead(A0), offset, span, 500, 4000);
  int pressureInt = int(pressure); // Convertim la numar intreg

  // --- CALCUL TEMPERATURA ---
  int temperatureVoltage = analogRead(A1);
  float temperatureBuffer = temperatureVoltage * Vin;
  float Vout = (temperatureBuffer) / 1024.0;
  temperatureBuffer = (Vin / Vout) - 1;
  float R2 = R1 / temperatureBuffer;

  float logR2 = log(R2);
  float temperature = (1.0 / (A + B * logR2 + C * logR2 * logR2 * logR2));
  temperature -= 273.15; // Convert to Celsius
  temperature= temperature-5;

  // 1. AFISARE PE ECRAN 
  display.clearDisplay();
  display.setTextSize(2); 
  display.setTextColor(SSD1306_WHITE);

  display.setCursor(0, 0);
  display.print(F("P:"));
  display.print(pressureInt);
  display.print(F(" hPa"));

  display.setCursor(0, 30);
  display.print(F("T:"));
  display.print(temperature);
  display.print(F("C"));

  display.display();

  //2. TRIMITERE CATRE PYTHON (Format: "24.50,1002") ---
  Serial.print(temperature); 
  Serial.print(","); 
  Serial.println(pressureInt); 

  delay(2000); // Asteapta 2 secunde
}