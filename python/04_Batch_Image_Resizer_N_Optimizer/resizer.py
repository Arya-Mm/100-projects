import argparse
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont, PngImagePlugin
from tqdm import tqdm
import io
import os
import logging
import concurrent.futures
import piexif  # for safe EXIF handling (install via pip install piexif)


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".bmp", ".gif"}

logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s -- %(levelname)s -- %(message)s"
)

def parse_args():
    p = argparse.ArgumentParser(description="Advanced Image Resizer & Optimizer")
    p.add_argument("-i", "--input", required=True)
    p.add_argument("-o", "--output", required=True)

    p.add_argument("--width", type=int)
    p.add_argument("--height", type=int)

    p.add_argument("--quality", type=int, default=85)
    p.add_argument("--watermark", type=str, default=None)
    p.add_argument("--preserve-exif", action="store_true")
    p.add_argument("--recursive", action="store_true")
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--overwrite", action="store_true")

    p.add_argument("--format", type=str, choices=["jpg", "jpeg", "png", "webp"],
                  help="Force output format")

    return p.parse_args()

def gather_images(root: Path, recursive: bool):
    if recursive:
        return [p for p in root.rglob("*") if p.suffix.lower() in IMAGE_EXTS]
    return [p for p in root.iterdir() if p.suffix.lower() in IMAGE_EXTS]

def resize_image(im: Image.Image, target_w, target_h):
    if not target_w and not target_h:
        return im

    if target_w and not target_h:
        scale = target_w / im.width
        target_h = int(im.height * scale)
    elif target_h and not target_w:
        scale = target_h / im.height
        target_w = int(im.width * scale)

    img = im.copy()
    img.thumbnail((target_w, target_h), Image.LANCZOS)
    return img

def apply_watermark(im, text):
    if not text:
        return im

    if im.mode != "RGBA":
        base = im.convert("RGBA")
    else:
        base = im.copy()

    txt_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    fontsize = max(16, base.size[0] // 30)
    try:
        font = ImageFont.truetype("arial.ttf", fontsize)
    except:
        font = ImageFont.load_default()

    tw, th = draw.textsize(text, font=font)

    x = base.width - tw - 20
    y = base.height - th - 20

    draw.rectangle((x - 5, y - 5, x + tw + 5, y + th + 5), fill=(0, 0, 0, 128))
    draw.text((x, y), text, fill=(255, 255, 255, 200), font=font)

    return Image.alpha_composite(base, txt_layer).convert(im.mode)

def process_one(job):
    src, root_in, root_out, options = job

    rel = src.relative_to(root_in)
    ext = options["format"] if options["format"] else src.suffix[1:]
    dst = (root_out / rel).with_suffix("." + ext)

    dst.parent.mkdir(parents=True, exist_ok=True)

    if dst.exists() and not options["overwrite"]:
        return False, "exists"

    try:
        with Image.open(src) as im:
            # Fix orientation
            im = ImageOps.exif_transpose(im)

            # Extract EXIF safely
            exif_original = None
            if options["preserve_exif"] and "exif" in im.info:
                exif_original = im.info["exif"]

            # Extract PNG metadata if PNG
            png_info = None
            if src.suffix.lower() == ".png":
                png_info = im.info  # preserves ICC profile, gamma, etc

            # Resize
            im2 = resize_image(im, options["width"], options["height"])

            # Watermark
            if options["watermark"]:
                im2 = apply_watermark(im2, options["watermark"])

            # Save safely
            buffer = io.BytesIO()

            save_params = {}
            if ext.lower() in ["jpg", "jpeg"]:
                save_params.update({
                    "format": "JPEG",
                    "quality": options["quality"],
                    "optimize": True,
                })
                if exif_original:
                    save_params["exif"] = exif_original

            elif ext.lower() == "png":
                save_params["format"] = "PNG"
                if png_info:
                    save_params["pnginfo"] = PngImagePlugin.PngInfo()

            elif ext.lower() == "webp":
                save_params.update({
                    "format": "WEBP",
                    "quality": options["quality"],
                })
            else:
                save_params["format"] = ext.upper()

            im2.save(buffer, **save_params)

            buffer.seek(0)
            with open(dst, "wb") as f:
                f.write(buffer.read())

        # Copy timestamps
        st = src.stat()
        os.utime(dst, (st.st_atime, st.st_mtime))

        return True, None

    except Exception as e:
        logging.error(f"{src} → ERROR: {e}")
        return False, str(e)
def main():
    args = parse_args()

    root_in = Path(args.input).resolve()
    root_out = Path(args.output).resolve()
    root_out.mkdir(parents=True, exist_ok=True)

    files = gather_images(root_in, args.recursive)
    if not files:
        print("No images found.")
        return

    options = {
        "width": args.width,
        "height": args.height,
        "quality": args.quality,
        "watermark": args.watermark,
        "preserve_exif": args.preserve_exif,
        "format": args.format,
        "overwrite": args.overwrite
    }

    jobs = [(f, root_in, root_out, options) for f in files]

    if args.workers > 1:
        with concurrent.futures.ThreadPoolExecutor(args.workers) as ex:
            results = list(tqdm(ex.map(process_one, jobs), total=len(jobs)))
    else:
        results = []
        for j in tqdm(jobs):
            results.append(process_one(j))

    success = sum(1 for r,_ in results if r)
    failed  = sum(1 for r,_ in results if not r)

    print("\nCompleted.")
    print(f"✔ Success: {success}")
    print(f"✖ Failed: {failed}")
    print("→ See errors.log for details")


if __name__ == "__main__":
    main()
