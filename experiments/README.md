# Phone-as-a-Sensor Experiments

Standalone scripts for trying the phone ideas from the talk plan before they go into the presentation. Run each one on its own, from this folder, with the phone and laptop on the same Wi-Fi or phone hotspot. Nothing here leaves the local network.

```bash
pip install -r ../requirements.txt -r requirements.txt
```

Find the laptop's IP with `ipconfig` (Windows) or `ip addr` (Linux/macOS), shown below as `<laptop-ip>`. Allow Python through the Windows firewall when it asks.

## 1. Phone sensors → MQTT → Python loop (Sistem Komputer)

`phone_sensor_termux.py` runs on the phone and publishes accelerometer readings to the `pythonid/sensor` topic. `phone_sensor_mqtt.py` runs on the laptop and lights a red "LED" while the phone is shaken. Replace the LED line with `serial.write(...)` to drive an Arduino or ESP32.

1. On the laptop, install [Mosquitto](https://mosquitto.org/download/) and start it with this folder's config, which lets the phone connect:
   ```bash
   mosquitto -c mosquitto.conf -v
   ```
2. On the laptop, in a second terminal:
   ```bash
   python phone_sensor_mqtt.py
   ```
3. On the phone, install [Termux](https://f-droid.org/packages/com.termux/) and the [Termux:API](https://f-droid.org/packages/com.termux.api/) app from F-Droid, then in Termux:
   ```bash
   pkg install python termux-api
   pip install paho-mqtt
   python phone_sensor_termux.py <laptop-ip>
   ```

## 2. Phone camera → YOLO (Teknik Informatika)

Install an IP camera app on the phone, such as **IP Webcam** (Android), and start its server. Then on the laptop:

```bash
python phone_camera_yolo.py http://<phone-ip>:8080/video
```

The window shows the pose detections, the people count and the inference time per frame. Press `q` to quit.

## 3. Phone mic → WebSocket → Whisper (Demo 0)

`phone_mic_whisper.py` serves `phone_mic.html` to the phone, which streams its microphone over a WebSocket. The laptop runs Whisper on each 2 seconds of audio, prints what it heard, and sends it back to the phone, marking **NEXT** or **BACK** when you say "next" or "back".

Phone browsers only allow the microphone on HTTPS pages, so create a self-signed certificate once (on Windows, `openssl` comes with Git Bash):

```bash
openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 30 -subj "/CN=pythonid"
```

Then start the server:

```bash
uvicorn phone_mic_whisper:app --host 0.0.0.0 --port 8443 --ssl-keyfile key.pem --ssl-certfile cert.pem
```

On the phone, open `https://<laptop-ip>:8443`, accept the certificate warning, and tap **Start**.
