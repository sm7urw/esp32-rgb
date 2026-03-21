import time
import random
import _thread
from machine import Pin, PWM, reset

# Sänk CPU-frekvensen för att spara batteri
machine.freq(80000000)  # 40 MHz istället för 160 MHz

print("CPU-frekvens: 40 MHz (spara batteri)\n")

print("=== Levande Ljus ===\n")

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

print("LED initierad - Njut av det levande ljuset!")
print("Knapp (GPIO 20):")
print("  - Kort tryck = Av/på ljuset")
print("  - Långt tryck (2+ sekunder) = Omstart ESP32\n")

def set_color(red, green, blue):
    """Sätt LED-färg (0-255 för varje färg)"""
    # Konvertera från 0-255 till 0-1023 och INVERTERA
    red_pwm.duty(1023 - int(red * 4.008))
    green_pwm.duty(1023 - int(green * 4.008))
    blue_pwm.duty(1023 - int(blue * 4.008))

def set_warm_color(brightness):
    """Sätt varm färg (röd + gul) med given ljusstyrka"""
    red = brightness
    green = int(brightness * 0.6)  # Lite gul blandning
    blue = 0
    
    # Lägg till lite flakering för levande effekt
    flicker = random.randint(-20, 25)
    
    red = max(0, min(255, red + flicker))
    green = max(0, min(255, int(green + flicker * 0.5)))
    
    set_color(red, green, blue)

def check_button():
    """Övervaka knappen i en separat tråd"""
    global light_on
    print("✓ Knappövervakning startad\n")
    
    while True:
        if button.value() == 0:  # Knappen tryckt in (LOW)
            press_start = time.time()
            
            # Vänta tills knappen släpps
            while button.value() == 0:
                time.sleep(0.05)
            
            press_duration = time.time() - press_start
            
            # Långt tryck (> 2 sekunder) = Omstart
            if press_duration > 2.0:
                print("\n LÅNGT TRYCK - Startar om ESP32...\n")
                time.sleep(1)
                reset()
            
            # Kort tryck (< 2 sekunder) = Av/på
            elif press_duration > 0.3:  # Debounce
                light_on = not light_on
                status = "PÅ ✨" if light_on else "AV 🌑"
                print(f"\n💡 Ljus är nu: {status}\n")
        
        time.sleep(0.05)

# Starta knappövervakning i en separat tråd
_thread.start_new_thread(check_button, ())

# HUVUDLOOP - Levande ljus-effekt
try:
    while True:
        if light_on:
            # Slumpmässiga min/max värden för varje cykel (mer variation)
            cycle_min = random.randint(20, 50)
            cycle_max = random.randint(150, 200) # Ändra ljusstyrkan
            
            # Långsam pulsande andnings-effekt med jämn kurva
            # Öka ljusstyrka (mindre steg = jämnare kurva)
            for brightness in range(cycle_min, cycle_max, 1):
                if not light_on:  # Kolla om knappen trycktes
                    break
                # Mycket flakering - gör ljuset "levande"
                flicker = random.randint(-20, 25)
                actual_brightness = max(0, min(255, brightness + flicker))
                
                set_warm_color(actual_brightness)
                time.sleep(0.01)  # Snabbare uppdateringar
            
            # Pausa lite på toppen (slumpmässig längd)
            time.sleep(random.uniform(0.1, 0.5))
            
            # Minska ljusstyrka (med samma flakering för konsistens)
            for brightness in range(cycle_max, cycle_min - 1, -1):
                if not light_on:  # Kolla om knappen trycktes
                    break
                flicker = random.randint(-20, 25)
                actual_brightness = max(0, min(255, brightness + flicker))
                
                set_warm_color(actual_brightness)
                time.sleep(0.01)
            
            # Slumpmässig pauslängd mellan pulser (gör det "levande")
            pause = random.uniform(0.3, 2.0)
            time.sleep(pause)
        else:
            # Ljuset är av - släck LED:n
            set_color(0, 0, 0)
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\nLevande ljus avslutat")
    set_color(0, 0, 0)  # Släck LED:n
