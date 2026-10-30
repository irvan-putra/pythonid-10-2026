# Edge AI & Multimodal Applications in Python

A minimal, self-reading ("quine-style") presentation built with **Tkinter**, **Faster-Whisper**, **Ultralytics YOLO11 Pose**, **MQTT**, and **Streamlit**. Everything runs on the laptop and the local Wi-Fi: no cloud service, no account, no internet needed during the talk.

## Slides & Scripts

**`presentation.py`** is the Tkinter presentation engine. After the title it shows its own source code, then every `slide_*.py` file in [`slides/`](slides/) in name order, with the current file name above the camera. Each slide module that has a `start(panel, go)` function adds its part of the live demo.

1. **`slides/slide_1_whisper.py`** — Live voice slide navigation (`"next"` / `"back"`) and subtitle transcription using `faster-whisper` (`tiny.en`, `int8`) and `sounddevice`. Publishes the transcript to the `pythonid/speech` topic.
2. **`slides/slide_2_yolo.py`** — Live webcam people & 17-keypoint pose estimation (`yolo11n-pose.pt`) with raised-hand vote counting. Publishes the counts on every frame to the `pythonid/votes` topic.
3. **`slides/slide_3_broker.py`** — Starts the local [Mosquitto](https://mosquitto.org/download/) MQTT broker with `slides/mosquitto.conf` when the presentation starts, and stops it when the window closes.
4. **`slides/slide_4_mqtt.py`** — Shared MQTT helpers (`listen`, `publish`), and the phone accelerometer (`pythonid/sensor` topic) driving a Python loop: shaking the phone lights a red "LED" in the presentation window.
5. **`slides/slide_5_termux.py`** — Runs on the phone in Termux and publishes its accelerometer readings to the broker. The presentation only shows it.
6. **`slides/slide_6_dashboard.py`** — Real-time Streamlit audience dashboard (`@st.fragment(run_every=1)`) that subscribes to the votes and speech topics.

```
Phone accelerometer ──► pythonid/sensor ──► sensor LED in the presentation
Webcam ──► YOLO ──────► pythonid/votes  ──► Streamlit dashboard (keeps 1 row per second)
Microphone ──► Whisper ► pythonid/speech ──► Streamlit word cloud (retained message)
                  all through the local Mosquitto broker
```

## 📊 Live Dashboard

The presentation starts the Streamlit dashboard on the laptop. The audience opens it on their phones, on the same Wi-Fi, at the **Network URL** that Streamlit prints in the terminal (`http://<laptop-ip>:8501`). It shows:

- **People / Votes** with the record so far, and **Approval** (hands ÷ people) as a percentage
- **Energy** area chart of people and hands over the last 10 minutes, shared by every viewer
- **Word cloud** of everything said so far, from the live Whisper transcript

How the data gets there:

- YOLO publishes a raw stream, one message per camera frame. The dashboard keeps one row per second for 10 minutes, so the history stays small however fast the camera runs.
- The dashboard has one MQTT subscriber (`st.cache_resource`), shared by every phone viewing it.
- Whisper publishes the whole transcript so far as a **retained** message. The broker keeps the last one and hands it to any subscriber that connects later, so the word cloud is complete even if the dashboard is first opened mid-talk.

The same dashboard is also deployed at https://pythonid-10-2026.streamlit.app as an example of free Streamlit hosting. That copy can't reach the laptop, so it shows "Waiting for votes..." instead of live data.

## Quick Start

Install [Mosquitto](https://mosquitto.org/download/) once (see [phone/README.md](phone/README.md) for the Windows service note), then:

```bash
pip install -r requirements.txt
python presentation.py
```

Allow Python and Mosquitto through the Windows firewall when asked, so phones on the Wi-Fi can reach the dashboard and the broker.

### Controls
- **Left / Right Arrow Keys**: Navigate slides
- **Voice Commands**: Say **"next"** or **"back"** into your microphone
- **Raise Hand in Webcam**: Increments the live raised-hand vote count in Tkinter and the Streamlit dashboard
- **Shake the Phone**: Lights the sensor LED. Run [`slides/slide_5_termux.py`](slides/slide_5_termux.py) on the phone with the laptop's IP; see [phone/README.md](phone/README.md) for the one-time setup.

## Phone as a Sensor

[phone/README.md](phone/README.md) covers using a smartphone as the sensor over local Wi-Fi: the accelerometer over MQTT (part of the presentation), plus a standalone page that streams the phone's camera into YOLO and its microphone into Whisper, served over WebSockets by `laptop/phone.py`.
