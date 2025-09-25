import argparse, zipfile, shutil, sys
from pathlib import Path

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

def count_images(p: Path) -> int:
    return sum(1 for x in p.rglob("*") if x.suffix.lower() in IMG_EXTS)

def find_dataset_root(base: Path) -> Path:
    candidates = [base] + [d for d in base.rglob("*") if d.is_dir()]
    for d in candidates:
        if (d / "images").exists() or (d / "labels").exists():
            return d
    return base

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zip_path", nargs="?", help="Path to dataset zip (positional fallback)")
    ap.add_argument("--zip", dest="zip_opt", help="Path to dataset zip")
    ap.add_argument("--outdir", default=".", help="Extraction directory")
    ap.add_argument("--force", action="store_true", help="Remove destination if it exists")
    args = ap.parse_args()

    zip_arg = args.zip_opt or args.zip_path
    if not zip_arg:
        print("Missing ZIP path. Use: python setup_roboflow.py ZIP or --zip ZIP")
        sys.exit(2)

    zip_path = Path(zip_arg)
    outdir = Path(args.outdir)
    if not zip_path.exists():
        print(f"Zip not found: {zip_path}")
        sys.exit(1)

    outdir.mkdir(parents=True, exist_ok=True)
    extract_root = outdir / zip_path.stem
    if extract_root.exists() and args.force:
        print(f"Removing existing: {extract_root}")
        shutil.rmtree(extract_root)
    elif extract_root.exists():
        print(f"Destination exists: {extract_root}")
    print(f"Extracting to: {extract_root}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(extract_root)

    ds_root = find_dataset_root(extract_root)
    print(f"Dataset root: {ds_root}")
    for split in ["train", "val", "test"]:
        img_dir = ds_root / "images" / split
        if img_dir.exists():
            print(f"{split} images: {count_images(img_dir)} at {img_dir}")
    print("Done")

if __name__ == "__main__":
    main()
