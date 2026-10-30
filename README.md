# Edge AI & Multimodal Applications in Python

A minimal, self-reading ("quine-style") presentation built with **Tkinter**, **Faster-Whisper**, **Ultralytics YOLO11 Pose**, and **Streamlit**.

## Slides & Scripts

1. **`presentation.py`** — Main Tkinter presentation engine (loads its own source code on Slide 1 and chains the remaining slides).
2. **`presentation_whisper.py`** — Live voice slide navigation (`"next"` / `"back"`) and subtitle transcription using `faster-whisper` (`tiny.en`, `int8`) and `sounddevice`.
3. **`presentation_yolo.py`** — Live webcam people & 17-keypoint pose estimation (`yolo11n-pose.pt`) with raised-hand vote counting.
4. **`presentation_streamlit.py`** — Real-time Streamlit audience voting dashboard (`@st.fragment(run_every=1)`) displaying live audience charts (see below).
5. **`presentation_redis.py`** — Tiny Upstash Redis REST relay (`push` / `read`) that sends live votes, slide number and spoken words from the laptop to the deployed dashboard.

## 🌐 Live Dashboard

The Streamlit voting dashboard is deployed at **https://pythonid-10-2026.streamlit.app** so the audience can follow the votes on their own phones. It shows:

- **People / Votes** with the record so far, **Approval** (hands ÷ people) as a percentage and progress bar, and **Reaction** time (seconds from the start of the current slide to its peak in hands)
- **Energy** area chart of people and hands over the last 10 minutes, shared by every viewer
- **Hands up vs. down** split and **left vs. right hand** counts (handy for two-option polls)
- **Votes per slide** (most hands seen on each slide)
- **Top words** spoken, from the live Whisper transcript

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
Laptop (YOLO + Whisper + slides) --LPUSH history / SET live--> Upstash Redis <--LRANGE history / GET live (every 1s)-- pythonid-10-2026.streamlit.app
```

- `presentation_yolo.py` calls `presentation_redis.push(people)` from its detection thread with one `(left_hand_up, right_hand_up)` entry per person. Pushes are throttled to one per second (one pipelined HTTP request) so they don't slow down the webcam loop.
- `presentation.py` records the current slide and `presentation_whisper.py` counts transcribed words in `presentation_redis.live` / `presentation_redis.words`; both ride along with each push.
- Redis keeps two keys: `history`, a list of the last 600 one-second snapshots (10 minutes), and `live`, the top words and most hands per slide.
- The dashboard wraps `presentation_redis.read()` in `st.cache_data(ttl=1)`. All audience sessions share one Redis read per second, which keeps usage well inside the free tier.
- If the Upstash variables aren't set, everything falls back to local `votes.txt` (history) and `live.json` files, so offline use still works. Delete an old `votes.txt` from before this change, as its format is different.

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
