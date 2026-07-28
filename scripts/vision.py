#!/usr/bin/env python3
"""
vision.py — thin wrapper around the ollama vision proxy (port 8787).

Usage:
    python vision.py <image_path> "<prompt>"
    python vision.py <image_path> "<prompt>" --model qwen3-vl:32b

Reads the image, base64-encodes it, sends to the proxy's OpenAI-compatible
endpoint, prints the model's response.

Exits non-zero on failure. Designed to be called from any agent/shell.
"""
import base64
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

PROXY_URL = "http://localhost:8787/v1/chat/completions"
DEFAULT_MODEL = "gemma4:latest"
TIMEOUT = 90  # seconds — gemma4 can be slow on vision tasks


def describe(image_path: str, prompt: str, model: str = DEFAULT_MODEL) -> str:
    p = Path(image_path)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    img_b64 = base64.b64encode(p.read_bytes()).decode()
    # Guess mime from extension
    ext = p.suffix.lower()
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "image/png")

    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{img_b64}"}},
            ],
        }],
        "stream": False,
        # gemma4 needs 400+ tokens on vision tasks; 256 produced empty content.
        "max_tokens": 1024,
        # gemma4 burns its budget on hidden reasoning and returns empty content
        # unless thinking is disabled. Force it off per proxy docs.
        "options": {"think": False},
    }

    req = urllib.request.Request(
        PROXY_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"HTTP {e.code}: {body[:500]}") from e

    msg = (
        result.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )
    return msg.strip()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python vision.py <image_path> '<prompt>' [--model NAME]")
        sys.exit(2)

    image_path = sys.argv[1]
    prompt = sys.argv[2]
    model = DEFAULT_MODEL
    if "--model" in sys.argv:
        idx = sys.argv.index("--model")
        model = sys.argv[idx + 1]

    try:
        out = describe(image_path, prompt, model)
        print(out)
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)
