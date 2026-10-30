What is Termux?
===============

- A Linux terminal for Android, no root needed
- Installs real packages: pkg install python
- Termux:API adds commands for the phone's hardware:
  termux-sensor, termux-battery-status, termux-location,
  termux-camera-photo, termux-vibrate...

The accelerometer measures acceleration on 3 axes (x, y, z) in m/s²:
- phone lying still: about 9.8 m/s², which is gravity
- phone shaken: much more

Here: termux-sensor -> Python -> MQTT -> the force shown on the laptop
