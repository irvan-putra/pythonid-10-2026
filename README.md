# Edge AI & Multimodal Applications in Python

A minimal, self-reading ("quine-style") presentation built with **Tkinter**, **Faster-Whisper**, **Ultralytics YOLO11 Pose**, and **Streamlit**.

## Slides & Scripts

1. **`presentation.py`** — Main Tkinter presentation engine (loads its own source code on Slide 1 and chains the remaining slides).
2. **`presentation_whisper.py`** — Live voice slide navigation (`"next"` / `"back"`) and subtitle transcription using `faster-whisper` (`tiny.en`, `int8`) and `sounddevice`.
3. **`presentation_yolo.py`** — Live webcam people & 17-keypoint pose estimation (`yolo11n-pose.pt`) with raised-hand vote counting.
4. **`presentation_streamlit.py`** — Real-time Streamlit audience voting dashboard (`@st.fragment(run_every=1)`) displaying live audience charts (see below).
5. **`presentation_redis.py`** — Tiny Upstash Redis REST relay (`push` / `read`) that sends live votes and spoken words from the laptop to the deployed dashboard.
6. **`presentation_broker.py`** — Starts the local [Mosquitto](https://mosquitto.org/download/) MQTT broker with `phone/mosquitto.conf` when the presentation starts, and stops it when the window closes.
7. **`presentation_mqtt.py`** — Phone accelerometer over MQTT (`pythonid/sensor` topic) driving a Python loop: shaking the phone lights a red "LED" in the presentation window.
8. **`phone/sensor_termux.py`** — Runs on the phone in Termux and publishes its accelerometer readings to the broker.

## 🌐 Live Dashboard

The Streamlit voting dashboard is deployed at **https://pythonid-10-2026.streamlit.app** so the audience can follow the votes on their own phones. It shows:

- **People / Votes** with the record so far, and **Approval** (hands ÷ people) as a percentage
- **Energy** area chart of people and hands over the last 10 minutes, shared by every viewer
- **Word cloud** of everything said so far, from the live Whisper transcript

## Quick Start

```bash
pip install -r requirements.txt
python presentation.py
```

### Controls
- **Left / Right Arrow Keys**: Navigate slides
- **Voice Commands**: Say **"next"** or **"back"** into your microphone
- **Raise Hand in Webcam**: Increments the live raised-hand vote count in Tkinter and the Streamlit dashboard
- **Shake the Phone**: Lights the sensor LED. Run [`phone/sensor_termux.py`](phone/sensor_termux.py) on the phone with the laptop's IP; see [phone/README.md](phone/README.md) for the one-time setup.

## Phone as a Sensor

The [`phone/`](phone/) folder has the scripts for using a smartphone as the sensor over local Wi-Fi: the accelerometer over MQTT (part of the presentation), plus standalone camera → YOLO and microphone → Whisper pages served over a WebSocket.

## Pushing Votes from the Laptop to the Deployed Dashboard

The deployed app runs on Streamlit Community Cloud, which can't reach the presenter's laptop and can't receive incoming requests. So both sides talk to a small shared key-value store, a free [Upstash Redis](https://upstash.com) database, through its REST API:

```
Laptop (YOLO + Whisper) --LPUSH history / SET live--> Upstash Redis <--LRANGE history / GET live (every 1s)-- pythonid-10-2026.streamlit.app
```

- `presentation_yolo.py` calls `presentation_redis.push(people, hands)` from its detection thread with the people and raised-hand counts. Pushes are throttled to one per second (one pipelined HTTP request) so they don't slow down the webcam loop.
- `presentation_whisper.py` appends the transcript to `presentation_redis.live`, which rides along with each push.
- Redis keeps two keys: `history`, a list of the last 600 one-second snapshots (10 minutes), and `live`, the full transcript.
- The dashboard wraps `presentation_redis.read()` in `st.cache_data(ttl=1)`. All audience sessions share one Redis read per second, which keeps usage well inside the free tier.
- If the Upstash variables aren't set, `presentation_redis.py` defaults to a local Redis at `http://localhost:8079` with token `local_token` (see [Local Redis](#local-redis-optional) below).

### Setup

1. Create a free Redis database at [upstash.com](https://upstash.com) and copy its **REST URL** and **REST token**.
2. **Deployed dashboard**: in Streamlit Community Cloud, open the app → **Settings → Secrets** and add:
   ```toml
   UPSTASH_REDIS_REST_URL = "https://<your-db>.upstash.io"
   UPSTASH_REDIS_REST_TOKEN = "<your-token>"
   ```
   (Streamlit exposes top-level secrets as environment variables, so the same `os.environ` lookup works in both places.)
3. **Laptop**: set the same two variables before starting the presentation:
   ```bash
   export UPSTASH_REDIS_REST_URL="https://<your-db>.upstash.io"
   export UPSTASH_REDIS_REST_TOKEN="<your-token>"
   python presentation.py
   ```
   On Windows PowerShell, use `$env:UPSTASH_REDIS_REST_URL="..."` instead.

Never commit the token. Keep it in Streamlit secrets and in your shell environment only.

### Local Redis (optional)

To rehearse offline, run Redis on your laptop instead of Upstash. Plain Redis doesn't speak Upstash's REST API, so put [Serverless Redis HTTP (SRH)](https://github.com/hiett/serverless-redis-http) in front of it. With [Docker](https://www.docker.com/products/docker-desktop/) installed:

```bash
docker network create redis-net
docker run -d --name redis --network redis-net redis
docker run -d --name redis-http --network redis-net -p 8079:80 -e SRH_MODE=env -e SRH_TOKEN=local_token -e SRH_CONNECTION_STRING="redis://redis:6379" hiett/serverless-redis-http
```

Then leave the `UPSTASH_*` variables unset (or remove them) and run both sides on the laptop:

```bash
python presentation.py
```

The presentation and the local dashboard at http://localhost:8501 both use the defaults (`http://localhost:8079`, `local_token`). The deployed dashboard can't reach your laptop, so it stays on "Waiting for votes..." in this mode.

To stop it later: `docker stop redis-http redis`, and `docker start redis redis-http` to bring it back.

If push fails, the terminal prints `push failed: ...`: `Connection refused` means the containers aren't running; `401 Unauthorized` means the token doesn't match.
