import time
import requests
import json
import random
import serial
import sys

# ==========================================
#              ZONA DE CONFIGURARE
# ==========================================

# 1. Vrei sa folosesti senzorul real?
# Pune False acum (cat nu ai cablu). Pune True cand faci rost de cablu.
FOLOSESTE_SENZOR_REAL = True

# 2. Portul Arduino (Doar daca FOLOSESTE_SENZOR_REAL = True)
# Va trebui sa verifici in Device Manager cand ai cablul (ex: COM3, COM5)
PORT_SERIAL = "COM5" 
VITEZA_SERIALA = 9600

# 3. Link-ul tau Firebase (Nu uita /date.json la final)
# ATENȚIE: Trebuie să aibă /date.json la final!
FIREBASE_URL = "https://termostatrc-default-rtdb.europe-west1.firebasedatabase.app/date.json"
# ==========================================

print("🚀 PORNIRE SISTEM MONITORIZARE IoT")
if FOLOSESTE_SENZOR_REAL:
    print(f"🔌 MOD: CITIRE SENZOR REAL pe {PORT_SERIAL}")
else:
    print("💻 MOD: SIMULARE DATE (Fara cablu)")
print("------------------------------------------------")

# Functie pentru conectare la Arduino
def conectare_arduino():
    if not FOLOSESTE_SENZOR_REAL:
        return None
    try:
        ser = serial.Serial(PORT_SERIAL, VITEZA_SERIALA, timeout=1)
        time.sleep(2) # Asteptam sa se stabilizeze conexiunea
        print("✅ Conexiune Seriala Reusita!")
        return ser
    except Exception as e:
        print(f"❌ EROARE: Nu pot conecta Arduino pe {PORT_SERIAL}")
        print("   Verifica daca ai cablul bun si daca ai pus COM-ul corect.")
        sys.exit()

ser = conectare_arduino()

while True:
    try:
        temp_final = 0.0
        pres_final = 0
        status_curent = ""

        if FOLOSESTE_SENZOR_REAL:
            # --- VARIANTA 1: CITIRE REALA ---
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                # Asteptam formatul: "24.50,1002"
                if "," in line:
                    parts = line.split(",")
                    if len(parts) == 2:
                        temp_final = float(parts[0])
                        pres_final = int(parts[1])
                        status_curent = "Online (Senzor)"
                else:
                    # Daca primim gunoaie pe serial, ignoram tura asta
                    continue
            else:
                continue # Nu am primit date, mai asteptam
                
        else:
            # --- VARIANTA 2: SIMULARE (Ce ai acum) ---
            temp_final = round(random.uniform(23.0, 26.0), 2)
            pres_final = random.randint(980, 1005)
            status_curent = "Online (Simulat)"
            time.sleep(3) # Pauza doar la simulare

        # --- TRIMITEREA CATRE FIREBASE (Comuna) ---
        # Trimitem doar daca avem valori valide (nu 0)
        if temp_final != 0:
            data_to_send = {
                "temperatura": temp_final,
                "presiune": pres_final,
                "status": status_curent,
                "timestamp": time.time()
            }

            response = requests.patch(FIREBASE_URL, json=data_to_send)

            if response.status_code == 200:
                print(f"📤 Trimis: Temp={temp_final} C | Pres={pres_final} hPa | Mod: {status_curent}")
            else:
                print(f"⚠️ Eroare Firebase: {response.status_code}")

    except ValueError:
        print("⚠️ Date corupte de la senzor, ignor...")
    except KeyboardInterrupt:
        print("\nOprit de utilizator.")
        break
    except Exception as e:
        print(f"❌ Eroare: {e}")
        if FOLOSESTE_SENZOR_REAL:
            time.sleep(1)