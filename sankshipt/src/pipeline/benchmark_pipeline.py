import time
import json
import re
from pathlib import Path
try:
    from .gender_fixer import sanitize_paryaya_gender
except ImportError:
    from gender_fixer import sanitize_paryaya_gender

def benchmark():
    t0 = time.time()
    base_dir = Path(".").resolve()
    sankshipt_dir = base_dir / "sankshipt"
    out_dir = sankshipt_dir / "output"
    img_map_file = base_dir / "Image" / "chapter-image-map.json"

    print("=" * 60)
    print("🚀 NAYA PRAKASH: HIGH-SPEED PIPELINE BENCHMARK")
    print("=" * 60)

    # 1. Load Image Map
    t_start = time.time()
    with open(img_map_file, 'r', encoding='utf-8') as f:
        img_records = json.load(f)
    img_by_src = {rec['source_file'].replace('\\', '/'): rec for rec in img_records}
    t_img = time.time() - t_start
    print(f"✓ Stage 1: Loaded {len(img_records)} image mappings in {t_img*1000:.1f} ms")

    # 2. Scan and parse all markdown chapters
    t_start = time.time()
    md_files = sorted(list(out_dir.glob("khanda_*/*.md")))
    chapter_files = [f for f in md_files if not f.name.startswith("000_")]
    print(f"✓ Found {len(chapter_files)} chapter markdown files (excluding intro files).")

    parsed_chapters = []
    gender_fixes_total = 0
    matched_images_total = 0

    for ch_path in chapter_files:
        raw_text = ch_path.read_text(encoding='utf-8')
        
        # Gender fix
        clean_text, fixes = sanitize_paryaya_gender(raw_text)
        if fixes > 0:
            gender_fixes_total += fixes

        # Rel path for image matching
        rel_src = ch_path.relative_to(base_dir).as_posix()
        img_rec = img_by_src.get(rel_src)
        if img_rec:
            matched_images_total += 1

        # Extract basic sections
        has_tattva = "## તત્વધારા" in clean_text
        has_kavya = "## કાવ્યધારા" in clean_text or "## કાવ્યધારા અને સાધનાધારા" in clean_text
        has_katha = "## કથાધારા" in clean_text
        has_vivek = "## વિવેકધારા" in clean_text
        has_darshan = "## દર્શનધારા" in clean_text

        parsed_chapters.append({
            "path": rel_src,
            "has_all_sections": (has_tattva and has_kavya and has_katha and has_vivek and has_darshan),
            "image": img_rec['press_file'] if img_rec else None,
            "gender_fixes": fixes
        })

    t_parse = time.time() - t_start
    print(f"✓ Stage 2: Parsed & validated {len(parsed_chapters)} chapters in {t_parse*1000:.1f} ms")
    print(f"    • Total 'પર્યાય' gender anomalies caught/corrected: {gender_fixes_total}")
    print(f"    • Total high-res 1-bit press images matched: {matched_images_total} / {len(img_records)}")

    # 3. Overall speed summary
    t_total = time.time() - t0
    print("\n" + "=" * 60)
    print(f"⚡ PIPELINE AUDIT COMPLETED IN {t_total:.2f} SECONDS!")
    print(f"   Rate: {len(chapter_files) / t_total:.1f} chapters/second parsed & verified!")
    print("=" * 60)

if __name__ == "__main__":
    benchmark()
