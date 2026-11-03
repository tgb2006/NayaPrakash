"""Book compiler for Sankshipt 2-Page A5 Edition of 203 Jain Nayas."""

from pathlib import Path
from typing import List, Dict, Any, Optional
from src.core.catalog_loader import CatalogLoader
from src.core.validator import ChapterValidator

def format_id(nid: Any) -> str:
    try:
        val = int(str(nid))
        return f"{val:03d}"
    except ValueError:
        return str(nid)

class BookCompiler:
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent.parent
        self.output_dir = self.base_dir / "output"
        self.compiled_dir = self.output_dir / "compiled"
        self.compiled_dir.mkdir(parents=True, exist_ok=True)
        self.loader = CatalogLoader(self.base_dir)
        self.validator = ChapterValidator()

    def generate_toc(self) -> str:
        khandas = self.loader.get_khandas()
        book_cfg = self.loader.get_book_config().get("book", {})
        title = book_cfg.get("title", "રસપાન")
        subtitle = book_cfg.get("subtitle", "નયનું જ્ઞાન નિર્વાણનું પાન")
        toc_lines = [
            f"# {title}: વિષય-સૂચિ (સંક્ષિપ્ત ૨-પેજ A5 આવૃત્તિ)",
            "",
            f"> **{subtitle}**",
            "",
            "---",
            ""
        ]

        for k in khandas:
            khanda_title = k.name_hindi
            toc_lines.append(f"## {khanda_title}")
            toc_lines.append(f"- **મૂળ નય**: {k.root_naya} ({k.sanskrit_name})")
            toc_lines.append(f"- **મુખ્ય શ્રેણી**: {k.primary_division} | **સ્વરૂપ**: {k.tri_aspect}")
            toc_lines.append(f"- **અધ્યાય વિસ્તાર**: નય ક્રમાંક {k.range[0]} થી {k.range[1]} (કુલ {k.chapters_count} નય)")
            toc_lines.append("")

            khanda_folder = self.output_dir / k.slug
            intro_file = khanda_folder / f"000_{k.slug}_parichay_gu.md"
            if intro_file.exists():
                toc_lines.append(f"  - 📖 **[ખંડ પરિચય અને મૂળ નય પ્રવેશ]({k.slug}/{intro_file.name})**")
            else:
                toc_lines.append(f"  - ⏳ *ખંડ પરિચય પૃષ્ઠ: પ્રતીક્ષિત*")

            nayas = self.loader.get_nayas_by_khanda(k.id)
            for n in nayas:
                nid_str = format_id(n.id)
                matching_files = list(khanda_folder.glob(f"chapter_{nid_str}_*.md"))
                if matching_files:
                    f = matching_files[0]
                    content = f.read_text(encoding="utf-8")
                    words = self.validator.count_words(content)
                    novella_info = self.validator.extract_novella(content)
                    story_title = f" — *નવલિકા: {novella_info['title']}*" if novella_info else ""
                    toc_lines.append(f"  - [x] **નય {nid_str}**: [{n.name_hindi}]({k.slug}/{f.name}){story_title} `({words} શબ્દો / ૨ પાના)`")
                else:
                    toc_lines.append(f"  - [ ] **નય {nid_str}**: {n.name_hindi} — *{n.definition_brief}*")
            toc_lines.append("")

        toc_content = "\n".join(toc_lines)
        toc_path = self.compiled_dir / "NayaPrakash_Sankshipt_TOC.md"
        with open(toc_path, "w", encoding="utf-8") as f:
            f.write(toc_content)

        return str(toc_path)

    def compile_full_book(self) -> str:
        khandas = self.loader.get_khandas()
        book_cfg = self.loader.get_book_config().get("book", {})
        title = book_cfg.get("title", "રસપાન")
        subtitle = book_cfg.get("subtitle", "નયનું જ્ઞાન નિર્વાણનું પાન")
        book_lines = [
            f"# {title}",
            f"### {subtitle}",
            "",
            "---",
            "",
            "## મંગલાચરણ",
            "",
            "```",
            "ણમો અરિહંતાણં, ણમો સિદ્ધાણં, ણમો આયરિયાણં।",
            "ણમો ઉવજ્ઝાયાણં, ણમો લોએ સવ્વસાહૂણં।।",
            "",
            "અનેકાંતમયી મૂર્તિઃ સત્યા સત્યવિભાવિની।",
            "નયપ્રકાશિકા ભૂયાજ્જિનેન્દ્રવદનામ્બુજાત્।।",
            "```",
            "",
            "---",
            ""
        ]

        total_words_compiled = 0
        total_chapters_included = 0

        for k in khandas:
            khanda_heading = k.name_hindi
            book_lines.append(f"\n\n# {khanda_heading}")
            book_lines.append(f"> **મૂળ સૂત્ર**: `{k.core_sutra}`")
            book_lines.append(f"> **વર્ગીકરણ**: {k.primary_division} ({k.tri_aspect})")
            book_lines.append("\n---\n")

            khanda_folder = self.output_dir / k.slug
            intro_file = khanda_folder / f"000_{k.slug}_parichay_gu.md"
            if intro_file.exists():
                intro_text = intro_file.read_text(encoding="utf-8")
                total_words_compiled += self.validator.count_words(intro_text)
                book_lines.append(intro_text)
                book_lines.append("\n\n---\n")

            nayas = self.loader.get_nayas_by_khanda(k.id)
            for n in nayas:
                nid_str = format_id(n.id)
                matching_files = list(khanda_folder.glob(f"chapter_{nid_str}_*.md"))
                if matching_files:
                    ch_file = matching_files[0]
                    ch_text = ch_file.read_text(encoding="utf-8")
                    total_words_compiled += self.validator.count_words(ch_text)
                    total_chapters_included += 1

                    book_lines.append(f"\n\n<!-- START 2-PAGE SPREAD: NAYA {nid_str} -->\n")
                    book_lines.append(ch_text)
                    book_lines.append(f"\n<!-- END 2-PAGE SPREAD: NAYA {nid_str} -->\n\n---\n")

        master_filename = "NayaPrakash_Sankshipt_Book.md"
        master_book_path = self.compiled_dir / master_filename
        with open(master_book_path, "w", encoding="utf-8") as f:
            f.write("\n".join(book_lines))

        # Regenerate TOC
        self.generate_toc()

        return str(master_book_path)
