import time
import random
import machine
from machine import Pin, PWM, reset

# 20 MHz - Väldigt lågt batteri-bruk
machine.freq(20000000)

print("=== Levande Ljus ===\n")

# GPIO-pinnar
RED_PIN = 3
GREEN_PIN = 4
BLUE_PIN = 5
BUTTON_PIN = 20

# Konfigurera PWM
red_pwm = PWM(Pin(RED_PIN), freq=1000)
green_pwm = PWM(Pin(GREEN_PIN), freq=1000)
blue_pwm = PWM(Pin(BLUE_PIN), freq=1000)

# Knapp
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

print("LED initierad - Njut av det levande ljuset!")
print("Tryck knappen (GPIO 20) för att starta om ESP32\n")

# Debounce och feedback
last_button_press = 0
BUTTON_DEBOUNCE = 0.5  # 500ms debounce


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


def blink_countdown(seconds=3):
    """Blinka blått med nedräkning innan omstart"""

    # Vänta tills knappen släpps innan vi börjar kolla efter avbrott
    while button.value() == 0:
        time.sleep(0.05)
    time.sleep(0.1)  # Lite extra debounce

    print(f"Omstart om {seconds} sekunder... (Tryck knappen igen för att avbryta)")

    for i in range(seconds, 0, -1):
        # Två blinkar per sekund
        for _ in range(2):
            set_color(0, 0, 255)  # Blå på
            time.sleep(0.2)

            # Kontrollera om användaren trycker knappen igen för att avbryta
            if button.value() == 0:
                print("\nOmstart avbruten!")
                set_color(0, 0, 0)
                return False

            set_color(0, 0, 0)    # Blå av
            time.sleep(0.2)

            # Kontrollera igen
            if button.value() == 0:
                print("\nOmstart avbruten!")
                set_color(0, 0, 0)
                return False

        print(f"{i - 1}...")

    return True  # Omstart bekräftad


# HUVUDLOOP
try:
    while True:
        # Slumpmässiga min/max värden för varje cykel (mer variation)
        cycle_min = random.randint(30, 70)
        cycle_max = random.randint(200, 255)
        
        # Långsam pulsande andnings-effekt med jämn kurva
        # Öka ljusstyrka (mindre steg = jämnare kurva)
        for brightness in range(cycle_min, cycle_max, 1):
            # Mycket flakering - gör ljuset "levande"
            flicker = random.randint(-20, 25)
            actual_brightness = max(0, min(255, brightness + flicker))
            
            set_warm_color(actual_brightness)
            time.sleep(0.01)  # Snabbare uppdateringar
        
        # Pausa lite på toppen (slumpmässig längd)
        time.sleep(random.uniform(0.1, 0.5))
        
        # Minska ljusstyrka (med samma flakering för konsistens)
        for brightness in range(cycle_max, cycle_min - 1, -1):
            flicker = random.randint(-20, 25)
            actual_brightness = max(0, min(255, brightness + flicker))
            
            set_warm_color(actual_brightness)
            time.sleep(0.01)
        
        # Slumpmässig pauslängd mellan pulser (gör det "levande")
        pause = random.uniform(0.3, 2.0)
        time.sleep(pause)

except KeyboardInterrupt:
    print("\nLevande ljus avslutat")
    set_color(0, 0, 0)