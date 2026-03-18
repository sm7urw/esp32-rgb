import time
import random
from machine import Pin, PWM

print("=== Levande Ljus ===\n")

# GPIO-pinnar (uppdaterad efter omödsodling)
RED_PIN = 3
GREEN_PIN = 4
BLUE_PIN = 5

# Konfigurera PWM
red_pwm = PWM(Pin(RED_PIN), freq=1000)
green_pwm = PWM(Pin(GREEN_PIN), freq=1000)
blue_pwm = PWM(Pin(BLUE_PIN), freq=1000)

print("LED initierad - Njut av det levande ljuset!\n")

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
    flicker = random.randint(-10, 10)
    
    red = max(0, min(255, red + flicker))
    green = max(0, min(255, int(green + flicker * 0.5)))
    
    set_color(red, green, blue)

# HUVUDLOOP - Levande ljus-effekt
try:
    while True:
        # Långsam pulsande andnings-effekt
        # Öka ljusstyrka
        for brightness in range(50, 256, 3):
            set_warm_color(brightness)
            time.sleep(0.03)
        
        # Minska ljusstyrka
        for brightness in range(255, 49, -3):
            set_warm_color(brightness)
            time.sleep(0.03)
        
        # Varierande pauslängd för naturlig känsla
        time.sleep(random.uniform(0.5, 1.5))

except KeyboardInterrupt:
    print("\nLevande ljus avslutat")
    set_color(0, 0, 0)  # Släck LED:n

