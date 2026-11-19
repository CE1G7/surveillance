"""Streams images and/or videos from a folder to the edge RTMP server.

Files are played in alphabetical order:
  * images are held on screen for --seconds
  * videos (mp4, avi, mov, mkv, ...) are played at real-time speed

All frames are resized to --width x --height and pushed at --fps, so the
server sees one continuous video stream across all files.
"""
import argparse
import shutil
import subprocess
import time
from itertools import cycle
from pathlib import Path

import cv2

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".m4v", ".flv"}


def ffmpeg_exe() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    # Fallback: pip-bundled static ffmpeg binary.
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def list_media(folder: Path) -> list[Path]:
    paths = sorted(p for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTS | VIDEO_EXTS)
    if not paths:
        raise SystemExit(f"No images or videos found in {folder}")
    return paths


def image_frames(path: Path, width: int, height: int, count: int):
    img = cv2.imread(str(path))
    if img is None:
        print(f"skipping unreadable image: {path.name}")
        return
    data = cv2.resize(img, (width, height)).tobytes()
    for _ in range(count):
        yield data


def video_frames(path: Path, width: int, height: int, fps: int):
    """Yields frames resampled from the video's own frame rate to `fps`,
    so playback runs at real-time speed regardless of the source rate."""
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        print(f"skipping unreadable video: {path.name}")
        return
    src_fps = cap.get(cv2.CAP_PROP_FPS) or fps
    if src_fps <= 0 or src_fps > 240:
        src_fps = fps
    step = src_fps / fps  # source frames per output frame
    src_index = -1        # index of the last source frame read
    frame = None
    out_index = 0
    try:
        while True:
            target = int(out_index * step)
            # Read forward until we reach the source frame for this output frame
            # (skips frames if the source is faster, repeats if slower).
            while src_index < target:
                ok, f = cap.read()
                if not ok:
                    return
                frame = f
                src_index += 1
            yield cv2.resize(frame, (width, height)).tobytes()
            out_index += 1
    finally:
        cap.release()


def start_ffmpeg(url: str, width: int, height: int, fps: int) -> subprocess.Popen:
    cmd = [
        ffmpeg_exe(), "-loglevel", "warning",
        # Raw BGR frames from stdin.
        "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{width}x{height}", "-r", str(fps), "-i", "-",
        "-c:v", "libx264", "-preset", "veryfast", "-tune", "zerolatency",
        "-pix_fmt", "yuv420p", "-g", str(fps),
        "-f", "flv", url,
    ]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", type=Path, help="folder containing images and/or videos")
    parser.add_argument("--url", default="rtmp://localhost:1935/live/stream")
    parser.add_argument("--seconds", type=float, default=2.0, help="time each image is shown")
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--width", type=int, default=1280)
    parser.add_argument("--height", type=int, default=720)
    parser.add_argument("--loop", action="store_true", help="repeat the folder forever")
    args = parser.parse_args()

    media = list_media(args.folder)
    frames_per_image = max(1, round(args.seconds * args.fps))
    frame_interval = 1.0 / args.fps

    proc = start_ffmpeg(args.url, args.width, args.height, args.fps)
    print(f"streaming {len(media)} files to {args.url}")
    try:
        next_frame = time.monotonic()
        for path in (cycle(media) if args.loop else media):
            print(f"sending {path.name}")
            if path.suffix.lower() in VIDEO_EXTS:
                frames = video_frames(path, args.width, args.height, args.fps)
            else:
                frames = image_frames(path, args.width, args.height, frames_per_image)
            for data in frames:
                proc.stdin.write(data)
                # Pace output in real time so the server receives a live stream.
                next_frame += frame_interval
                time.sleep(max(0.0, next_frame - time.monotonic()))
    except (BrokenPipeError, KeyboardInterrupt):
        pass
    finally:
        try:
            proc.stdin.close()
        except BrokenPipeError:
            pass
        proc.wait()


if __name__ == "__main__":
    main()
