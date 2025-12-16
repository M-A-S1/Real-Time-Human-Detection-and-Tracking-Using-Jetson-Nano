#!/usr/bin/env python3
import cv2
import argparse
import json
import sys

POINTS_FILE = "zone_points.json"
PREVIEW_IMAGE = "zone_preview.jpg"

WINDOW_SIZE = (416, 416)   # <--- NEW SIZE

points = []

def click_event(event, x, y, flags, param):
    global points
    frame_for_display = param

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((int(x), int(y)))
            print(f"Point {len(points)}: {(int(x), int(y))}")

            cv2.circle(frame_for_display, (int(x), int(y)), 5, (0,255,255), -1)
            cv2.imshow("Select 4 Points", frame_for_display)

        if len(points) == 4:
            print("\n✔ 4 points selected (TL, TR, BR, BL):")
            for i, p in enumerate(points, 1):
                print(f"{i}: {p}")

            # Save JSON
            try:
                with open(POINTS_FILE, "w") as f:
                    json.dump(points, f)
                print(f"✔ Saved to '{POINTS_FILE}'")
            except Exception as e:
                print("❌ JSON save error:", e)

            # Save preview
            try:
                cv2.imwrite(PREVIEW_IMAGE, frame_for_display)
                print(f"✔ Saved preview '{PREVIEW_IMAGE}'")
            except Exception as e:
                print("❌ Preview save error:", e)

            cv2.waitKey(500)
            cv2.destroyAllWindows()
            sys.exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--i", dest="input_uri", required=True,
                        help="Input stream (IP camera, USB, file)")
    parser.add_argument("-m", action="store_true")
    parser.add_argument("-s", action="store_true")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.input_uri)
    if not cap.isOpened():
        print("❌ Cannot open stream:", args.input_uri)
        return

    ret, frame = cap.read()
    if not ret:
        print("❌ Cannot read frame from stream.")
        return

    # Resize first frame to WINDOW_SIZE
    frame = cv2.resize(frame, WINDOW_SIZE)

    window_name = "Select 4 Points"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    display_frame = frame.copy()
    cv2.setMouseCallback(window_name, click_event, display_frame)
    cv2.imshow(window_name, display_frame)

    print("\n🎯 Click FOUR points in this order:")
    print("1) Top-Left")
    print("2) Top-Right")
    print("3) Bottom-Right")
    print("4) Bottom-Left")
    print("\nPress ESC or 'q' to exit without saving.\n")

    # Continuously update live feed
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠ No more frames.")
            break

        # Resize every frame to 416×416
        frame = cv2.resize(frame, WINDOW_SIZE)

        # Keep the displayed frame updated
        display_frame[:] = frame

        # redraw previous clicked points
        for p in points:
            cv2.circle(display_frame, p, 5, (0,255,255), -1)

        cv2.imshow(window_name, display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key in [27, ord('q')]:  # ESC or q
            print("❌ Exiting without saving.")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
