import threading
import time
import requests
import warnings
import sys
from datetime import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageFont, ImageDraw

warnings.filterwarnings("ignore", category=DeprecationWarning)

# --- Configuration ---
YOUR_DEVICE_ID = "<CHANGE TO YOUR DEVICE ID>"
YOUR_TEMPEST_API_KEY = "<CHANGE TO YOUR API KEY>"

FONT_PATH = "fonts/04B_24__.TTF" #This font is required - this is the only one that will display correctly
DATE_FONT_SIZE = 8
TIME_FONT_SIZE = 24
TEMP_HUM_FONT_SIZE = 8

# Dallas Stars Colors
DALLAS_GREEN = (0, 97, 65) #This is in RGB format... it might need to be RBG dependin on your Matrix HAT
WHITE = (255, 255, 255)
DIM_BRIGHTNESS = 40
FULL_BRIGHTNESS = 60

print("Initializing Matrix...")
try:
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat-pwm'
    options.drop_privileges = False  # DO NOT DROP ROOT

    # Optional: If using a newer Pi, you might need this:
    # options.gpio_slowdown = 2

    matrix = RGBMatrix(options=options)
    print("Matrix initialized successfully.")
except Exception as e:
    print(f"CRITICAL ERROR: Matrix failed to initialize: {e}")
    sys.exit(1)

cached_temp, cached_hum = "--", "--"

def get_weather():
    global cached_temp, cached_hum
    url = f"https://swd.weatherflow.com/swd/rest/observations/device/{YOUR_DEVICE_ID}?token={YOUR_TEMPEST_API_KEY}"
    print(f"Updating weather from Tempest...")
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if "obs" in data and len(data["obs"]) > 0:
            obs = data["obs"][0]
            cached_temp = f"{(obs[7] * 9/5) + 32:.1f}"
            cached_hum = obs[8]
            print(f"Weather Updated: {cached_temp}F")
    except Exception as e:
        print(f"Weather API Error: {e}")

def display_loop():
    print("Starting display loop...")
    try:
        font_date = ImageFont.truetype(FONT_PATH, DATE_FONT_SIZE)
        font_time = ImageFont.truetype(FONT_PATH, TIME_FONT_SIZE)
        font_weather = ImageFont.truetype(FONT_PATH, TEMP_HUM_FONT_SIZE)
    except:
        print("Font not found, using default.")
        font_date = font_time = font_weather = ImageFont.load_default()

    while True:
        now = datetime.now()
        matrix.brightness = DIM_BRIGHTNESS if (21 <= now.hour or now.hour < 9) else FULL_BRIGHTNESS

        image = Image.new("RGB", (64, 32), color=(0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Helper to center
        def center(text, font):
            bb = draw.textbbox((0, 0), text, font=font)
            return (64 - (bb[2] - bb[0])) // 2

        weather_txt = f"{cached_temp}F {cached_hum}%"

        draw.text((center(now.strftime("%b %d %Y"), font_date), 0), now.strftime("%b %d %Y"), fill=WHITE, font=font_date)
        draw.text((center(now.strftime("%H:%M"), font_time), 4), now.strftime("%H:%M"), fill=DALLAS_GREEN, font=font_time)
        draw.text((center(weather_txt, font_weather), 24), weather_txt, fill=WHITE, font=font_weather)

        matrix.SetImage(image.rotate(180))
        time.sleep(5)

if __name__ == "__main__":
    # Initial weather pull
    get_weather()

    # Background thread
    t = threading.Thread(target=lambda: [time.sleep(600) or get_weather() for _ in iter(int, 1)], daemon=True)
    t.start()

    try:
        display_loop()
    except KeyboardInterrupt:
        matrix.Clear()
