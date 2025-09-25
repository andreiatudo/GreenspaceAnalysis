import argparse, time
from pathlib import Path
from ultralytics import YOLO

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}

def expand_sources(srcs):
    paths = []
    for s in srcs:
        p = Path(s)
        if p.is_dir():
            for q in sorted(p.rglob("*")):
                if q.suffix.lower() in IMG_EXTS:
                    paths.append(str(q))
        elif p.exists():
            paths.append(str(p))
    return paths

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", required=True)
    ap.add_argument("--source", nargs="+", required=True)
    ap.add_argument("--conf", type=float, default=0.5)
    ap.add_argument("--imgsz", type=int, default=1280)
    ap.add_argument("--device", default="")
    ap.add_argument("--project", default="runs_local")
    ap.add_argument("--name", default=None)
    args = ap.parse_args()

    ts = time.strftime("%Y%m%d_%H%M%S")
    name = args.name or f"predict_{ts}"
    src_list = expand_sources(args.source)
    if not src_list:
        print("No valid images found in --source")
        return

    print(f"Inference start: images={len(src_list)}, weights={args.weights}, conf={args.conf}")
    model = YOLO(args.weights)
    results = model.predict(
        source=src_list,
        conf=args.conf,
        imgsz=args.imgsz,
        device=args.device,
        save=True,
        project=args.project,
        name=name,
        verbose=False
    )
    for r in results:
        masks = 0 if r.masks is None else r.masks.data.shape[0]
        print(f"Image: {Path(r.path).name} masks={masks}")
    out = Path(model.predictor.save_dir) if hasattr(model, "predictor") else Path(args.project) / name
    print(f"Inference done. Output: {out}")

if __name__ == "__main__":
    main()
