import argparse, sys
from pathlib import Path
from ultralytics import YOLO

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--model", default="yolov8n-seg.pt")
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--device", default="")
    ap.add_argument("--project", default="runs")
    ap.add_argument("--name", default=None)
    ap.add_argument("--patience", type=int, default=50)
    args = ap.parse_args()

    data_yaml = Path(args.data)
    if not data_yaml.exists():
        print(f"Data YAML not found: {data_yaml}")
        sys.exit(2)

    model_arg = args.model
    model_path = Path(model_arg) if model_arg.endswith(".pt") else None
    if model_path and model_path.exists():
        try:
            size = model_path.stat().st_size
            if size < 100_000:
                print(f"Detected tiny or corrupt weights: {model_path} ({size} bytes). Deleting.")
                model_path.unlink(missing_ok=True)
        except Exception as e:
            print(f"Warning: could not inspect weights file: {e}")

    print("Training start")
    print(f"- data:   {data_yaml}")
    print(f"- model:  {model_arg}")
    print(f"- epochs: {args.epochs}")
    print(f"- imgsz:  {args.imgsz}")
    print(f"- batch:  {args.batch}")
    print(f"- device: {args.device}")
    print(f"- out:    {args.project} / {args.name or '(auto)'}")
    print(f"- patience: {args.patience}")

    try:
        model = YOLO(model_arg)
    except Exception as e:
        print(f"Failed to load model '{model_arg}': {e}")
        if model_path and model_path.exists():
            try:
                model_path.unlink(missing_ok=True)
            except Exception as de:
                print(f"Cleanup failed: {de}")
        raise

    r = model.train(
        data=str(data_yaml),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project=args.project,
        name=args.name,
        patience=args.patience
    )

    save_dir = Path(r.save_dir)
    best = save_dir / "weights" / "best.pt"
    last = save_dir / "weights" / "last.pt"
    print("Training done")
    print(f"- best: {best if best.exists() else '(missing)'}")
    print(f"- last: {last if last.exists() else '(missing)'}")

if __name__ == "__main__":
    main()
