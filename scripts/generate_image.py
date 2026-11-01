#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate images using Foxtrai AI Drawing API.

Usage:
    uv run generate_image.py --prompt "your image description" --filename "output.png" [--resolution 1K|2K|4K] [--model nano-banana-pro]
"""

import argparse
import hashlib
import os
import sys
import time
from pathlib import Path

import httpx
from PIL import Image as PILImage


def load_env_from_skill():
    """Load .env file from skill's config folder."""
    script_dir = Path(__file__).parent
    env_path = script_dir.parent / "config" / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


# Auto-load config from skill folder
load_env_from_skill()


def get_api_key() -> str | None:
    return os.environ.get("FOXTRAI_API_KEY")


def get_base_url() -> str:
    return os.environ.get("FOXTRAI_BASE_URL", "https://www.foxtrai.com/api/generate")


def get_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
    }


def upload_image(client: httpx.Client, base_url: str, headers: dict, image_path: str) -> str | None:
    """Upload an image and return the asset_id."""
    img = PILImage.open(image_path)
    width, height = img.size
    
    with open(image_path, "rb") as f:
        file_bytes = f.read()
    
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    file_size = len(file_bytes)
    filename = Path(image_path).name
    
    suffix = Path(image_path).suffix.lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    mime_type = mime_map.get(suffix, "image/png")
    
    print(f"Uploading image: {filename} ({width}x{height}, {file_size} bytes)")
    
    upload_req = {
        "filename": filename,
        "mime_type": mime_type,
        "size": file_size,
        "hash": file_hash,
        "width": width,
        "height": height,
    }
    
    resp = client.post(f"{base_url}/image/upload", json=upload_req, headers=headers)
    if resp.status_code != 200:
        print(f"Upload auth failed: {resp.status_code} {resp.text}", file=sys.stderr)
        return None
    
    data = resp.json().get("data", {})
    asset_id = data.get("asset_id")
    upload_url = data.get("upload_url")
    is_hit = data.get("is_hit", False)
    
    if is_hit:
        print(f"Image already exists (cache hit), asset_id: {asset_id}")
        return asset_id
    
    if upload_url:
        print(f"Uploading to cloud storage...")
        put_headers = {"Content-Type": mime_type}
        put_resp = client.put(upload_url, content=file_bytes, headers=put_headers, timeout=60)
        if put_resp.status_code not in (200, 201):
            print(f"File upload failed: {put_resp.status_code}", file=sys.stderr)
            return None
        
        time.sleep(1)
        check_resp = client.get(f"{base_url}/image", params={"asset_id": asset_id}, headers=headers)
        if check_resp.status_code != 200:
            print(f"Upload verification failed: {check_resp.status_code}", file=sys.stderr)
            return None
        
        print(f"Upload successful, asset_id: {asset_id}")
    
    return asset_id


def create_task(client: httpx.Client, base_url: str, headers: dict, 
                prompt: str, model: str, resolution: str, 
                input_asset_ids: list[str] | None = None,
                aspect_ratio: str = "16:9") -> str | None:
    """Create a drawing task and return the task_id."""
    task_req = {
        "prompt": prompt,
        "model": model,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
    }
    
    if input_asset_ids:
        task_req["input_asset_ids"] = input_asset_ids
    
    print(f"Creating task with model: {model}, resolution: {resolution}")
    
    resp = client.post(f"{base_url}/image/task/create", json=task_req, headers=headers, timeout=30)
    if resp.status_code != 200:
        print(f"Task creation failed: {resp.status_code} {resp.text}", file=sys.stderr)
        return None
    
    data = resp.json().get("data", {})
    task_id = data.get("task_id")
    print(f"Task created: {task_id}")
    return task_id


