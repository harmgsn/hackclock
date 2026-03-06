Download tempest-weather-clock.py
Download 04B_24__.TTF (FONT)
Download and run tempest-weather-clock-setup.sh
Once setup completes - you can run the clock with:
env/bin/python3 tempest_weather_clock.py

The python environment is setup and prepared as part of the setup script.

I am not a python developer, I am not a developer.  I'm a sysadmin - I hack to make it work for me.

Feel free to take and modify this to work for you

The original "main.py" clock is no longer maintained.  It supports OpenWeatherMap but will need to be updated to support pillow>v10 and python environments with python >3.13.

You will need to edit this and change OWM_ZIP and OWM_API_KEY to be yours
You can also edit the DALLAS_GREEN at the top to change the colors.  In it's current format it's RGB - but your display might be RBG so you'll have to swap values around to make it look right for you.

![](https://github.com/harmgsn/hackclock/blob/main/Example.png)
