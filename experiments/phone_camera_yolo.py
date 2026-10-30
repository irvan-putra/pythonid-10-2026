import sys, cv2
from ultralytics import YOLO

# python phone_camera_yolo.py http://<phone-ip>:8080/video   (IP Webcam app on the phone)
model, phone = YOLO("yolo11n-pose.pt"), cv2.VideoCapture(sys.argv[1])
while phone.isOpened():
    ok, frame = phone.read()
    if not ok:
        break
    result = model(frame, verbose=False)[0]
    image = result.plot()
    text = f"People: {len(result.boxes)} | {result.speed['inference']:.0f} ms"
    cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Phone camera -> YOLO (q to quit)", image)
    if cv2.waitKey(1) == ord("q"):
        break
