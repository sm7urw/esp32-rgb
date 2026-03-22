import time
import random
import _thread
import machine
from machine import Pin, PWM, reset

# Sänk CPU-frekvensen för att spara batteri

machine.freq(40000000)  # 40 MHz istället för 160 MHz

print(“CPU-frekvens: 40 MHz (spara batteri)”)

print(”=== Levande Ljus ===\n”)

# GPIO-pinnar

RED_PIN = 3
GREEN_PIN = 4
BLUE_PIN = 5

# Konfigurera PWM

red_pwm = PWM(Pin(RED_PIN), freq=1000)
green_pwm = PWM(Pin(GREEN_PIN), freq=1000)
blue_pwm = PWM(Pin(BLUE_PIN), freq=1000)

# Knapp

button_pin = 20  # GPIO 20
button = Pin(button_pin, Pin.IN, Pin.PULL_UP)

# Global flagga för ljus-status

light_on = True

print(“LED initierad - Njut av det levande ljuset!”)
print(“Knapp (GPIO 20):”)
print(”  - Kort tryck = Av/på ljuset”)
print(”  - Långt tryck (2+ sekunder) = Omstart ESP32\n”)

def set_color(red, green, blue):
“”“Sätt LED-färg (0-255 för varje färg)”””
# Konvertera från 0-255 till 0-1023 och INVERTERA
red_pwm.duty(1023 - int(red * 4.008))
green_pwm.duty(1023 - int(green * 4.008))
blue_pwm.duty(1023 - int(blue * 4.008))

def set_warm_color(brightness):
“”“Sätt varm färg (röd + gul) med given ljusstyrka”””
red = brightness
green = int(brightness * 0.6)  # Lite gul blandning
blue = 0

```
# Lägg till lite flakering för levande effekt
flicker = random.randint(-20, 25)

red = max(0, min(255, red + flicker))
green = max(0, min(255, int(green + flicker * 0.5)))

set_color(red, green, blue)
```

def check_button():
“”“Övervaka knappen i en separat tråd”””
global light_on
print(“✓ Knappövervakning startad - Väntar på knapptryck…\n”)

```
while True:
    button_state = button.value()
    
    if button_state == 0:  # Knappen tryckt in (LOW)
        print("KNAPP TRYCKT - Börjar mäta tid...")
        press_start = time.time()
        
        # Vänta tills knappen släpps
        while button.value() == 0:
            time.sleep(0.05)
        
        press_duration = time.time() - press_start
        print(f"Knapp släppt efter {press_duration:.2f} sekunder\n")
        
        # Långt tryck (> 2 sekunder) = Omstart
        if press_duration > 2.0:
            print("🔄 LÅNGT TRYCK DETEKTERAT - Startar om!\n")
            time.sleep(1)
            reset()
        
        # Kort tryck (> 0.3 sekunder) = Av/på
        elif press_duration > 0.3:
            light_on = not light_on
            status = "PÅ ✨" if light_on else "AV 🌑"
            print(f"💡 KORT TRYCK - Ljus är nu: {status}\n")
        else:
            print("(För kort tryck, ignorera)\n")
    
    time.sleep(0.05)
```

# Starta knappövervakning i en separat tråd

try:
_thread.start_new_thread(check_button, ())
except Exception as e:
print(f”ERROR när knappövervakning startades: {e}”)

# HUVUDLOOP - Levande ljus-effekt

try:
while True:

```
    if light_on:
        # KAOTISK FLADDRING - mycket mer naturlig än upp-ned mönster!
        # Istället för att gå från A till B, hoppar vi slumpmässigt omkring
        
        current_brightness = random.randint(20, 60)
        
        # Slumpmässiga fladdrar - ibland upp, ibland ner, ibland ingenting
        for _ in range(random.randint(80, 250)):
            if not light_on:
                break
            
            # Slumpmässig riktning och stegstorlek
            # Mer sannolikhet för små steg = naturligare rörelse
            direction = random.choice([-2, -1, -1, 0, 0, 1, 1, 2])
            
            # Uppdatera ljusstyrka
            current_brightness += direction
            current_brightness = max(15, min(180, current_brightness))
            
            # EXTRA flakering för super-naturlig effekt
            flicker = random.randint(-30, 35)
            actual_brightness = max(0, min(255, current_brightness + flicker))
            
            set_warm_color(actual_brightness)
            
            # Slumpmässig tid mellan uppdateringar (gör det ojämnt!)
            time.sleep(random.uniform(0.003, 0.025))
            
            # Slumpmässiga pauser mitt i fladdringen
            if random.random() < 0.08:  # 8% chans
                time.sleep(random.uniform(0.05, 0.2))
        
        # Slumpmässig pauslängd mellan pulser
        time.sleep(random.uniform(0.1, 1.2))
    else:
        # Ljuset är av - släck LED:n
        set_color(0, 0, 0)
        time.sleep(0.1)
```

except KeyboardInterrupt:
print(”\nLevande ljus avslutat”)
set_color(0, 0, 0)  # Släck LED:n
