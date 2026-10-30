# Phone-as-a-Sensor Experiments

Standalone scripts for trying the phone ideas from the talk plan before they go into the presentation. Run each one on its own, from this folder, with the phone and laptop on the same Wi-Fi or phone hotspot. Nothing here leaves the local network.

```bash
python -m pip install -r ../requirements.txt -r requirements.txt
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

## Phone browser setup (for experiments 2 and 3)

Experiments 2 and 3 run in the phone's browser, served by the laptop, so no app is needed. Phone browsers only allow the camera and microphone on secure pages (`https://` or `localhost`), even on your own Wi-Fi. Pick one way:

- **Chrome flag (Android, no certificate):** on the phone open `chrome://flags/#unsafely-treat-insecure-origin-as-secure`, enable it, enter `http://<laptop-ip>:8000`, and tap **Relaunch**. Start the servers below on port 8000 without the `--ssl-...` options.
- **Self-signed certificate (any phone, including iPhone):** create it once with the command below (on Windows, `openssl` comes with Git Bash), add `--port 8443 --ssl-keyfile key.pem --ssl-certfile cert.pem` to the server command, open `https://<laptop-ip>:8443` and accept the warning.
  ```bash
  openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 30 -subj "/CN=pythonid"
  ```

Run one server at a time, since both use the same port.

## 2. Phone camera → WebSocket → YOLO (Teknik Informatika)

`phone_camera.html` shows the phone's back camera and sends a JPEG frame over a WebSocket; `phone_camera_yolo.py` runs YOLO pose on it, shows the result in a window on the laptop, and replies with the people count, then the phone sends the next frame.

```bash
python -m uvicorn phone_camera_yolo:app --host 0.0.0.0 --port 8000
```

On the phone, open `http://<laptop-ip>:8000` and tap **📷 Start**.

## 3. Phone mic → WebSocket → Whisper (Demo 0)

`phone_mic.html` streams the phone's microphone over a WebSocket. `phone_mic_whisper.py` runs Whisper on each 2 seconds of audio, prints what it heard, and sends it back to the phone, marking **NEXT** or **BACK** when you say "next" or "back".

```bash
python -m uvicorn phone_mic_whisper:app --host 0.0.0.0 --port 8000
```

On the phone, open `http://<laptop-ip>:8000` and tap **🎙 Start**.
