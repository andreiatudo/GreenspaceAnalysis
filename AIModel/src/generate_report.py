import argparse, json, csv, datetime, io, base64
from collections import defaultdict, Counter
from pathlib import Path
import matplotlib.pyplot as plt

def make_bar_chart(class_names, percents, title="Coverage Summary", ylabel="Mean area (%)"):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(class_names, percents, color="#2a7fff")
    ax.set_ylabel(ylabel)
    ax.set_xlabel("Class")
    ax.set_title(title)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    plt.xticks(rotation=30, ha="right")
    buf = io.BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode("utf-8")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--indir", required=True)
    ap.add_argument("--model-name", default="YOLOv8-seg (best.pt)")
    ap.add_argument("--metrics", default=None, help="Optional path to results.json with YOLO metrics")
    args = ap.parse_args()

    indir = Path(args.indir)
    if not indir.exists():
        print(f"JSON folder not found: {indir}")
        return

    json_files = sorted(indir.glob("*.json"))
    if not json_files:
        print("No JSON files found")
        return

    per_image = []
    class_set = set()
    counts = Counter()
    for jf in json_files:
        with open(jf, "r", encoding="utf-8") as f:
            data = json.load(f)
        h, w = data["height"], data["width"]
        img_area = float(h * w)
        d = defaultdict(float)
        for seg in data.get("segments_kept", []):
            cname = seg.get("class_name", str(seg.get("class_id", "?")))
            d[cname] += float(seg["area_pixels"]) / img_area
            class_set.add(cname)
            counts[cname] += 1
        per_image.append(d)

    class_list = sorted(class_set)
    nimg = len(per_image)
    mean_fracs = {}
    for c in class_list:
        s = sum(d.get(c, 0.0) for d in per_image)
        mean_fracs[c] = (s / nimg) * 100.0
    mean_fracs = dict(sorted(mean_fracs.items(), key=lambda kv: kv[1], reverse=True))

    # === Save CSV ===
    outdir = indir.parent
    csv_path = outdir / "coverage_summary.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["class", "mean_area_percent", "instances"])
        for c, v in mean_fracs.items():
            w.writerow([c, f"{v:.2f}", counts[c]])

    # === Load YOLO metrics if available ===
    metrics_data = None
    if args.metrics and Path(args.metrics).exists():
        with open(args.metrics, "r", encoding="utf-8") as f:
            metrics_data = json.load(f)

    # === Markdown report ===
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    md_path = outdir / "Green-Space_Survey_Report.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Green-Space Survey Report\n\n")
        f.write(f"- Generated: {now}\n")
        f.write(f"- Images: {nimg}\n")
        f.write(f"- Model: {args.model_name}\n")
        f.write("- Filters: confidence and min_area_frac applied in analysis\n\n")

        f.write("## Coverage Summary (mean area % per class)\n\n")
        f.write("| Class | Mean area | Instances |\n|---|---:|---:|\n")
        for c, v in mean_fracs.items():
            f.write(f"| {c} | {v:.2f}% | {counts[c]} |\n")

        if metrics_data:
            f.write("\n## YOLO Metrics (validation set)\n\n")
            f.write("| Class | Box(P) | Box(R) | Box mAP50 | Mask(P) | Mask(R) | Mask mAP50 |\n")
            f.write("|---|---:|---:|---:|---:|---:|---:|\n")
            for c in metrics_data.get("per_class", []):
                f.write(f"| {c['name']} | {c['box_p']:.3f} | {c['box_r']:.3f} | {c['box_ap50']:.3f} "
                        f"| {c['mask_p']:.3f} | {c['mask_r']:.3f} | {c['mask_ap50']:.3f} |\n")

        # Simple interpretation
        f.write("\n## Interpretation\n")
        if mean_fracs:
            top_class = next(iter(mean_fracs))
            f.write(f"- Model detects **{top_class}** most reliably (largest coverage in test images).\n")
        if counts:
            rare = [c for c,v in counts.items() if v < 3]
            if rare:
                f.write(f"- Classes with very few examples (need more data): {', '.join(rare)}.\n")

    # === HTML report ===
    html_path = outdir / "Green-Space_Survey_Report.html"
    chart_uri = make_bar_chart(list(mean_fracs.keys()), [mean_fracs[c] for c in mean_fracs.keys()])
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Green-Space Survey Report</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 24px; }}
table {{ border-collapse: collapse; width: 100%; max-width: 800px; }}
th, td {{ border-bottom: 1px solid #eee; padding: 6px 10px; }}
th {{ text-align: left; background: #f9f9f9; }}
td.num {{ text-align: right; }}
.meta {{ color:#555; margin-bottom: 4px; }}
.chart {{ margin: 16px 0 24px; }}
h2 {{ margin-top: 28px; }}
</style></head><body>
<h1>Green-Space Survey Report</h1>
<div class="meta">Generated: {now}</div>
<div class="meta">Images: {nimg}</div>
<div class="meta">Model: {args.model_name}</div>
<div class="meta">Filters: confidence and min_area_frac applied in analysis</div>
<div class="chart"><img src="{chart_uri}" alt="Coverage Summary"></div>
<h2>Coverage Summary</h2>
<table>
<thead><tr><th>Class</th><th class="num">Mean area (%)</th><th class="num">Instances</th></tr></thead>
<tbody>
"""
    for c, v in mean_fracs.items():
        html += f"<tr><td>{c}</td><td class=\"num\">{v:.2f}</td><td class=\"num\">{counts[c]}</td></tr>\n"
    html += "</tbody></table>"

    if metrics_data:
        html += "<h2>YOLO Metrics (validation set)</h2><table><thead><tr>"
        html += "<th>Class</th><th class='num'>Box(P)</th><th class='num'>Box(R)</th><th class='num'>Box mAP50</th>"
        html += "<th class='num'>Mask(P)</th><th class='num'>Mask(R)</th><th class='num'>Mask mAP50</th></tr></thead><tbody>"
        for c in metrics_data.get("per_class", []):
            html += (f"<tr><td>{c['name']}</td><td class='num'>{c['box_p']:.3f}</td><td class='num'>{c['box_r']:.3f}</td>"
                     f"<td class='num'>{c['box_ap50']:.3f}</td><td class='num'>{c['mask_p']:.3f}</td>"
                     f"<td class='num'>{c['mask_r']:.3f}</td><td class='num'>{c['mask_ap50']:.3f}</td></tr>")
        html += "</tbody></table>"

    if mean_fracs:
        top_class = next(iter(mean_fracs))
        html += f"<h2>Interpretation</h2><p>Model detects <b>{top_class}</b> most reliably in this dataset."
        rare = [c for c,v in counts.items() if v < 3]
        if rare:
            html += f" However, classes with very few examples (need more data): {', '.join(rare)}."
        html += "</p>"

    html += "</body></html>"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Report saved: {md_path}")
    print(f"CSV saved: {csv_path}")
    print(f"HTML saved: {html_path}")

if __name__ == "__main__":
    main()
