import time, threading, tkinter as tk, cv2, slide_5_mqtt as mqtt
from PIL import Image, ImageTk
from ultralytics import YOLO

phone = {"frame": None, "time": 0}  # latest phone camera frame (slide_7_sensor.py)

def hand_up(keypoints):
    y = keypoints[:, 1]  # 9,5 = left wrist/shoulder, 10,6 = right; y: top is 0, visible >0
    return bool(0 < y[9] < y[5] or 0 < y[10] < y[6])

def detect(root, video):
    model = YOLO("yolo11n-pose.pt")
    webcam = cv2.VideoCapture(0)
    while True:
        if time.time() - phone["time"] < 1:  # the phone camera takes over while it streams
            frame, phone["frame"] = phone["frame"], None
        else:
            ok, frame = webcam.read()
        if frame is None:  # no new phone frame yet, or no webcam
            time.sleep(0.03)
            continue
        result = model(frame, verbose=False)[0]
        raised = [hand_up(keypoints) for keypoints in result.keypoints.xy]
        people, hands = len(raised), sum(raised)
        rgb = cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb).resize((320, 240))
        mqtt.publish("votes", {"people": people, "hands": hands})
        root.after(0, update, video, image, people, hands)

def update(video, image, people, hands):
    video.photo = ImageTk.PhotoImage(image)
    text = f"👥 People: {people} | ✋ Hands: {hands}"
    video.config(image=video.photo, text=text, compound="top")

def start(root, go):
    video = tk.Label(root, text="📷 Starting YOLO Pose...", font=("Consolas", 12))
    video.pack()
    threading.Thread(target=detect, args=(root, video), daemon=True).start()
