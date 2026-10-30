import threading, tkinter as tk, cv2, presentation_redis
from PIL import Image, ImageTk
from ultralytics import YOLO

def hands_up(kp):
    # COCO keypoints: 5,6 = L/R shoulder, 9,10 = L/R wrist; [1] = y (0 is top, >0 means visible)
    return int(0 < kp[9][1] < kp[5][1]), int(0 < kp[10][1] < kp[6][1])

def detect(root, cam):
    model = YOLO("yolo11n-pose.pt")
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            break
        res = model(frame, verbose=False)[0]
        people = [hands_up(kp) for kp in res.keypoints.xy]
        hands = sum(1 for left_up, right_up in people if left_up or right_up)
        rgb = cv2.cvtColor(res.plot(), cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb).resize((320, 240))
        presentation_redis.push(people)
        root.after(0, update, cam, img, len(people), hands)

def update(cam, img, people, hands):
    cam.img = ImageTk.PhotoImage(img)
    cam.config(image=cam.img, text=f"👥 People: {people} | ✋ Hands: {hands}", compound="top")

def start(root):
    cam = tk.Label(root, text="📷 Starting YOLO Pose...", font=("Consolas", 12))
    cam.pack(side="right", padx=20)
    threading.Thread(target=detect, args=(root, cam), daemon=True).start()
