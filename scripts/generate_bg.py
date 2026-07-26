#!/usr/bin/env python3
"""
generate_bg.py — generate circuit-board background + 3-phase breathing animation mp4.

Animation matches reference (a_left_to_right_illumination_f.mp4) per vision analysis:
  Phase 1 (0-2s): Dormant — circuit small on left, crisp lines, white bg
  Phase 2 (2-8s): Expansion — lines start glowing, circuit expands left→full-width,
                  central bright spot emerges and peaks
  Phase 3 (8-10s): Contraction — circuit contracts back to small-left, glow fades
  Loops seamlessly (end state = start state).

Outputs:
    public/images/bg-circuit.png  — static full-width circuit (the source image)
    public/images/bg-circuit.mp4  — 10s breathing animation, loops seamlessly
"""
from __future__ import annotations
import os
import random
import math
import subprocess
from PIL import Image, ImageDraw, ImageFilter

# ─── Config ────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 2560, 1440
OUTPUT_DIR = r"C:/Users/zarat/Projects/portfolio-website-astro/public/images"
STATIC_PNG = os.path.join(OUTPUT_DIR, "bg-circuit.png")
VIDEO_MP4 = os.path.join(OUTPUT_DIR, "bg-circuit.mp4")
FRAMES_DIR = r"C:/Users/zarat/Projects/.zcode/mockups/bg-frames"

TOTAL_SECONDS = 10.0
FPS = 30

# Circuit aesthetics — INVERTED from earlier version.
# Reference: bright glowing traces on medium gray bg, dense in CENTER not left.
BG_COLOR = (160, 160, 160)          # medium gray background
TRACE_COLOR = (210, 210, 210)       # light gray traces (brighter than bg)
NODE_COLOR = (220, 220, 220)        # even lighter nodes
TRACE_WIDTH = 2
NODE_RADIUS = 4
SEED = 42

# Phase timing (in seconds, 0-10s loop)
T_DORMANT_END = 1.5     # Phase 1 end (dormant)
T_EXPAND_PEAK = 5.0     # Phase 2 peak (max expansion + glow)
T_CONTRACT_START = 7.0  # Phase 3 start (contraction begins)
# T=10s = T=0s (loop point)


