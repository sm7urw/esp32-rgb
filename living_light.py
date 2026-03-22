import time
import random
import _thread
import machine
from machine import Pin, PWM, reset

# Sänk CPU-frekvensen för att spara batteri
machine.freq(40000000)  # 40 MHz

print("=== Levande Ljus ===\n")
print("CPU-frekvens: 40 MHz\n")

# GPIO-pinnar
RED_PIN = 3
GREEN_PIN = 4
BLUE_PIN = 5

# Konfigurera PWM
red_pwm = PWM(Pin(RED_PIN), freq=1000)
green_pwm = PWM(Pin(GREEN_PIN), freq=1000)
blue_pwm = PWM(Pin(BLUE_PIN), freq=1000)

# Knapp
button = Pin(20, Pin.IN, Pin.PULL_UP)

# Global flagga för ljus-status
light_on = True

print("LED initierad - Njut av det levande ljuset!")
print("Knapp (GPIO 20):")
print("  - Kort tryck = Av/på ljuset")
print("  - Långt tryck (2+ sekunder) = Omstart ESP32\n")

def set_color(red, green, blue):
    """Sätt LED-färg (0-255 för varje färg)"""
    red_pwm.duty(1023 - int(red * 4.008))
    green_pwm.duty(1023 - int(green * 4.008))
    blue_pwm.duty(1023 - int(blue * 4.008))

def set_warm_color(brightness):
    """Sätt varm färg (röd + gul) med given ljusstyrka"""
    red = brightness
    green = int(brightness * 0.6)
    blue = 0
    
    # Lägg till flakering
    flicker = random.randint(-30, 35)
    
    red = max(0, min(255, red + flicker))
    green = max(0, min(255, int(green + flicker * 0.5)))
    
    set_color(red, green, blue)

def check_button():
    """Övervaka knappen"""
    global light_on
    print("✓ Knappövervakning startad\n")
    
    while True:
        if button.value() == 0:  # Knappen tryckt
            press_start = time.time()
            
            # Vänta tills knappen släpps
            while button.value() == 0:
                time.sleep(0.05)
            
            press_duration = time.time() - press_start
            
            # Långt tryck = Omstart
            if press_duration > 2.0:
                print("\n🔄 Omstartar...\n")
                time.sleep(1)
                reset()
            
            # Kort tryck = Av/på
            elif press_duration > 0.3:
                light_on = not light_on
                status = "PÅ ✨" if light_on else "AV 🌑"
                print(f"\n💡 Ljus: {status}\n")
        
        time.sleep(0.05)

# Starta knappövervakning
_thread.start_new_thread(check_button, ())

# HUVUDLOOP - Kaotisk levande ljus-effekt
try:
    while True:
        if light_on:
            # Slumpmässig fladdring - kaotisk och naturlig
            current_brightness = random.randint(20, 60)
            
            # Slumpmässiga fladdrar - LÅNGSAMMARE men tydlig
            for _ in range(random.randint(120, 300)):
                if not light_on:
                    break
                
                # Mindre steg = lugnare rörelse
                direction = random.choice([-1, -1, 0, 0, 0, 1, 1])
                current_brightness += direction
                current_brightness = max(15, min(180, current_brightness))
                
                # Flakering för levande effekt
                flicker = random.randint(-25, 30)
                actual_brightness = max(0, min(255, current_brightness + flicker))
                
                set_warm_color(actual_brightness)
                
                # LÅNGSAM uppdatering - detta är nyckeln!
                time.sleep(random.uniform(0.02, 0.06))
                
                # Slumpmässiga pauser (långsammare)
                if random.random() < 0.05:
                    time.sleep(random.uniform(0.1, 0.4))
            
            # Paus mellan pulser
            time.sleep(random.uniform(0.1, 1.2))
        else:
            # Ljuset är av
            set_color(0, 0, 0)
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\nAvslutat")
    set_color(0, 0, 0)
