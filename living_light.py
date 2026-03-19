import time
import random
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
                return False  # Avbruten
            
            set_color(0, 0, 0)    # Blå av
            time.sleep(0.2)
            
            # Kontrollera igen
            if button.value() == 0:
                print("\nOmstart avbruten!")
                set_color(0, 0, 0)
                return False  # Avbruten
        
        print(f"{i - 1}...")
    
    return True  # Omstart bekräftad

# HUVUDLOOP
try:
    while True:
        # Kontrollera knappen med debounce
        if button.value() == 0:
            current_time = time.time()
            
            if current_time - last_button_press > BUTTON_DEBOUNCE:
                print("\n✓ KNAPP TRYCKT - Omstart initierad\n")
                
                # Blinkande nedräkning
                should_reset = blink_countdown(seconds=3)
                
                if should_reset:
                    print("\nStartar om ESP32...\n")
                    time.sleep(1)
                    reset()
                
                last_button_press = current_time
                time.sleep(0.5)  # Lite extra debounce efter feedback

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