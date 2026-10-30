For the curious: YOLO-Face
==========================

The COCO pose model sees a face only as 5 points (nose, eyes, ears).
Face detectors are YOLO models trained on faces instead:

- Dataset: WIDER FACE, about 32,000 images with 390,000 faces,
  small, blurry, crowded, turned away...
- YOLO5Face (2021) also returns 5 facial landmarks:
  both eyes, the nose, and both mouth corners
- Community weights exist for newer YOLO versions, or train your own
  with Ultralytics on a face dataset (e.g. from Roboflow Universe)

Uses: counting faces, blurring faces for privacy, checking who is
looking at the camera.

Detection is not recognition: knowing who a face is needs another
model (e.g. ArcFace), and consent. Faces are biometric personal data
under Indonesia's personal data protection law (UU PDP, 2022).

More: roboflow.com/blog/yolo-face
