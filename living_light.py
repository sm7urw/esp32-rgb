import time
import random
from machine import Pin, PWM, reset

print("=== Levande Ljus ===\n")

# GPIO-pinnar
RED_PIN = 3
GREEN_PIN = 4
BLUE_PIN = 5
BUTTON_PIN = 6

# Konfigurera PWM
red_pwm = PWM(Pin(RED_PIN), freq=1000)
green_pwm = PWM(Pin(GREEN_PIN), freq=1000)
blue_pwm = PWM(Pin(BLUE_PIN), freq=1000)

# Knapp
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

print("LED initierad - Njut av det levande ljuset!")
print("Tryck knappen (GPIO 6) för att starta om ESP32\n")

def set_color(red, green, blue):
    red_pwm.duty(1023 - int(red * 4.008))
    green_pwm.duty(1023 - int(green * 4.008))
    blue_pwm.duty(1023 - int(blue * 4.008))

def set_warm_color(brightness):
    red = brightness
    green = int(brightness * 0.6)
    blue = 0

    flicker = random.randint(-10, 10)
    red = max(0, min(255, red + flicker))
    green = max(0, min(255, int(green + flicker * 0.5)))

    set_color(red, green, blue)

# HUVUDLOOP
try:
    while True:
        # Kontrollera knappen
        if button.value() == 0:
            print("\n🔄 KNAPP TRYCKT - Startar om ESP32...\n")
            time.sleep(1)
            reset()

        # Levande ljus-effekt
        for brightness in range(50, 256, 3):
            set_warm_color(brightness)
            time.sleep(0.03)

        for brightness in range(255, 49, -3):
            set_warm_color(brightness)
            time.sleep(0.03)

        time.sleep(random.uniform(0.5, 1.5))

except KeyboardInterrupt:
    print("\nLevande ljus avslutat")
    set_color(0, 0, 0)
