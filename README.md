This is *NOT* compatible with Pillow 10.x  - You'll have to remove it and install Pillow 9.5.0

pip uninstall pillow
pip install pillow==9.5.0

I am not a python developer, I am not a developer.  I'm a sysadmin - I hack to make it work for me.

Feel free to take and modify this to work for you

You will need to edit this and change OWM_ZIP and OWM_API_KEY to be yours
You can also edit the DALLAS_GREEN at the top to change the colors.  In it's current format it's RGB - but your display might be RBG so you'll have to swap values around to make it look right for you.

