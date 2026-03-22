import time
import random
import _thread
import machine
from machine import Pin, PWM, reset

# Sänk CPU-frekvensen för att spara batteri
machine.freq(80000000)

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
button = Pin(20, Pin.IN, Pin.PULL_UP)

# Global flagga för ljus-status
light_on = True

print("LED initierad")
print("Knapp (GPIO 20): Kort=Av/på, Långt=Omstart\n")

def set_color(red, green, blue):
    """Sätt LED-färg"""
    red_pwm.duty(1023 - int(red * 4.008))
    green_pwm.duty(1023 - int(green * 4.008))
    blue_pwm.duty(1023 - int(blue * 4.008))

def set_warm_color(brightness):
    """Sätt varm färg med flakering"""
    red = brightness
    green = int(brightness * 0.4)
    blue = 0
    
    flicker = random.randint(-20, 25)
    red = max(0, min(255, red + flicker))
    green = max(0, min(255, int(green + flicker * 0.5)))
    
    set_color(red, green, blue)

def check_button():
    """Övervaka knappen"""
    global light_on
    
    while True:
        if button.value() == 0:
            press_start = time.time()

            while button.value() == 0:
                time.sleep(0.05)
            
            press_duration = time.time() - press_start

            if press_duration > 2.0:
                print("🔄 Omstartar...\n")
                time.sleep(1)
                reset()
            elif press_duration > 0.3:
                light_on = not light_on
                status = "PÅ ✨" if light_on else "AV 🌑"
                print(f"💡 {status}\n")
        
        time.sleep(0.05)

# Starta knappövervakning
_thread.start_new_thread(check_button, ())

# HUVUDLOOP - Lugn levande ljus-effekt
print("Ljuset startar...\n")

try:
    pulse_counter = 0
    while True:
        if light_on:
            pulse_counter += 1

            # Lugn, långsam pulsation
            brightness = 50
            direction = 1

            # Långsam ökning
            while brightness < 150 and light_on:
                set_warm_color(brightness)
                brightness += 1
                time.sleep(0.04)
            
            # Långsam minskning
            while brightness > 50 and light_on:
                set_warm_color(brightness)
                brightness -= 1
                time.sleep(0.04)
            
            # Kort paus
            time.sleep(random.uniform(0.2, 0.8))
        else:
            # Ljuset är av
            set_color(0, 0, 0)
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\nAvslutat")
    set_color(0, 0, 0)
