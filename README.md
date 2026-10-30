# Edge AI & Multimodal Applications in Python

A minimal, self-reading ("quine-style") presentation built with **Tkinter**, **Faster-Whisper**, **Ultralytics YOLO11 Pose**, **MQTT**, **FastAPI**, and **Streamlit**, using a smartphone as a sensor. The AI and the phone sensors run on the laptop and the local Wi-Fi; the dashboard's data also goes to a free public MQTT broker, so the audience can follow it online at **https://pythonid-10-2026.streamlit.app**. If the internet drops, everything on the laptop keeps working.

## Slides

`presentation.py` opens with the Tkinter introduction, shows its own source code, then every other `slide_*` file in slide-number order. A new concept is introduced by a short `.md` slide with the same number; within a number, code (`.py`) comes last. The files in [`slides/`](slides/) can be code, config, a web page, scripts or a `.png` image, and the current file name shows above the camera. It imports every slide module first, then calls each one's `start(panel, go)`.

Slides 1 and 2 are plain laptop code. Later slides extend them by replacing their functions and objects when imported (monkeypatching), so each new idea lives in its own slide.

| Slide | File | What it shows |
|---|---|---|
| 0 | `slides/slide_0_tkinter.md` | What is Tkinter? |
| 0 | `presentation.py` | The presentation engine itself |
| 1 | `slides/slide_1_whisper.md` | What is Whisper? |
| 1 | `slides/slide_1_whisper.py` | Laptop mic → `faster-whisper` (`tiny.en`, `int8`) → say **"next"** / **"back"** to change slides, with a live subtitle |
| 2 | `slides/slide_2_yolo.md` | What is YOLO? |
| 2 | `slides/slide_2_yolo.py` | Laptop webcam → YOLO11 pose (`yolo11n-pose.pt`) → people and raised-hand count |
| 3 | `slides/slide_3_coco.png` | The COCO pose keypoints, and how a raised hand is detected |
| 3 | `slides/slide_3_yolo_face.md` | For the curious: YOLO-Face, face detection vs recognition |
| 4 | `slides/slide_4_mqtt.md` | What is MQTT? |
| 4 | `slides/slide_4_mqtt_vs_coap.md` | MQTT vs CoAP: two ways to talk IoT |
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
| 13 | `slides/slide_13_phone_camera.js` | The phone side: rotates each camera frame to match how the phone is held (from gravity, via `devicemotion`), then sends it as JPEG over the `/camera` WebSocket |
| 14 | `slides/slide_14_streamlit.md` | What is Streamlit? From raw events to a dashboard |
| 14 | `slides/slide_14_publish.py` | Wraps Whisper's `show()` and YOLO's `update()` to also publish the transcript and votes, to the laptop's broker and to the public `broker.hivemq.com` |
| 15 | `slides/slide_15_subscribe.py` | The dashboard's MQTT subscriber on the public broker: keeps one row of votes per second for 10 minutes (Jakarta time), and the transcript |
| 16 | `slides/slide_16_dashboard.py` | The Streamlit dashboard: hosted on Streamlit Community Cloud for the audience, and started by the presentation on the laptop with `--local` |

```
                                  laptop: Mosquitto                 internet: broker.hivemq.com
Laptop or phone camera ──► YOLO ──► pythonid/votes   +  irvan-putra/pythonid-10-2026/votes  ──► dashboards
Laptop or phone mic ──► Whisper ──► pythonid/speech  +  irvan-putra/pythonid-10-2026/speech ──► word clouds
Phone accelerometer (Termux) ─────► pythonid/sensor  ──► sensor LED in the presentation (stays on the laptop)
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
   This opens the slides and starts the Mosquitto broker, the phone server (port 8000) and a local copy of the dashboard at http://localhost:8501. Find the laptop's IP for the phone with `ipconfig` (IPv4 Address).
3. **Slides 4–7 (MQTT):** on the phone, in Termux, run the script with the laptop's IP, then shake the phone to turn the LED red:
   ```bash
   python slide_7_termux.py <laptop-ip>
   ```
4. **Slides 8–13 (phone camera and mic):** on the phone, open `http://<laptop-ip>:8000` in Chrome, tap **📷🎙 Start**, and allow the camera and microphone. While it streams, YOLO uses the phone camera and Whisper uses the phone mic; when the phone stops, both go back to the laptop's.
5. **Slides 14–16 (dashboard):** the audience opens **https://pythonid-10-2026.streamlit.app** on their phones, over their own mobile data or any Wi-Fi.
6. The slides open full screen. To stop, close them with **Alt+F4**; this also stops Mosquitto, the phone server and the local dashboard.

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
- `slides/slide_14_publish.py` sends the votes and speech to the laptop's broker and to the free public broker `broker.hivemq.com`, under `irvan-putra/pythonid-10-2026/` so they don't clash with other users. The phone sensor stays on the laptop.

There are two copies of the same dashboard code. The online one reads the public broker. The one the presentation starts on the laptop gets `--local` and reads the laptop's broker, so it also works without internet; open it at http://localhost:8501.

The online dashboard is hosted on [Streamlit Community Cloud](https://streamlit.io/cloud) with **`slides/slide_16_dashboard.py`** as its main file; it installs the small [`slides/requirements.txt`](slides/requirements.txt) next to it instead of the full presentation requirements. Open it once before the talk: free apps go to sleep when nobody has used them for a while.

A public broker has no password: anyone can read these topics, or publish to them. That's fine for vote counts and the talk's own transcript, but never send private data through it; for that, use a broker with logins, such as a free HiveMQ Cloud account.

## Troubleshooting

- **The LED stays on "Waiting for phone...":** the Mosquitto Windows service may still be running (`net stop mosquitto`), the IP may be wrong, or the phone may be on another Wi-Fi. If the terminal says `Mosquitto not found`, install it.
- **The phone page's Start button does nothing:** the address in the Chrome flag must match the address bar exactly (`http://`, the IP and `:8000`).
- **The phone page says `Error: Permission denied`:** check that Chrome **⋮ → Settings → Site settings → Camera** and **Microphone** are on, that Android **Settings → Apps → Chrome → Permissions** allows both, and on Samsung that **Camera access** and **Mic access** are on in Quick Settings. Then reopen the page and tap **Allow**.
- **The phone can't open the phone page:** check the firewall prompt and that the Wi-Fi is set to **Private**.
- **The online dashboard stays on "Waiting for votes...":** the laptop needs internet. Check that HiveMQ receives the data in its web client (https://www.hivemq.com/demos/websocket-client/) by subscribing to `irvan-putra/pythonid-10-2026/#`.
