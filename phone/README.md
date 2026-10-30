# Phone as a Sensor

Scripts for using a smartphone as the sensor over local Wi-Fi, so nothing leaves the local network. Keep the phone and laptop on the same Wi-Fi or phone hotspot.

Find the laptop's IP with `ipconfig` (Windows) or `ip addr` (Linux/macOS), shown below as `<laptop-ip>`. Allow Python and Mosquitto through the Windows firewall when it asks, and set the Wi-Fi connection to **Private**.

## Accelerometer → MQTT → presentation (Sistem Komputer)

`termux.py` runs on the phone and publishes accelerometer readings to the `pythonid/sensor` topic. The presentation's `laptop/broker.py` starts the Mosquitto broker with `laptop/mosquitto.conf`, and `laptop/mqtt.py` lights the sensor LED while the phone is shaken.

**Laptop (one time):** install [Mosquitto](https://mosquitto.org/download/). On Windows, if the installer added a Mosquitto service, stop it from an Administrator PowerShell with `net stop mosquitto`: it only accepts connections from the laptop itself, and it holds the port the presentation needs.

**Phone (one time):** install [Termux](https://f-droid.org/packages/com.termux/) and [Termux:API](https://f-droid.org/packages/com.termux.api/) from F-Droid, then in Termux:

```bash
pkg install python termux-api
```
```bash
python -m pip install paho-mqtt
```

Copy `termux.py` to the phone, for example:

```bash
curl -O https://raw.githubusercontent.com/irvan-putra/pythonid-10-2026/main/phone/termux.py
```

**Each time:** start `python presentation.py` on the laptop, then on the phone:

```bash
python termux.py <laptop-ip>
```

## Phone browser setup (for the camera and mic pages)

The camera and mic pages run in the phone's browser, served by the laptop from the `laptop/` folder, so no app is needed. Their packages come with the main `requirements.txt`. Run the commands below from the project folder.

Phone browsers only allow the camera and microphone on secure pages (`https://` or `localhost`), even on your own Wi-Fi. Pick one way:

- **Chrome flag (Android, no certificate):** on the phone open `chrome://flags/#unsafely-treat-insecure-origin-as-secure`, enable it, enter `http://<laptop-ip>:8000`, and tap **Relaunch**.
- **Self-signed certificate (any phone, including iPhone):** create it once with the command below (on Windows, `openssl` comes with Git Bash), add `--port 8443 --ssl-keyfile key.pem --ssl-certfile cert.pem` to the server command instead of `--port 8000`, open `https://<laptop-ip>:8443` and accept the warning.
  ```bash
  openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 30 -subj "/CN=pythonid"
  ```

Run one server at a time, since both use the same port.

## Camera → WebSocket → YOLO (Teknik Informatika)

`laptop/camera.html` shows the phone's back camera and sends a JPEG frame over a WebSocket. `laptop/camera.py` runs YOLO pose on it, shows the result in a window on the laptop, and replies with the people count; then the phone sends the next frame.

```bash
python -m uvicorn laptop.camera:app --host 0.0.0.0 --port 8000
```

On the phone, open `http://<laptop-ip>:8000` and tap **📷 Start**.

## Mic → WebSocket → Whisper

`laptop/mic.html` streams the phone's microphone over a WebSocket. `laptop/mic.py` runs Whisper on each 2 seconds of audio, prints what it heard, and sends it back to the phone, marking **NEXT** or **BACK** when you say "next" or "back".

```bash
python -m uvicorn laptop.mic:app --host 0.0.0.0 --port 8000
```

On the phone, open `http://<laptop-ip>:8000` and tap **🎙 Start**.

If the grey line says `Error: Permission denied`, the microphone is blocked before Chrome can ask. Check that Chrome **⋮ → Settings → Site settings → Microphone** is on, that Android **Settings → Apps → Chrome → Permissions → Microphone** is allowed, and on Samsung that **Mic access** is on in Quick Settings. Then reopen the page and tap **Allow** when asked.
