import shutil
from pathlib import Path

art_dir = Path(r"C:\Users\Admin\.gemini\antigravity\brain\5a6fbdb9-9b2f-4a7a-8b5e-4d67f6575988")
ch070_dir = Path("sankshipt/pilot_long_title_ch070").resolve()
ch001_dir = Path("sankshipt/pilot_chapter_001").resolve()

copies = [
    (ch070_dir / "tattvadhara_symmetrical_zoom.png", art_dir / "ch070_tattvadhara_symmetrical_zoom.png"),
    (ch070_dir / "page_002_left_preview.png", art_dir / "ch070_page_002_left_preview.png"),
    (ch070_dir / "chapter_070_spread_preview.png", art_dir / "chapter_070_spread_preview.png"),
    (ch070_dir / "chapter_070.pdf", art_dir / "chapter_070.pdf"),
    (ch001_dir / "ch001_tattvadhara_zoom.png", art_dir / "ch001_tattvadhara_zoom.png"),
    (ch001_dir / "page_002_left_preview.png", art_dir / "chapter_001_page_002_preview.png"),
    (ch001_dir / "chapter_001_spread_preview.png", art_dir / "chapter_001_spread_preview.png"),
    (ch001_dir / "chapter_001.pdf", art_dir / "chapter_001.pdf"),
]

for src, dst in copies:
    shutil.copy2(src, dst)
    print(f"Copied {src.name} -> {dst.name}")

print("All artifact files synchronized successfully!")
