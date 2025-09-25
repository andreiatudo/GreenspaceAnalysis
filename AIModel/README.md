# Quick Commands — Green-Space Pipeline

Minimal reference for the 5 scripts: what they do and the arguments you must pass.

---

## 1) setup_roboflow.py
**What it does:** Extracts a dataset ZIP and prints image counts per split.

**Command:**
```powershell
python .\src\setup_roboflow.py --zip <ZIP_PATH> --outdir <EXTRACT_DIR> [--force]
```
- Required: `--zip <ZIP_PATH>`
- Optional: `--outdir <EXTRACT_DIR>` (default `.`), `--force`
- Also supports positional ZIP: `python .\src\setup_roboflow.py <ZIP_PATH>`

**Example:**
```powershell
python .\src\setup_roboflow.py --zip .\data\MainDataSet.v2i.yolov8.zip --outdir . --force
```

---

## 2) train_seg.py
**What it does:** Trains a YOLO segmentation model on your dataset YAML and saves weights.

**Command:**
```powershell
python .\src\train_seg.py --data <DATA_YAML> [--model <CKPT_OR_NAME>] [--epochs N] [--imgsz N] [--batch N|-1] [--device 0] [--project <DIR>] [--name <RUN>]
```
- Required: `--data <DATA_YAML>`
- Common optional: `--model yolov8n-seg.pt`, `--epochs 50`, `--imgsz 640`, `--batch -1`, `--device 0`

**Example:**
```powershell
python .\src\train_seg.py --data .\data.yaml --model yolov8n-seg.pt --epochs 50 --imgsz 640 --batch -1 --device 0 --project .\runs --name seg_n_640
```

---

## 3) infer_seg.py
**What it does:** Runs segmentation inference on files/folders and saves visual outputs.

**Command:**
```powershell
python .\src\infer_seg.py --weights <WEIGHTS_PT> --source <IMG_OR_DIR> [<IMG_OR_DIR> ...] [--conf 0.5] [--imgsz 640] [--device 0] [--project <DIR>] [--name <RUN>]
```
- Required: `--weights <WEIGHTS_PT>`, `--source <IMG_OR_DIR> [<...>]`

**Example:**
```powershell
python .\src\infer_seg.py --weights .\runs\seg_n_640\weights\best.pt --source .\test\images --conf 0.5 --imgsz 640
```

---

## 4) analyze_masks.py
**What it does:** Runs the model, filters masks by confidence and minimum area, writes one JSON per image to a timestamped `reports/<timestamp>/json` (or `--outdir`).

**Command:**
```powershell
python .\src\analyze_masks.py --weights <WEIGHTS_PT> --source <IMG_DIR_OR_FILE> [--conf 0.6] [--min-area-frac 0.02] [--imgsz 1280] [--outdir <DIR>]
```
- Required: `--weights <WEIGHTS_PT>`, `--source <IMG_DIR_OR_FILE>`
- Common optional: `--conf`, `--min-area-frac`, `--imgsz`, `--outdir`

**Example:**
```powershell
python .\src\analyze_masks.py --weights .\runs\seg_n_640\weights\best.pt --source .\test\images --conf 0.6 --min-area-frac 0.02 --imgsz 1280
```

---

## 5) generate_report.py
**What it does:** Reads the analyzer JSONs and saves `Green-Space_Survey_Report.md`, `.html`, and `coverage_summary.csv`.

**Command:**
```powershell
python .\src\generate_report.py --indir <REPORT_JSON_DIR> [--model-name "LABEL"] [--metrics results.json]
```
- Required: `--indir <REPORT_JSON_DIR>` (path to the `json` folder)

**Example:**
```powershell
python .\src\generate_report.py --indir .\reports\YYYY-MM-DD_HH-MM-SS\json --model-name "YOLOv8-seg (best.pt)"
```
