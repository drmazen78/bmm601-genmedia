"""
convert-images.py
-----------------
GenMedia (BMM601) — image build step.

Reads every PNG/JPG under public/assets/images, and writes a WEBP and an AVIF
sibling next to each one. Resizes anything wider than 1024px down to 1024px
keeping aspect ratio. Originals are NEVER deleted — they stay in place as
fallbacks for older browsers (and for inspection).

Run: python convert-images.py
"""

from pathlib import Path
import sys

from PIL import Image
import pillow_avif  # noqa: F401  (registers AVIF codec into Pillow on import)


PROJECT_ROOT = Path(__file__).resolve().parent
IMAGES_DIR = PROJECT_ROOT / "public" / "assets" / "images"
MAX_WIDTH = 1024
WEBP_QUALITY = 82
AVIF_QUALITY = 65
SOURCE_EXTS = {".png", ".jpg", ".jpeg"}


def kb(path: Path) -> float:
    return round(path.stat().st_size / 1024, 1)


def fit_width(img: Image.Image, max_w: int) -> Image.Image:
    if img.width <= max_w:
        return img
    new_h = round(img.height * max_w / img.width)
    return img.resize((max_w, new_h), Image.Resampling.LANCZOS)


def convert_one(src: Path) -> tuple[float, float, float] | None:
    """Returns (orig_kb, webp_kb, avif_kb) or None on failure."""
    try:
        with Image.open(src) as im:
            im.load()
            # Preserve alpha for PNGs that have it; JPGs are RGB anyway.
            if im.mode not in ("RGB", "RGBA"):
                im = im.convert("RGBA" if "A" in im.mode else "RGB")
            im = fit_width(im, MAX_WIDTH)

            webp_out = src.with_suffix(".webp")
            avif_out = src.with_suffix(".avif")

            im.save(webp_out, format="WEBP", quality=WEBP_QUALITY, method=6)
            im.save(avif_out, format="AVIF", quality=AVIF_QUALITY, speed=5)

        return kb(src), kb(webp_out), kb(avif_out)
    except Exception as e:
        print(f"  [error] {src.name}: {e}", file=sys.stderr)
        return None


def main() -> int:
    if not IMAGES_DIR.is_dir():
        print(f"Images folder not found: {IMAGES_DIR}", file=sys.stderr)
        return 1

    sources = sorted(p for p in IMAGES_DIR.iterdir()
                     if p.is_file() and p.suffix.lower() in SOURCE_EXTS)
    if not sources:
        print(f"No PNG/JPG files in {IMAGES_DIR}")
        return 1

    print(f"Converting {len(sources)} images from {IMAGES_DIR}\n")

    rows = []
    total_orig = total_webp = total_avif = 0.0
    fail = 0

    for src in sources:
        result = convert_one(src)
        if result is None:
            fail += 1
            continue
        o, w, a = result
        total_orig += o
        total_webp += w
        total_avif += a
        rows.append((src.name, o, w, a))

    # Summary table
    print()
    print(f"{'File':28} {'Orig KB':>9} {'WEBP KB':>9} {'AVIF KB':>9} {'Saved':>8}")
    print("-" * 68)
    for name, o, w, a in rows:
        best = min(w, a)
        saved_pct = round(100 * (1 - best / o), 1) if o else 0
        print(f"{name:28} {o:9.1f} {w:9.1f} {a:9.1f} {saved_pct:7.1f}%")
    print("-" * 68)
    if total_orig:
        best_total = min(total_webp, total_avif)
        total_saved = round(100 * (1 - best_total / total_orig), 1)
        print(f"{'TOTAL':28} {total_orig:9.1f} {total_webp:9.1f} {total_avif:9.1f} {total_saved:7.1f}%")
    if fail:
        print(f"\n{fail} file(s) failed — see errors above.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