def poll_task(client: httpx.Client, base_url: str, headers: dict, 
              task_id: str, max_wait: int = 300) -> dict | None:
    """Poll task status until completion."""
    start_time = time.time()
    poll_interval = 3
    
    while time.time() - start_time < max_wait:
        resp = client.get(f"{base_url}/image/task", params={"task_id": task_id}, headers=headers)
        if resp.status_code != 200:
            print(f"Poll failed: {resp.status_code}", file=sys.stderr)
            time.sleep(poll_interval)
            continue
        
        data = resp.json().get("data", resp.json())
        status = data.get("status", "unknown")
        progress = data.get("progress", 0)
        
        print(f"  Status: {status}, Progress: {progress}%", end="\r")
        
        if status == "success":
            print(f"\nTask completed successfully!")
            return data
        elif status == "failed":
            error_msg = data.get("error_msg", "Unknown error")
            print(f"\nTask failed: {error_msg}", file=sys.stderr)
            return None
        
        time.sleep(poll_interval)
    
    print(f"\nTask timed out after {max_wait} seconds", file=sys.stderr)
    return None


def download_image(client: httpx.Client, url: str, output_path: Path) -> bool:
    """Download the generated image with fallback methods."""
    print(f"Downloading result image...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Try httpx first
    try:
        resp = client.get(url, timeout=60, follow_redirects=True)
        if resp.status_code == 200:
            output_path.write_bytes(resp.content)
            return True
        print(f"httpx download failed: {resp.status_code}")
    except Exception as e:
        print(f"httpx download error: {e}")
    
    # Fallback to urllib (no proxy)
    print("Trying fallback download method...")
    try:
        import urllib.request
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            output_path.write_bytes(resp.read())
        return True
    except Exception as e:
        print(f"Fallback download error: {e}", file=sys.stderr)
    
    # Print URL for manual download
    print(f"\nAuto-download failed. Please download manually:")
    print(f"URL: {url}")
    print(f"Save to: {output_path}")
    return False


def main():
    parser = argparse.ArgumentParser(description="Generate images using Foxtrai AI Drawing API")
    parser.add_argument("--prompt", "-p", required=True, help="Image description/prompt")
    parser.add_argument("--filename", "-f", required=True, help="Output filename")
    parser.add_argument("--input-image", "-i", help="Optional input/reference image path")
    parser.add_argument("--resolution", "-r", choices=["1K", "2K", "4K"], default="2K", help="Output resolution")
    parser.add_argument("--model", "-m", default="nano-banana-pro", help="Model name")
    parser.add_argument("--aspect-ratio", "-a", default="16:9", help="Aspect ratio (e.g., 16:9, 1:1, 4:3)")
    
    args = parser.parse_args()
    
    api_key = get_api_key()
    if not api_key:
        print("Error: FOXTRAI_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    
    base_url = get_base_url()
    headers = get_headers(api_key)
    output_path = Path(args.filename)
    
    print(f"Using API: {base_url}")
    print(f"Model: {args.model}, Resolution: {args.resolution}")
    
    with httpx.Client(timeout=30) as client:
        input_asset_ids = []
        if args.input_image:
            asset_id = upload_image(client, base_url, headers, args.input_image)
            if asset_id:
                input_asset_ids.append(asset_id)
            else:
                print("Warning: Failed to upload reference image, proceeding without it")
        
        task_id = create_task(
            client, base_url, headers,
            prompt=args.prompt,
            model=args.model,
            resolution=args.resolution,
            input_asset_ids=input_asset_ids if input_asset_ids else None,
            aspect_ratio=args.aspect_ratio
        )
        
        if not task_id:
            sys.exit(1)
        
        result = poll_task(client, base_url, headers, task_id)
        if not result:
            sys.exit(1)
        
        outputs = result.get("edges", {}).get("outputs", [])
        if not outputs:
            print("Error: No output image in result", file=sys.stderr)
            sys.exit(1)
        
        image_url = outputs[0].get("url") or outputs[0].get("path")
        if not image_url:
            print("Error: No image URL in output", file=sys.stderr)
            print(f"Output data: {outputs[0]}", file=sys.stderr)
            sys.exit(1)
        
        if download_image(client, image_url, output_path):
            print(f"\nImage saved: {output_path.resolve()}")
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
