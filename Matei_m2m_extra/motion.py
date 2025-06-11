#!/usr/bin/env python3
"""
motion_snapshot.py – motion detection using periodic JPEG snapshots.

Run:
  python3 motion_snapshot.py [--debug] [--threshold N] [--min-area N] [--output-dir DIR]

Arguments
  --debug         show live windows with FPS and intermediate masks
  --threshold     pixel-intensity delta for motion (default 25)
  --min-area      ignore contours smaller than this area (default 5000 px)
  --output-dir    directory to store captured frames (default ./captures)
"""

import cv2
import time
import argparse
import os
import sys
import urllib.request
import numpy as np


SNAP_URL = "http://100.119.64.66:8081/?action=snapshot"   # <-- snapshot endpoint


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--debug", action="store_true",
                   help="display debug windows and FPS counter")
    p.add_argument("--threshold", type=int, default=25,
                   help="pixel delta threshold")
    p.add_argument("--min-area", type=int, default=5000,
                   help="minimum contour area to treat as motion")
    p.add_argument("--output-dir", type=str, default="./captures",
                   help="where to save motion frames")
    return p.parse_args()


def fetch_snapshot(url: str, timeout: float = 5.0):
    """Download one JPEG from the snapshot URL and decode it to a BGR image."""
    data = urllib.request.urlopen(url, timeout=timeout).read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    return img


def prune_old_photos(folder: str = "./captures", keep: int = 10) -> int:
    """
    Remove all but the newest <keep> .jpg files in <folder>.
    Returns the number of files remaining after cleanup.
    """
    photos_dir = Path(folder)
    if not photos_dir.exists():
        return 0

    # newest-first list of all JPEGs
    photos = sorted(photos_dir.glob("*.jpg"),
                    key=os.path.getmtime,
                    reverse=True)

    # delete everything after the first <keep> items
    for photo in photos[keep:]:
        try:
            photo.unlink()
        except OSError as e:
            print(f"Warning: could not delete {photo}: {e}")

    return len(list(photos_dir.glob("*.jpg")))


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    # ----- initial frame ----------------------------------------------------
    try:
        prev = fetch_snapshot(SNAP_URL)
        if prev is None:
            sys.exit("ERROR: Unable to decode first snapshot")
    except Exception as err:
        sys.exit(f"ERROR: Cannot fetch first snapshot – {err}")

    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

    # ----- main loop --------------------------------------------------------
    while True:
        start = time.time()
        try:
            frame = fetch_snapshot(SNAP_URL)
            if frame is None:
                print("ERROR: Unable to decode snapshot", file=sys.stderr)
                break
        except Exception as err:
            print(f"ERROR: Snapshot fetch failed – {err}", file=sys.stderr)
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # frame differencing
        delta = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(delta, args.threshold, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion = False
        for c in contours:
            if cv2.contourArea(c) < args.min_area:
                continue
            motion = True
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if motion:
            ts = time.strftime("%Y%m%d_%H%M%S")
            fname = os.path.join(args.output_dir, f"motion_{ts}.jpg")
            cv2.imwrite(fname, frame)
            print(f"[{ts}] Motion detected – saved {fname}")

        if args.debug:
            fps = 1.0 / max(time.time() - start, 1e-6)
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.imshow("Live", frame)
            cv2.imshow("Thresh", thresh)
            cv2.imshow("Delta", delta)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        prev_gray = gray

    if args.debug:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
