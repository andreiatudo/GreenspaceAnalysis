from PIL import Image
import argparse, sys, re
from pathlib import Path

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

def merge_patches(patch_dir: Path, output_path: Path, patch_size=None, prefix="patch"):
    files = [p for p in patch_dir.iterdir() if p.is_file() and p.suffix.lower() in IMG_EXTS]
    if not files:
        print("No patch files found in the given directory.")
        sys.exit(1)

    # Expect filenames like: patch_<id>_<top>_<left>.<ext>
    pattern = re.compile(rf"{re.escape(prefix)}_\d+_(\d+)_(\d+)", re.IGNORECASE)
    coords = []
    for fp in files:
        m = pattern.search(fp.stem)
        if m:
            top = int(m.group(1))
            left = int(m.group(2))
            coords.append((top, left, fp))

    if not coords:
        print("No valid patch filenames found (expected 'patch_<id>_<top>_<left>.<ext>').")
        sys.exit(1)

    # Determine patch size: provided or infer from the first patch
    if patch_size is None:
        with Image.open(coords[0][2]) as im0:
            pw, ph = im0.size
    else:
        pw, ph = patch_size

    max_right = max(left for _, left, _ in coords) + pw
    max_bottom = max(top for top, _, _ in coords) + ph

    canvas = Image.new("RGB", (max_right, max_bottom))
    for top, left, fp in coords:
        with Image.open(fp) as patch:
            canvas.paste(patch.convert("RGB"), (left, top))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path)
    print(f"Reconstructed image saved: {output_path} (size {canvas.size[0]}x{canvas.size[1]}, from {len(coords)} patches)")

def main():
    ap = argparse.ArgumentParser(description="Reconstruct an image from patches named 'patch_<id>_<top>_<left>.<ext>'.")
    ap.add_argument("--patch-dir", required=True, help="Folder containing patches.")
    ap.add_argument("--output", default="reconstructed.png", help="Output image path.")
    ap.add_argument("--patch-width", type=int, default=None, help="Patch width (optional). If omitted, inferred from the first patch.")
    ap.add_argument("--patch-height", type=int, default=None, help="Patch height (optional). If omitted, inferred from the first patch.")
    ap.add_argument("--prefix", default="patch", help="Filename prefix used when splitting.")
    args = ap.parse_args()

    pdir = Path(args.patch_dir)
    if not pdir.exists() or not pdir.is_dir():
        print(f"Patch directory not found: {pdir}")
        sys.exit(2)

    psize = (args.patch_width, args.patch_height) if (args.patch_width and args.patch_height) else None
    merge_patches(pdir, output_path=Path(args.output), patch_size=psize, prefix=args.prefix)

if __name__ == "__main__":
    main()