def generate_circuit(width: int, height: int, seed: int) -> Image.Image:
    """Draw a circuit-board pattern with central-dense distribution.
    Reference: ~38% trace coverage overall, 70% in center sections, 5% at edges.
    Returns an RGB image (no transparency)."""
    random.seed(seed)
    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Finer grid + higher probability to reach 70% center density
    grid_step = 18  # finer grid for denser pattern
    nodes = []

    cx, cy = width / 2, height / 2
    max_dist = math.sqrt(cx**2 + cy**2)
    for y in range(grid_step // 2, height, grid_step):
        for x in range(grid_step // 2, width, grid_step):
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            dist_frac = dist / max_dist
            # Steeper falloff — center nearly saturated, edges sparse
            prob = max(0.02, 0.98 * (1 - dist_frac * 1.25))
            if random.random() < prob:
                jx = random.randint(-6, 6)
                jy = random.randint(-6, 6)
                nodes.append((x + jx, y + jy))

    # Draw MANY traces per node — reference has dense interconnects
    traces = 0
    for idx, (x1, y1) in enumerate(nodes):
        radius = random.randint(30, 80)
        candidates = [
            (nx, ny) for nx, ny in nodes
            if (nx, ny) != (x1, y1) and abs(nx - x1) <= radius and abs(ny - y1) <= radius
        ]
        # Connect to 3-5 of them (was 2-3)
        random.shuffle(candidates)
        for x2, y2 in candidates[:random.randint(3, 5)]:
            if random.random() < 0.5:
                draw.line([(x1, y1), (x2, y1), (x2, y2)], fill=TRACE_COLOR, width=TRACE_WIDTH)
            else:
                draw.line([(x1, y1), (x1, y2), (x2, y2)], fill=TRACE_COLOR, width=TRACE_WIDTH)
            traces += 1

    # Draw nodes on top
    for x, y in nodes:
        bbox = [x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS]
        draw.ellipse(bbox, fill=NODE_COLOR)
        if random.random() < 0.15:
            r2 = NODE_RADIUS + 3
            draw.ellipse([x - r2, y - r2, x + r2, y + r2], outline=NODE_COLOR, width=1)

    print(f"Generated circuit: {len(nodes)} nodes, {traces} traces")
    return img


def ease_in_out(t: float) -> float:
    """Smooth ease-in-out curve (0→1)."""
    if t < 0.5:
        return 4 * t * t * t
    return 1 - pow(-2 * t + 2, 3) / 2


def compute_expansion(t: float) -> float:
    """Return 0.0→1.0 indicating how expanded the circuit is at time t (0-10s).
    0 = dormant (small left), 1 = fully expanded (full width + glow).
    Matches the 3-phase breathing pattern."""
    if t < T_DORMANT_END:
        # Phase 1: dormant (low expansion, slight ease)
        return 0.05 + 0.05 * ease_in_out(t / T_DORMANT_END)
    elif t < T_EXPAND_PEAK:
        # Phase 2: expanding toward peak
        progress = (t - T_DORMANT_END) / (T_EXPAND_PEAK - T_DORMANT_END)
        return 0.10 + 0.90 * ease_in_out(progress)
    elif t < T_CONTRACT_START:
        # Hold at peak
        return 1.0
    else:
        # Phase 3: contracting back toward dormant
        progress = (t - T_CONTRACT_START) / (TOTAL_SECONDS - T_CONTRACT_START)
        return 1.0 - 0.95 * ease_in_out(progress)


def render_frame(circuit_img: Image.Image, t: float, white_bg: Image.Image) -> Image.Image:
    """Render a single frame of the animation at time t (0-10s).

    CURRENTLY PAUSED: effects disabled while we lock the circuit content.
    Returns the static circuit image for every frame so we can verify
    the pattern matches the reference screenshot before re-adding effects.
    """
    # TODO: re-enable breathing expansion, glow, central bright spot
    # once circuit content is verified matching.
    return circuit_img.copy()


def render_animation(circuit_img: Image.Image, output_mp4: str, frames_dir: str):
    """Render the full 10s breathing animation and encode to mp4."""
    os.makedirs(frames_dir, exist_ok=True)
    for f in os.listdir(frames_dir):
        if f.endswith(".png"):
            os.remove(os.path.join(frames_dir, f))

    width, height = circuit_img.size
    white_bg = Image.new("RGB", (width, height), (255, 255, 255))
    total_frames = int(TOTAL_SECONDS * FPS)

    print(f"Rendering {total_frames} frames ({TOTAL_SECONDS}s at {FPS}fps)...")
    for i in range(total_frames):
        t = i / FPS
        frame = render_frame(circuit_img, t, white_bg)
        out_path = os.path.join(frames_dir, f"frame_{i:05d}.png")
        frame.save(out_path)
        if i % 30 == 0:
            exp = compute_expansion(t)
            print(f"  frame {i}/{total_frames} (t={t:.1f}s, expansion={exp:.2f})")

    print(f"Encoding {output_mp4}...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%05d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "20",
        "-preset", "medium",
        "-movflags", "+faststart",
        output_mp4,
    ]
    subprocess.run(cmd, check=True)
    size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    print(f"Encoded: {output_mp4} ({size_mb:.2f} MB)")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=== Step 1: Generate circuit image ===")
    circuit = generate_circuit(WIDTH, HEIGHT, SEED)
    circuit.save(STATIC_PNG)
    print(f"Saved {STATIC_PNG} ({os.path.getsize(STATIC_PNG) // 1024} KB)")

    print("\n=== Step 2: Render breathing animation ===")
    render_animation(circuit, VIDEO_MP4, FRAMES_DIR)
    print("\nDone.")


if __name__ == "__main__":
    main()
