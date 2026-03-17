from machine import Pin, PWM
import time
import urandom

# Konstanter
PWM_FREQ = 1000
BASE_RED = 1.0
BASE_GREEN = 0.5
BASE_BLUE = 0.0
FLICKER_GREEN_MIN = 0.4
FLICKER_GREEN_MAX = 0.6
FLICKER_DELAY_MIN = 0.04
FLICKER_DELAY_MAX = 0.12

# Ange pinnummer för RGB LED och tryckknapp
red_pin = PWM(Pin(3))
green_pin = PWM(Pin(4))
blue_pin = PWM(Pin(5))
button_pin = Pin(6, Pin.IN, Pin.PULL_UP)  # Tryckknapp på GPIO 6, intern pull-up

# Initiera PWM
def init_pwm():
    red_pin.freq(PWM_FREQ)
    green_pin.freq(PWM_FREQ)
    blue_pin.freq(PWM_FREQ)
    red_pin.duty(0)
    green_pin.duty(0)
    blue_pin.duty(0)

# Sätt RGB-färger (anpassat för ESP32)
def set_rgb(red, green, blue):
    red_pin.duty(int(red * 1023))
    green_pin.duty(int(green * 1023))
    blue_pin.duty(int(blue * 1023))

# Mjuk fade-out när programmet avbryts
def fade_out():
    for i in range(100, -1, -1):
        factor = i / 100
        set_rgb(BASE_RED * factor, BASE_GREEN * factor, BASE_BLUE * factor)
        time.sleep(0.01)

# Flimra LED
def flicker():
    set_rgb(BASE_RED, BASE_GREEN, BASE_BLUE)
    time.sleep(urandom.uniform(FLICKER_DELAY_MIN, FLICKER_DELAY_MAX))
    flicker_green = urandom.uniform(FLICKER_GREEN_MIN, FLICKER_GREEN_MAX)
    set_rgb(BASE_RED, flicker_green, BASE_BLUE)
    time.sleep(urandom.uniform(FLICKER_DELAY_MIN, FLICKER_DELAY_MAX))

# Kör programmet
init_pwm()
try:
    while True:
        # Kontrollera om knappen trycks in (låg signal)
        if button_pin.value() == 0:
            print("Knapp tryckt – avbryter programmet...")
            fade_out()
            set_rgb(0, 0, 0)
            break
        flicker()
except KeyboardInterrupt:
    fade_out()
    set_rgb(0, 0, 0)
