What is YOLO?
=============

- "You Only Look Once": finds objects in an image in a single pass
  of a neural network, fast enough for live video
- Introduced in 2015 by Redmon et al.; since then many teams have
  built new versions. This talk uses YOLO11 from Ultralytics
  (pip install ultralytics, AGPL-3.0 licence)
- Tasks: detect, segment, classify, track, and pose

Pose estimation with yolo11n-pose.pt:
- n = nano, the smallest model (about 3M parameters), runs on a CPU
- trained on the COCO dataset: for every person it returns a box
  and 17 keypoints (eyes, ears, shoulders, elbows, wrists, hips,
  knees, ankles...) as (x, y) pixel positions

Here: webcam frame -> people and keypoints -> who has a hand up?
