import argparse
import numpy as np
import cv2
from ultralytics import YOLO
from yolox.tracker.byte_tracker import BYTETracker

# parse CLI args (video input, output, model)
parser = argparse.ArgumentParser(description="Run MOT with YOLOv8 + BYTETracker")
parser.add_argument("--video", "-v", type=str, default=None, help="Path to input video file. If omitted, webcam is used.")
parser.add_argument("--output", "-o", type=str, default=None, help="Optional output video path to save results.")
parser.add_argument("--model", "-m", type=str, default="yolov8n.pt", help="YOLO model path.")
parser.add_argument("--frame_rate", type=int, default=30, help="Frame rate for tracker / output.")
cli_args = parser.parse_args()

# --- create args with all required attributes for BYTETracker ---
args = argparse.Namespace()
args.track_thresh = 0.5
args.match_thresh = 0.8
args.track_buffer = 30
args.mot20 = False
args.frame_rate = cli_args.frame_rate
args.det_thresh = 0.5
args.min_box_area = 10

# --- initialize tracker ---
tracker = BYTETracker(args)

# --- load YOLOv8 model ---
model = YOLO(cli_args.model)

# open video or webcam
if cli_args.video:
    cap = cv2.VideoCapture(cli_args.video)
else:
    cap = cv2.VideoCapture(0)

# optional video writer
writer = None
if cli_args.output:
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cli_args.frame_rate or cap.get(cv2.CAP_PROP_FPS) or 30
    writer = cv2.VideoWriter(cli_args.output, fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)[0]
    dets = []

    for box in results.boxes:
        try:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            score = float(box.conf.cpu().numpy()[0])
            dets.append([x1, y1, x2, y2, score])
        except Exception:
            continue

    if len(dets) == 0:
        dets_for_tracker = np.zeros((0, 5), dtype=np.float32)
    else:
        dets = np.array(dets, dtype=np.float32)
        dets_for_tracker = dets[:, :5]

    img_info = [frame.shape[0], frame.shape[1], 1.0]  # H, W, scale_factor
    img_size = [frame.shape[0], frame.shape[1]]

    online_targets = tracker.update(dets_for_tracker, img_info, img_size)

    # draw tracks
    for t in online_targets:
        x1, y1, x2, y2 = map(int, t.tlbr)
        track_id = t.track_id
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"ID {track_id}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("MOT", frame)
    if writer:
        writer.write(frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
if writer:
    writer.release()
cv2.destroyAllWindows()
