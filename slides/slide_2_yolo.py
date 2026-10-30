import threading, tkinter as tk, cv2
from PIL import Image, ImageTk
from ultralytics import YOLO

webcam = cv2.VideoCapture(0)

def hand_up(keypoints):
    """COCO pose keypoints, facing the camera, left hand up:

                     9
                     |
       4 2 0 1 3     7
                     |
     6 ------+------ 5
     |       |
     8       |
     |  12 --+-- 11
    10   |       |
        14       13
         |       |
        16       15

    A hand is up when its wrist is above its shoulder (y is 0 at the top).
    """
    y = keypoints[:, 1]
    return bool(0 < y[9] < y[5] or 0 < y[10] < y[6])

def detect(root, video):
    model = YOLO("yolo11n-pose.pt")
    while webcam.isOpened():
        ok, frame = webcam.read()
        if not ok:
            break
        result = model(frame, verbose=False)[0]
        raised = [hand_up(keypoints) for keypoints in result.keypoints.xy]
        people, hands = len(raised), sum(raised)
        rgb = cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb).resize((320, 240))
        root.after(0, update, video, image, people, hands)

def update(video, image, people, hands):
    video.photo = ImageTk.PhotoImage(image)
    text = f"👥 People: {people} | ✋ Hands: {hands}"
    video.config(image=video.photo, text=text, compound="top")

def start(root, go):
    video = tk.Label(root, text="📷 Starting YOLO Pose...", font=("Consolas", 12))
    video.pack()
    threading.Thread(target=detect, args=(root, video), daemon=True).start()
