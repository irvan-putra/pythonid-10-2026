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

## Camera + mic → WebSocket → YOLO + Whisper (Teknik Informatika)

`laptop/phone.html` runs in the phone's browser, served by `laptop/phone.py` on the laptop, so no app is needed. One **Start** tap streams both:

- the back camera as JPEG frames over the `/camera` WebSocket. The laptop runs YOLO pose on each frame, shows the result in a window, and replies with the people count; then the phone sends the next frame.
- the microphone over the `/audio` WebSocket. The laptop runs Whisper on each 2 seconds of audio, prints what it heard, and sends it back, marking **NEXT** or **BACK** when you say "next" or "back".

Phone browsers only allow the camera and microphone on secure pages (`https://` or `localhost`), even on your own Wi-Fi. Pick one way:

- **Chrome flag (Android, no certificate):** on the phone open `chrome://flags/#unsafely-treat-insecure-origin-as-secure`, enable it, enter `http://<laptop-ip>:8000`, and tap **Relaunch**.
- **Self-signed certificate (any phone, including iPhone):** create it once with the command below (on Windows, `openssl` comes with Git Bash), add `--ssl-keyfile key.pem --ssl-certfile cert.pem` to the server command and use port 8443 instead of 8000, then open `https://<laptop-ip>:8443` and accept the warning.
  ```bash
  openssl req -x509 -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 30 -subj "/CN=pythonid"
  ```

Start the server from the project folder (its packages come with the main `requirements.txt`):

```bash
python -m uvicorn laptop.phone:app --host 0.0.0.0 --port 8000
```

On the phone, open `http://<laptop-ip>:8000`, tap **📷🎙 Start**, and allow the camera and microphone.

If the grey line says `Error: Permission denied`, the camera or microphone is blocked before Chrome can ask. Check that Chrome **⋮ → Settings → Site settings → Camera** and **Microphone** are on, that Android **Settings → Apps → Chrome → Permissions** allows both, and on Samsung that **Camera access** and **Mic access** are on in Quick Settings. Then reopen the page and tap **Allow** when asked.
