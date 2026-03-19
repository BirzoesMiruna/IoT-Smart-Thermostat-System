# IoT Smart Thermostat System

## 1. Overview
This project consists of an integrated IoT ecosystem designed for real-time monitoring of ambient temperature and atmospheric pressure. The system features a multi-level architecture that connects a hardware sensory node to a mobile application via a cloud-based infrastructure.

## 2. System Architecture
The platform is organized into four hierarchical layers to ensure a seamless data flow:
* **Physical Level (Sensorial):** Data acquisition using an Arduino Uno and analog sensors.
* **Gateway Level (Processing):** A Python-based middleware that handles serial communication and data transmission to the cloud.
* **Cloud Level (Storage):** Real-time data persistence and synchronization using Google Firebase.
* **Application Level (Visualization):** A cross-platform mobile application for remote monitoring.



## 3. Technical Specifications
* **Control Unit:** Arduino Uno (ATmega328P) operating at 16MHz.
* **Sensors:**
    * **Temperature:** NTC 10kOhm Thermistor using the Steinhart-Hart equation for high-precision conversion.
    * **Pressure:** Analog sensor mapped to hPa.
* **Local Interface:** 0.96 inch OLED display (128x64 resolution) via I2C interface.
* **Connectivity:**
    * Hardware-to-PC: Serial UART (USB) at 9600 bps.
    * PC-to-Cloud: HTTP/REST protocol using JSON data format.
* **Cloud Platform:** Google Firebase Realtime Database (NoSQL).
* **Mobile Client:** Developed with React Native and Expo.

## 4. Key Features
* **High Precision Monitoring:** Implementation of the Steinhart-Hart model ensures accurate temperature readings by linearizing the NTC thermistor response.
* **Hybrid Gateway Mode:** The Python script can operate in both real-sensor mode (USB reading) and simulation mode for testing purposes.
* **Real-time Synchronization:** Data is sampled and transmitted every 2-3 seconds, providing near-instant updates to the mobile dashboard.
* **HMI Functionality:** Local OLED display ensures system functionality even in offline mode.

## 5. Software Structure
* **Firmware:** Written in C++ for Arduino, handling ADC readings, mathematical calculations, and data serialization.
* **Gateway:** Python script utilizing the PySerial library for local data acquisition and the Requests library for Cloud interfacing.
* **Mobile App:** Built with React Native, utilizing React Hooks (useState, useEffect) for real-time data polling.

## 6. How to Run
1. **Hardware:** Connect the Arduino Uno to the PC via USB. Ensure the sensors and OLED are wired correctly.
2. **Firmware:** Upload the `.ino` sketch to the Arduino.
3. **Gateway:** Run the Python script on a PC to start data synchronization with Firebase.
4. **Mobile:** Use the Expo Go app to run the React Native application and monitor the data remotely.
