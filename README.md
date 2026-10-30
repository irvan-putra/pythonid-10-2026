# Edge AI & Multimodal Applications in Python

A minimal, self-reading ("quine-style") presentation built with **Tkinter**, **Faster-Whisper**, **Ultralytics YOLO11 Pose**, and **Streamlit**.

## Slides & Scripts

1. **`presentation.py`** — Main Tkinter presentation engine (loads its own source code on Slide 1 and chains the remaining slides).
2. **`presentation_whisper.py`** — Live voice slide navigation (`"next"` / `"back"`) and subtitle transcription using `faster-whisper` (`tiny.en`, `int8`) and `sounddevice`.
3. **`presentation_yolo.py`** — Live webcam people & 17-keypoint pose estimation (`yolo11n-pose.pt`) with raised-hand vote counting.
4. **`presentation_streamlit.py`** — Real-time Streamlit audience voting dashboard (`@st.fragment(run_every=1)`) displaying live people & raised-hand vote charts.

## Quick Start

```bash
pip install -r requirements.txt
python presentation.py
```

### Controls
- **Left / Right Arrow Keys**: Navigate slides
- **Voice Commands**: Say **"next"** or **"back"** into your microphone
- **Raise Hand in Webcam**: Increments the live raised-hand vote count in Tkinter and the Streamlit dashboard
