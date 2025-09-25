# README — CreatingPatches & CreatingBigImage

---

## Dependențe
```powershell
pip install pillow
```

---

## 1) CreatingPatches.py
Împarte o imagine (sau toate imaginile dintr-un folder) în patch-uri de dimensiune fixă și le salvează pe disc.

### Comandă
```powershell
python CreatingPatches.py --input <IMAGE_OR_FOLDER> --patch-width <W> --patch-height <H> --output-dir <OUT_DIR> [--prefix patch] [--ext png|jpg|jpeg] [--per-image-subfolders]
```

### Argumente
- `--input` (obligatoriu): fișier imagine sau folder cu imagini
- `--patch-width`, `--patch-height` (obligatorii): dimensiunea patch-urilor în pixeli
- `--output-dir` (implicit `patches`): directorul în care se salvează patch-urile
- `--prefix` (implicit `patch`): prefixul fișierelor patch
- `--ext` (implicit `png`): format de ieșire (`png|jpg|jpeg`)
- `--per-image-subfolders`: dacă intrarea este folder, creează subfoldere per imagine

### Exemple
```powershell
# o singură imagine -> patches/
python CreatingPatches.py --input .\image2.png --patch-width 1920 --patch-height 1080 --output-dir .\patches

# un folder de imagini -> patches/<nume_imagine>/
python CreatingPatches.py --input .ig_images --patch-width 1920 --patch-height 1080 --output-dir .\patches --per-image-subfolders
```

---

## 2) CreatingBigImage.py
Reconstruiește o imagine mare din patch-uri denumite `patch_<id>_<top>_<left>.<ext>`.

### Comandă
```powershell
python CreatingBigImage.py --patch-dir <PATCH_FOLDER> --output <OUT_IMAGE> [--patch-width <W> --patch-height <H>] [--prefix patch]
```

### Argumente
- `--patch-dir` (obligatoriu): folderul cu patch-uri
- `--output` (implicit `reconstructed.png`): fișierul de ieșire
- `--patch-width`, `--patch-height` (opționale): dacă lipsesc, dimensiunea se deduce din primul patch
- `--prefix` (implicit `patch`): prefixul folosit la spargere (trebuie să corespundă numelui patch-urilor)

### Exemple
```powershell
# reconstruire din patches/
python CreatingBigImage.py --patch-dir .\patches --output .
econstructed.png

# dacă patch-urile sunt în subfolderul imaginii și vrei să specifici prefixul
python CreatingBigImage.py --patch-dir .\patches\image2 --output .
econstructed_image2.png --prefix patch
```

> Notă: dacă căile conțin spații, pune-le între ghilimele.
