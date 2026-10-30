import threading, tkinter as tk, cv2, presentation_redis
from PIL import Image, ImageTk
from ultralytics import YOLO

def hands_up(keypoints):
    # COCO keypoints: 5,6 = L/R shoulder, 9,10 = L/R wrist; y is 0 at the top and >0 when visible
    y = keypoints[:, 1]
    return int(0 < y[9] < y[5]), int(0 < y[10] < y[6])

def detect(root, video):
    model = YOLO("yolo11n-pose.pt")
    webcam = cv2.VideoCapture(0)
    while webcam.isOpened():
        ok, frame = webcam.read()
        if not ok:
            break
        result = model(frame, verbose=False)[0]
        people = [hands_up(keypoints) for keypoints in result.keypoints.xy]
        hands = sum(1 for left_up, right_up in people if left_up or right_up)
        rgb = cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb).resize((320, 240))
        presentation_redis.push(people)
        root.after(0, update, video, image, len(people), hands)

def update(video, image, people_count, hands_count):
    video.photo = ImageTk.PhotoImage(image)
    text = f"👥 People: {people_count} | ✋ Hands: {hands_count}"
    video.config(image=video.photo, text=text, compound="top")

def start(root):
    video = tk.Label(root, text="📷 Starting YOLO Pose...", font=("Consolas", 12))
    video.pack(side="right", padx=20)
    threading.Thread(target=detect, args=(root, video), daemon=True).start()
