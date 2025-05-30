import threading
import time
import requests
from datetime import datetime
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageFont, ImageDraw
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Configuration for the RGB matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'  # Change to your specific hardware mapping

matrix = RGBMatrix(options=options)

# Colors
DALLAS_GREEN = (0, 97, 65)
WHITE = (255, 255, 255)

# Font settings
FONT_PATH = "/home/pi/nhl-led-scoreboard/assets/fonts/04B_24__.TTF"
#FONT_PATH2= "/home/pi/nhl-led-scoreboard/assets/fonts/score_large.otf"
DATE_FONT_SIZE = 8
TIME_FONT_SIZE = 24
TEMP_HUM_FONT_SIZE = 8

# Brightness levels
DIM_BRIGHTNESS = 40  # Adjust as needed
FULL_BRIGHTNESS = 60

# Function to rotate image
def rotate_image(image):
    return image.rotate(180)

# Function to get temperature and humidity from Weather Underground
def get_temp_and_humidity():
    global cached_temperature, cached_humidity
    url = f"https://swd.weatherflow.com/swd/rest/observations/device/" \
          f"{YOUR_DEVICE_ID}?token={YOUR_TEMPEST_API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Debug response to check structure
    print(data)

    try:
        if "obs" in data and len(data["obs"]) > 0:
            observation = data["obs"][0]
            temperature = (observation[7] * 9/5) + 32  # Correct index for temperature
            humidity = observation[8]  # Correct index for humidity
            cached_temperature = f"{temperature:.1f}"  # Store in cache
            cached_humidity = humidity
        else:
            raise KeyError("Missing 'obs' data in API response")
    except (KeyError, IndexError) as e:
        print(f"Error parsing weather data: {e}")
        cached_temperature, cached_humidity = "--", "--"

    return cached_temperature, cached_humidity

# Function to display the date, time, temperature, and humidity.
def display_date_time():
    global cached_temperature, cached_humidity
    while True:
        current_time = datetime.now()

        # Adjust brightness based on time
        matrix.brightness = DIM_BRIGHTNESS if 21 <= current_time.hour or current_time.hour < 9 else FULL_BRIGHTNESS

        # Extracting date and time components
        date_string = current_time.strftime("%b %d %Y")
        time_string = current_time.strftime("%H:%M")

        # Use cached values for temperature and humidity
        temperature, humidity = cached_temperature, cached_humidity

        # Create a blank image
        image = Image.new("RGB", (options.cols, options.rows), color=(0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Load fonts
        font_date = ImageFont.truetype(FONT_PATH, DATE_FONT_SIZE)
        font_time = ImageFont.truetype(FONT_PATH, TIME_FONT_SIZE)
        font_temp_hum = ImageFont.truetype(FONT_PATH, TEMP_HUM_FONT_SIZE)

        # Calculate text positions for centering
        date_width, date_height = draw.textsize(date_string, font=font_date)
        date_position = ((options.cols - date_width) // 3, 1)

        time_width, time_height = draw.textsize(time_string, font=font_time)
        time_position = ((options.cols - time_width) // 2, 5)

        temp_hum_text = f"{temperature}F  {humidity}%"
        temp_hum_width, temp_hum_height = draw.textsize(temp_hum_text, font=font_temp_hum)
        temp_hum_position = ((options.cols - temp_hum_width) // 2, 24)

        # Display date in white
        draw.text(date_position, date_string, fill=WHITE, font=font_date)

        # Display time in Dallas Stars green
        draw.text(time_position, time_string, fill=DALLAS_GREEN, font=font_time)

        # Display temperature and humidity below time
        draw.text(temp_hum_position, temp_hum_text, fill=WHITE, font=font_temp_hum)

        # Rotate the image
        rotated_image = rotate_image(image)

        # Display the image on the RGB matrix
        matrix.SetImage(rotated_image)

        time.sleep(5)  # Update every 5 seconds

def weather_thread():
    while True:
        try:
            # Update the cached temperature and humidity every 10 minutes
            get_temp_and_humidity()
        except Exception as e:
            print(f"Weather update failed: {e}")
        time.sleep(600)  # Update every 10 minutes

cached_temperature, cached_humidity = "--", "--"

if __name__ == "__main__":
    try:
        # Start the weather thread
        weather_thread = threading.Thread(target=weather_thread)
        weather_thread.daemon = True
        weather_thread.start()

        # Start the main display thread
        display_date_time()
    except KeyboardInterrupt:
        pass
