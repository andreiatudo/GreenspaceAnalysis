from PIL import Image
import argparse, sys
from pathlib import Path

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

def split_image_into_patches(image_path: Path, patch_size=(1920, 1080), output_dir: Path = Path("patches"), prefix="patch", ext="png"):
    pw, ph = patch_size
    image = Image.open(image_path).convert("RGB")
    iw, ih = image.size
    output_dir.mkdir(parents=True, exist_ok=True)

    patch_id = 0
    for top in range(0, ih, ph):
        for left in range(0, iw, pw):
            right = min(left + pw, iw)
            bottom = min(top + ph, ih)

            patch = image.crop((left, top, right, bottom))

            if patch.size != (pw, ph):
                padded = Image.new("RGB", (pw, ph))
                padded.paste(patch, (0, 0))
                patch = padded

            out_path = output_dir / f"{prefix}_{patch_id}_{top}_{left}.{ext}"
            patch.save(out_path)
            patch_id += 1

    print(f"{image_path.name}: saved {patch_id} patches to '{output_dir}' ({pw}x{ph}).")

def main():
    ap = argparse.ArgumentParser(description="Split a single image or all images under a folder into fixed-size patches.")
    ap.add_argument("--input", required=True, help="Path to an image file or a folder of images.")
    ap.add_argument("--patch-width", type=int, default=1920, help="Patch width in pixels.")
    ap.add_argument("--patch-height", type=int, default=1080, help="Patch height in pixels.")
    ap.add_argument("--output-dir", default="patches", help="Directory to store patches.")
    ap.add_argument("--prefix", default="patch", help="Filename prefix for patches.")
    ap.add_argument("--ext", default="png", choices=["png", "jpg", "jpeg"], help="Output image format.")
    ap.add_argument("--per-image-subfolders", action="store_true", help="If input is a folder, create a subfolder per image.")
    args = ap.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print(f"Input not found: {inp}")
        sys.exit(2)

    patch_size = (args.patch_width, args.patch_height)
    out_root = Path(args.output_dir)

    if inp.is_file():
        split_image_into_patches(inp, patch_size=patch_size, output_dir=out_root, prefix=args.prefix, ext=args.ext)
    elif inp.is_dir():
        imgs = sorted([p for p in inp.rglob("*") if p.suffix.lower() in IMG_EXTS])
        if not imgs:
            print("No images found in the input folder.")
            sys.exit(1)
        for img in imgs:
            outdir = out_root / img.stem if args.per_image_subfolders else out_root
            split_image_into_patches(img, patch_size=patch_size, output_dir=outdir, prefix=args.prefix, ext=args.ext)
    else:
        print(f"Unsupported input path: {inp}")
        sys.exit(2)

if __name__ == "__main__":
    main()
