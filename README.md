# Edge AI & Multimodal Applications in Python

A minimal, self-reading ("quine-style") presentation built with **Tkinter**, **Faster-Whisper**, **Ultralytics YOLO11 Pose**, and **Streamlit**.

## Slides & Scripts

1. **`presentation.py`** — Main Tkinter presentation engine (loads its own source code on Slide 1 and chains the remaining slides).
2. **`presentation_whisper.py`** — Live voice slide navigation (`"next"` / `"back"`) and subtitle transcription using `faster-whisper` (`tiny.en`, `int8`) and `sounddevice`.
3. **`presentation_yolo.py`** — Live webcam people & 17-keypoint pose estimation (`yolo11n-pose.pt`) with raised-hand vote counting.
4. **`presentation_redis.py`** — Tiny Upstash Redis REST relay (`push` / `read`) that sends live votes from the laptop to the deployed dashboard.
5. **`presentation_streamlit.py`** — Real-time Streamlit audience voting dashboard (`@st.fragment(run_every=1)`) displaying live people & raised-hand vote charts.

## 🌐 Live Dashboard

The Streamlit voting dashboard is deployed at **https://pythonid-10-2026.streamlit.app** so the audience can follow the votes on their own phones.

## Quick Start

```bash
pip install -r requirements.txt
python presentation.py
```

### Controls
- **Left / Right Arrow Keys**: Navigate slides
- **Voice Commands**: Say **"next"** or **"back"** into your microphone
- **Raise Hand in Webcam**: Increments the live raised-hand vote count in Tkinter and the Streamlit dashboard

## Pushing Votes from the Laptop to the Deployed Dashboard

The deployed app runs on Streamlit Community Cloud, which can't see `votes.txt` on the presenter's laptop and can't receive incoming requests. So both sides talk to a small shared key-value store, a free [Upstash Redis](https://upstash.com) database, through its REST API:

```
Laptop (YOLO) --SET votes "people,hands"--> Upstash Redis <--GET votes (every 1s)-- pythonid-10-2026.streamlit.app
```

- `presentation_yolo.py` calls `presentation_redis.push(people, hands)` from its detection thread. Pushes are throttled to one per second so they don't slow down the webcam loop.
- The dashboard wraps `presentation_redis.read()` in `st.cache_data(ttl=1)`. All audience sessions share one Redis `GET` per second, which keeps usage well inside the free tier.
- If the Upstash variables aren't set, everything falls back to the local `votes.txt` file, so offline use still works.

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
