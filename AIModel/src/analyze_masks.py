import argparse, json, time
from pathlib import Path
from ultralytics import YOLO
import torch

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--conf", type=float, default=0.5)
    ap.add_argument("--min-area-frac", type=float, default=0.01)
    ap.add_argument("--imgsz", type=int, default=1280)
    ap.add_argument("--outdir", default=None)
    args = ap.parse_args()

    ts = time.strftime("%Y-%m-%d_%H-%M-%S")
    outdir = Path(args.outdir or f"reports/{ts}")
    json_dir = outdir / "json"
    json_dir.mkdir(parents=True, exist_ok=True)

    print("Analysis start")
    print(f"- weights:        {args.weights}")
    print(f"- source:         {args.source}")
    print(f"- conf:           {args.conf}")
    print(f"- min_area_frac:  {args.min_area_frac}")
    print(f"- imgsz:          {args.imgsz}")

    model = YOLO(args.weights)
    names = model.model.names if hasattr(model.model, "names") else {}

    results = model(args.source, conf=args.conf, stream=True, imgsz=args.imgsz, verbose=False)
    num_imgs = 0
    kept_total = 0

    for res in results:
        num_imgs += 1
        h, w = res.orig_shape
        img_area = float(h * w)
        kept = []
        if res.masks is not None and res.boxes is not None:
            masks = res.masks.data
            confs = res.boxes.conf.cpu().tolist()
            clss = res.boxes.cls.cpu().tolist()
            for i in range(masks.shape[0]):
                conf = float(confs[i])
                cls_id = int(clss[i])
                mask = masks[i]
                if mask.dtype != torch.bool:
                    mask = mask > 0.5
                area_pix = int(mask.sum().item())
                area_frac = area_pix / img_area
                if conf >= args.conf and area_frac >= args.min_area_frac:
                    kept.append({
                        "class_id": cls_id,
                        "class_name": names.get(cls_id, str(cls_id)),
                        "conf": conf,
                        "area_pixels": area_pix,
                        "area_frac": area_frac
                    })
        stem = Path(res.path).stem
        with open(json_dir / f"{stem}.json", "w", encoding="utf-8") as f:
            json.dump({
                "image": res.path,
                "height": h,
                "width": w,
                "segments_kept": kept,
                "params": {
                    "conf_threshold": args.conf,
                    "min_area_frac": args.min_area_frac
                }
            }, f, ensure_ascii=False, indent=2)
        kept_total += len(kept)
        print(f"Processed: {stem} kept_segments={len(kept)}")

    print("Analysis done")
    print(f"- images:     {num_imgs}")
    print(f"- kept total: {kept_total}")
    print(f"- output dir: {outdir}")
    print(f"Next: python .\\src\\generate_report.py --indir {json_dir}")

if __name__ == "__main__":
    main()
