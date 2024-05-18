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

# Colors - Yeah, I'm a stars fan.  You'll need to adjust RGB or if your board has B/G backwards then make it RBG
DALLAS_GREEN = (0, 97, 65)
WHITE = (255, 255, 255)

# Font settings
FONT_PATH = "/home/pi/nhl-led-scoreboard/assets/fonts/04B_24__.TTF"
DATE_FONT_SIZE = 8
TIME_FONT_SIZE = 24
TEMP_HUM_FONT_SIZE = 8

# Brightness levels
DIM_BRIGHTNESS = 40  # Adjust as needed
FULL_BRIGHTNESS = 80

# Function to rotate image
def rotate_image(image):
    return image.rotate(180)

# Function to get temperature and humidity from OpenWeatherMap API
# You'll need to edit OWM_ZIP and OWM_API_KEY to match your settings
def get_temp_and_humidity():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=OWM_ZIP&appid=OWM_API_KEY&units=imperial"
    response = requests.get(url)
    data = response.json()
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    return temperature, humidity

# Function to display the date, time, temperature, and humidity.
def display_date_time():
    while True:
        current_time = datetime.now()

        # Adjust brightness based on time
        matrix.brightness = DIM_BRIGHTNESS if 21 <= current_time.hour or current_time.hour < 9 else FULL_BRIGHTNESS

        # Extracting date and time components
        date_string = current_time.strftime("%b %d %Y")
        time_string = current_time.strftime("%H:%M")

        # Get temperature and humidity from OpenWeatherMap API
        temperature, humidity = get_temp_and_humidity()

        # Remove the degree symbol from temperature
        temperature = str(temperature).split('.')[0]

        # Create a blank image
        image = Image.new("RGB", (options.cols, options.rows), color=(0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Load fonts
        font_date = ImageFont.truetype(FONT_PATH, DATE_FONT_SIZE)
        font_time = ImageFont.truetype(FONT_PATH, TIME_FONT_SIZE)
        font_temp_hum = ImageFont.truetype(FONT_PATH, TEMP_HUM_FONT_SIZE)

        # Calculate text positions for centering
        date_width, date_height = draw.textsize(date_string, font=font_date)
        date_position = ((options.cols - date_width) // 2, 1)

        time_width, time_height = draw.textsize(time_string, font=font_time)
        time_position = ((options.cols - time_width) // 2, 5)

        temp_hum_text = f"{temperature}F    {humidity}%"
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

        time.sleep(5)  # Update every minute

if __name__ == "__main__":
    try:
        display_date_time()
    except KeyboardInterrupt:
        pass
