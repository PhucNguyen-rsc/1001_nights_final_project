"""Install Ali Baba neutral-emotion full-body sprites into the engine, and rewrite
animation CSVs so only the body slot renders. Run from worktree root."""
import csv
import os
from PIL import Image

EMOTIONS_DIR = "/Users/pucca/NYUAD/1001/Royal-Animation/character_emotions"
SPRITE_ROOT = "data/animation/sprite/character"
ANIM_ROOT = "data/animation/1"

# engine_char -> (emotion_sheet_prefix, target_height_px)
# target_h = 2 * (foot_y - body_y) from the engine char's Default/0 row,
# so the resized image's centre lands at body_y and bottom at foot_y.
MAPPING = {
    "miquella":       ("alibaba",                 548),
    "miquella_kid":   ("alibaba_son",             374),
    "miquella_doll":  ("tailor",                  248),
    "trina":          ("marianna",                660),
    "trina_kid":      ("abdallah",                376),
    "trina_doll":     ("marianna",                244),
    "rabbit_leader":  ("chief_of_thief",          404),
    "rabbit_servant": ("standard_thief",          404),
    "lacrima":        ("qasim_wife",              236),
    "malenia":        ("alibaba_wife",           1190),
    "godrick":        ("qasim",                   550),
}


def neutral_crop(sheet_path):
    """Take leftmost 1/5 of sheet, then tight-bbox crop transparent margins."""
    img = Image.open(sheet_path).convert("RGBA")
    w, h = img.size
    cell = img.crop((0, 0, w // 5, h))
    bbox = cell.getbbox()
    if bbox:
        cell = cell.crop(bbox)
    return cell


def resize_to_height(img, target_h):
    w, h = img.size
    new_w = max(1, round(w * target_h / h))
    return img.resize((new_w, target_h), Image.LANCZOS)


def install_all():
    for char, (sheet_prefix, target_h) in MAPPING.items():
        sheet = os.path.join(EMOTIONS_DIR, f"{sheet_prefix}_emotions.png")
        if not os.path.exists(sheet):
            print(f"  MISSING SHEET: {sheet}")
            continue
        cropped = neutral_crop(sheet)
        resized = resize_to_height(cropped, target_h)
        # overwrite every body png variant (most chars have only body.png)
        body_dir = os.path.join(SPRITE_ROOT, char, "body", "1", "normal")
        if not os.path.isdir(body_dir):
            print(f"  MISSING BODY DIR: {body_dir}")
            continue
        for fname in os.listdir(body_dir):
            if fname.endswith(".png"):
                target = os.path.join(body_dir, fname)
                resized.save(target)
                print(f"  wrote {target} ({resized.size})")
        # also handle alt mode subfolders (normal2, etc.) so mode-overrides match
        mode_root = os.path.join(SPRITE_ROOT, char, "body", "1")
        for sub in os.listdir(mode_root):
            sub_dir = os.path.join(mode_root, sub)
            if sub == "normal" or not os.path.isdir(sub_dir):
                continue
            for fname in os.listdir(sub_dir):
                if fname.endswith(".png"):
                    target = os.path.join(sub_dir, fname)
                    resized.save(target)
                    print(f"  wrote (mode={sub}) {target}")


def body_only_csvs():
    """Rewrite each character's animation CSV so every row has only p1_body filled
    (using whatever Default/0's p1_body cell says) and all other character-part
    columns are blank. Keep Name, effect_*, frame_property, animation_property,
    sound_effect untouched."""
    keep_cols = {"Name", "p1_body"}
    # also keep the engine-property columns (last few)
    suffix_keep = ("effect_1", "effect_2", "effect_3", "effect_4", "effect_5",
                   "effect_6", "effect_7", "effect_8", "frame_property",
                   "animation_property", "sound_effect")
    for char in MAPPING:
        path = os.path.join(ANIM_ROOT, f"{char}.csv")
        if not os.path.exists(path):
            print(f"  MISSING ANIM CSV: {path}")
            continue
        with open(path, encoding="utf-8") as f:
            rows = list(csv.reader(f))
        header = rows[0]
        # find Default/0 row to grab the canonical body cell
        body_idx = header.index("p1_body")
        default_row = next((r for r in rows[1:] if r and r[0] == "Default/0"), None)
        if not default_row:
            print(f"  NO Default/0 in {path}")
            continue
        canonical_body = default_row[body_idx]
        # normalize the body cell so the new full-body sprite renders upright,
        # un-flipped, scale 1. Cell format:
        # <type>,<name>,<x>,<y>,<angle>,<flip>,<layer>,<scale_x>,<scale_y>,<extra>
        parts = canonical_body.split(",")
        if len(parts) == 10:
            parts[4] = "0"  # angle
            parts[5] = "0"  # flip
            parts[7] = "1"  # scale_x
            parts[8] = "1"  # scale_y
            canonical_body = ",".join(parts)
        # decide which columns to keep
        keep_idx = set()
        for i, col in enumerate(header):
            if col in keep_cols or col in suffix_keep:
                keep_idx.add(i)
        # rewrite rows
        new_rows = [header]
        for r in rows[1:]:
            if not r:
                continue
            new_r = [""] * len(header)
            for i in range(len(header)):
                if i < len(r):
                    if i in keep_idx:
                        new_r[i] = r[i]
            # always force p1_body to canonical
            new_r[body_idx] = canonical_body
            new_rows.append(new_r)
        with open(path, "w", encoding="utf-8", newline="") as f:
            csv.writer(f, quoting=csv.QUOTE_MINIMAL).writerow(new_rows[0])
            for r in new_rows[1:]:
                csv.writer(f, quoting=csv.QUOTE_MINIMAL).writerow(r)
        print(f"  rewrote {path} ({len(new_rows)-1} rows; body cell={canonical_body!r})")


if __name__ == "__main__":
    print("== installing body sprites ==")
    install_all()
    print()
    print("== rewriting animation CSVs to body-only ==")
    body_only_csvs()
