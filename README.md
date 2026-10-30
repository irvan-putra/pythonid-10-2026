# Edge AI & Multimodal Applications in Python

A minimal, self-reading ("quine-style") presentation built with **Tkinter**, **Faster-Whisper**, **Ultralytics YOLO11 Pose**, **MQTT**, **FastAPI**, and **Streamlit**, using a smartphone as a sensor. Everything runs on the laptop and the local Wi-Fi: no cloud service, no account, no internet needed during the talk.

## Slides

`presentation.py` shows its own source code first, then every `slide_*` file in slide-number order. A new concept is introduced by a short `.md` slide with the same number, shown just before the code. The files in [`slides/`](slides/) can be code, config, a web page, scripts or a `.png` image, and the current file name shows above the camera. It imports every slide module first, then calls each one's `start(panel, go)`.

Slides 1 and 2 are plain laptop code. Later slides extend them by replacing their functions and objects when imported (monkeypatching), so each new idea lives in its own slide.

| Slide | File | What it shows |
|---|---|---|
| 0 | `presentation.py` | The presentation engine itself |
| 1 | `slides/slide_1_whisper.md` | What is Whisper? |
| 1 | `slides/slide_1_whisper.py` | Laptop mic → `faster-whisper` (`tiny.en`, `int8`) → say **"next"** / **"back"** to change slides, with a live subtitle |
| 2 | `slides/slide_2_yolo.md` | What is YOLO? |
| 2 | `slides/slide_2_yolo.py` | Laptop webcam → YOLO11 pose (`yolo11n-pose.pt`) → people and raised-hand count |
| 3 | `slides/slide_3_coco.png` | The COCO pose keypoints, and how a raised hand is detected |
| 4 | `slides/slide_4_mqtt.md` | What is MQTT? |
| 4 | `slides/slide_4_broker.py` | The "Waiting for phone..." line: the laptop runs a local [Mosquitto](https://mosquitto.org/download/) MQTT broker, started with the presentation and stopped when the window closes |
| 5 | `slides/slide_5_mosquitto.conf` | The broker config that lets the phone on the same Wi-Fi connect |
| 6 | `slides/slide_6_mqtt.py` | MQTT helpers (`listen`, `publish`) and the sensor LED: shaking the phone turns it red |
| 7 | `slides/slide_7_termux.md` | What is Termux? |
| 7 | `slides/slide_7_termux.py` | Runs on the phone in Termux and publishes its accelerometer to the broker |
| 8 | `slides/slide_8_websocket.md` | FastAPI and WebSockets |
| 8 | `slides/slide_8_sensor.py` | A FastAPI server on port 8000 that serves the phone page and its scripts |
| 9 | `slides/slide_9_sensor.html` | The page the phone opens to stream its camera and mic over WebSockets |
| 10 | `slides/slide_10_monkeypatch.md` | Monkeypatching and duck typing, used on slides 10 and 12 |
| 10 | `slides/slide_10_phone_mic.py` | Receives the phone mic and replaces Whisper's `record()`: the phone mic while it's connected, else the laptop mic |
| 11 | `slides/slide_11_phone_mic.js` | The phone side: streams the mic over the `/audio` WebSocket |
| 12 | `slides/slide_12_phone_camera.py` | Receives the phone camera and replaces YOLO's `webcam` with a `PhoneCamera` that has the same `isOpened()` / `read()` |
| 13 | `slides/slide_13_phone_camera.js` | The phone side: sends camera frames as JPEG over the `/camera` WebSocket |
| 14 | `slides/slide_14_streamlit.md` | What is Streamlit? From raw events to a dashboard |
| 14 | `slides/slide_14_publish.py` | Wraps Whisper's `show()` and YOLO's `update()` to also publish the transcript and votes to MQTT |
| 15 | `slides/slide_15_subscribe.py` | The dashboard's MQTT subscriber: keeps one row of votes per second for 10 minutes, and the transcript |
| 16 | `slides/slide_16_dashboard.py` | The local Streamlit dashboard with all the live data |

```
Laptop or phone camera ──► YOLO ──► pythonid/votes  ──► Streamlit dashboard (1 row per second)
Laptop or phone mic ──► Whisper ──► pythonid/speech ──► Streamlit word cloud (retained message)
Phone accelerometer (Termux) ─────► pythonid/sensor ──► sensor LED in the presentation
                     all through the local Mosquitto broker
```

## Setup (one time)

### Laptop

1. Install the Python packages:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Install [Mosquitto](https://mosquitto.org/download/). On Windows, if the installer added a Mosquitto service, stop it from an **Administrator** PowerShell: it only accepts connections from the laptop itself, and it holds the port the presentation needs.
   ```bash
   net stop mosquitto
   ```
3. Set your Wi-Fi connection to **Private** (Windows Settings → Network & Internet), and allow Python and Mosquitto through the firewall when Windows asks.

### Phone (Android)

1. **Accelerometer:** install [Termux](https://f-droid.org/packages/com.termux/) and [Termux:API](https://f-droid.org/packages/com.termux.api/) from F-Droid (not the Play Store), then in Termux:
   ```bash
   pkg install python termux-api
   ```
   ```bash
   python -m pip install paho-mqtt
   ```
   ```bash
   curl -O https://raw.githubusercontent.com/irvan-putra/pythonid-10-2026/main/slides/slide_7_termux.py
   ```
2. **Camera and mic:** phone browsers only allow them on secure pages (`https://` or `localhost`), even on your own Wi-Fi. In Chrome on the phone, open `chrome://flags/#unsafely-treat-insecure-origin-as-secure`, enable it, enter `http://<laptop-ip>:8000` (see below for the IP), and tap **Relaunch**.

## Running the talk

1. Connect the laptop and the phone to the same Wi-Fi (or the laptop to the phone's hotspot).
2. On the laptop, from the project folder:
   ```bash
   python presentation.py
   ```
   This opens the slides and starts the Mosquitto broker, the phone server (port 8000) and the Streamlit dashboard (port 8501). Streamlit prints a **Network URL** like `http://192.168.1.67:8501` in the terminal; that IP is the laptop's IP (`ipconfig` shows it too).
3. **Slides 4–7 (MQTT):** on the phone, in Termux, run the script with the laptop's IP, then shake the phone to turn the LED red:
   ```bash
   python slide_7_termux.py <laptop-ip>
   ```
4. **Slides 8–13 (phone camera and mic):** on the phone, open `http://<laptop-ip>:8000` in Chrome, tap **📷🎙 Start**, and allow the camera and microphone. While it streams, YOLO uses the phone camera and Whisper uses the phone mic; when the phone stops, both go back to the laptop's.
5. **Slides 14–16 (dashboard):** the audience opens the **Network URL** on their phones, on the same Wi-Fi.
6. The slides open full screen. To stop, close them with **Alt+F4** (this also stops Mosquitto and the phone server), then press **Ctrl+C** in the terminal to stop the dashboard.

### Controls

- **Left / Right Arrow Keys**: change slides
- **"next" / "back"**: say it into the laptop or phone mic to change slides
- **Raise your hand** in front of the camera: counts as a vote, shown on the laptop and the dashboard
- **Shake the phone**: lights the sensor LED

## 📊 Live Dashboard

The dashboard (`slides/slide_16_dashboard.py`) shows:

- **People / Votes** with the record so far, and **Approval** (hands ÷ people) as a percentage
- **Energy** area chart of people and hands over the last 10 minutes, shared by every viewer
- **Word cloud** of everything said so far, from the live Whisper transcript

How the data gets there:

- YOLO publishes a raw stream, one message per camera frame. The dashboard keeps one row per second for 10 minutes, so the history stays small however fast the camera runs.
- The dashboard has one MQTT subscriber (`st.cache_resource`), shared by every phone viewing it.
- Whisper publishes the whole transcript so far as a **retained** message. The broker keeps the last one and hands it to any subscriber that connects later, so the word cloud is complete even if the dashboard is first opened mid-talk.

The same dashboard is also deployed at https://pythonid-10-2026.streamlit.app as an example of free Streamlit hosting. That copy can't reach the laptop, so it shows "Waiting for votes..." instead of live data.

## Troubleshooting

- **The LED stays on "Waiting for phone...":** the Mosquitto Windows service may still be running (`net stop mosquitto`), the IP may be wrong, or the phone may be on another Wi-Fi. If the terminal says `Mosquitto not found`, install it.
- **The phone page's Start button does nothing:** the address in the Chrome flag must match the address bar exactly (`http://`, the IP and `:8000`).
- **The phone page says `Error: Permission denied`:** check that Chrome **⋮ → Settings → Site settings → Camera** and **Microphone** are on, that Android **Settings → Apps → Chrome → Permissions** allows both, and on Samsung that **Camera access** and **Mic access** are on in Quick Settings. Then reopen the page and tap **Allow**.
- **Phones can't open the dashboard or the phone page:** check the firewall prompt and that the Wi-Fi is set to **Private**.
