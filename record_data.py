import os
import glob
import time
from PIL import Image
from capture_images import take_screenshot, PHONE_REGION

GIF_FRAMES_DIR = "gif_frames"
OUTPUT_GIF = "recording.gif"


def clear_frames():
    for f in glob.glob(os.path.join(GIF_FRAMES_DIR, "frame_*.png")):
        os.remove(f)


def compile_gif():
    paths = sorted(glob.glob(os.path.join(GIF_FRAMES_DIR, "frame_*.png")))
    if not paths:
        print("No frames to compile.")
        return
    frames = [Image.open(p) for p in paths]
    frames[0].save(
        OUTPUT_GIF,
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=500,
    )
    print(f"Saved {len(frames)}-frame GIF to {OUTPUT_GIF}")


if __name__ == "__main__":
    os.makedirs(GIF_FRAMES_DIR, exist_ok=True)
    clear_frames()
    time.sleep(5.0)

    print("Recording...")

    i = 0
    try:
        while True:
            ss = take_screenshot()
            frame = ss.crop(PHONE_REGION)
            frame.save(os.path.join(GIF_FRAMES_DIR, f"frame_{i:04d}.png"))
            i += 1
            print(f"  frame {i}", end="\r")
            time.sleep(1.0)
    except KeyboardInterrupt:
        print(f"\nStopped after {i} frame(s). Compiling GIF...")
        compile_gif()
