#!/usr/bin/env python3

from pathlib import Path
from types import SimpleNamespace
import argparse
import logging
import json
import cv2
import time
import numpy as np
import fastmot
import fastmot.models
from fastmot.utils import ConfigDecoder, Profiler

# ==============================================================
# FLOOR-ALIGNED ZONE (USER-SELECTED POINTS)
# ==============================================================
POINTS_FILE = "zone_points.json"

# Load 4 polygon points from JSON
try:
    with open(POINTS_FILE, "r") as f:
        pts_list = json.load(f)

    if len(pts_list) != 4:
        raise ValueError("zone_points.json must contain exactly 4 points.")

    ZONE = np.array(pts_list, dtype=np.int32)

    print("✔ Loaded ZONE points from JSON:", ZONE)

except Exception as e:
    print("❌ ERROR loading zone_points.json:", e)
    print("   Using fallback default zone (should be avoided!)")

    # Fallback only to avoid crash (you can remove fallback)
    ZONE = np.array([
        (164, 339),
        (130, 323),
        (180, 297),
        (210, 312)
    ], dtype=np.int32)


def draw_zone(frame):
    """
    Draws the danger zone as a floor-aligned polygon using the user-selected points.
    """
    pts = ZONE.reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 255), thickness=3)

    # Put "DANGER" text near the center of the polygon
    cx = int(np.mean(ZONE[:, 0]))
    cy = int(np.mean(ZONE[:, 1]))
    cv2.putText(frame, "DANGER",
                (cx - 40, cy),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (0, 255, 255), 2)

def point_in_polygon(point):
    """
    Returns True if point is inside the ZONE polygon.
    """
    poly = ZONE.astype(np.int32)
    inside = cv2.pointPolygonTest(poly, point, False)
    return inside >= 0

def draw_message_box(frame, message, counts, color):
    box_x1, box_y1, box_x2, box_y2 = 20, 20, 600, 70
    overlay = frame.copy()
    cv2.rectangle(overlay, (box_x1, box_y1), (box_x2, box_y2), color, -1)
    alpha = 0.6
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    cv2.putText(frame, message, (box_x1 + 10, box_y1 + 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255, 255, 255), 2)
    counts_text = f"Safe: {counts['safe']} | Danger: {counts['danger']}"
    cv2.putText(frame, counts_text, (box_x1 + 10, box_y1 + 55),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255, 255, 255), 1)

# ==============================================================
# MAIN PROGRAM
# ==============================================================

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    optional = parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    group = parser.add_mutually_exclusive_group()

    required.add_argument('-i', '--input-uri', required=True)
    optional.add_argument('-c', '--config',
                          default=Path(__file__).parent / 'cfg' / 'mot.json')
    optional.add_argument('-l', '--labels')
    optional.add_argument('-o', '--output-uri')
    optional.add_argument('-t', '--txt')
    optional.add_argument('-m', '--mot', action='store_true')
    optional.add_argument('-s', '--show', action='store_true')
    group.add_argument('-q', '--quiet', action='store_true')
    group.add_argument('-v', '--verbose', action='store_true')
    parser._action_groups.append(optional)
    args = parser.parse_args()

    # Logging
    logging.basicConfig(format='%(asctime)s [%(levelname)8s] %(message)s')
    logger = logging.getLogger(fastmot.__name__)
    logger.setLevel(logging.INFO if not args.verbose else logging.DEBUG)

    # Load config
    with open(args.config) as cfg_file:
        config = json.load(cfg_file, cls=ConfigDecoder,
                           object_hook=lambda d: SimpleNamespace(**d))

    # Labels
    if args.labels:
        with open(args.labels) as f:
            fastmot.models.set_label_map(f.read().splitlines())

    # Video I/O
    stream = fastmot.VideoIO(config.resize_to, args.input_uri,
                             args.output_uri, **vars(config.stream_cfg))

    mot = None
    txt = None
    if args.mot:
        mot = fastmot.MOT(config.resize_to, **vars(config.mot_cfg),
                          draw=(args.show or args.output_uri is not None))
        mot.reset(stream.cap_dt)

    if args.txt:
        Path(args.txt).parent.mkdir(parents=True, exist_ok=True)
        txt = open(args.txt, 'w')

    if args.show:
        cv2.namedWindow('Video', cv2.WINDOW_AUTOSIZE)

    logger.info("Starting video capture...")
    stream.start_capture()

    try:
        with Profiler('app') as prof:
            frame_counter = 0
            fps = 0
            last_time = time.time()

            while not args.show or cv2.getWindowProperty('Video', 0) >= 0:
                frame = stream.read()
                if frame is None:
                    break

                # FPS
                frame_counter += 1
                now = time.time()
                if now - last_time >= 1:
                    fps = frame_counter
                    frame_counter = 0
                    last_time = now

                # Tracking
                if args.mot:
                    mot.step(frame)

                # Draw the floor-aligned danger zone
                draw_zone(frame)

                # Count
                safe_count = 0
                danger_count = 0

                # Track-based zone logic
                if args.mot:
                    for track in mot.visible_tracks():
                        x1, y1, x2, y2 = track.tlbr.astype(int)

                        # FEET POINT (bottom middle)
                        fx = int((x1 + x2) / 2)
                        fy = int(y2)
                        feet = (fx, fy)

                        # Draw feet debugging point
                        cv2.circle(frame, feet, 4, (255, 0, 0), -1)

                        # Check floor polygon zone
                        in_zone = point_in_polygon(feet)

                        if in_zone:
                            danger_count += 1
                            color = (0, 0, 255)
                        else:
                            safe_count += 1
                            color = (0, 255, 0)

                        # Draw bounding box
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

                # Alarm / message
                counts = {"safe": safe_count, "danger": danger_count}
                if danger_count > 0:
                    draw_message_box(frame,
                                     f"DANGER ALERT: {danger_count} person(s)",
                                     counts,
                                     (0, 0, 255))

                # FPS Display
                cv2.putText(frame, f"FPS: {fps}",
                            (frame.shape[1] - 150, frame.shape[0] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (255, 255, 255), 2)

                if args.show:
                    cv2.imshow('Video', frame)
                    if cv2.waitKey(1) & 0xFF == 27:
                        break

                if args.output_uri:
                    stream.write(frame)

    finally:
        if txt: txt.close()
        stream.release()
        cv2.destroyAllWindows()

    # Stats
    if args.mot:
        avg_fps = round(mot.frame_count / prof.duration)
        logger.info("Average FPS: %d", avg_fps)
        mot.print_timing_info()

if __name__ == "__main__":
    main()
