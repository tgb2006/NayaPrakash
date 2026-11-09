"""Book compiler for Sankshipt 2-Page A5 Edition of 203 Jain Nayas."""

from pathlib import Path
from typing import List, Dict, Any, Optional
from src.core.catalog_loader import CatalogLoader
from src.core.validator import ChapterValidator

def format_id(nid: Any) -> str:
    s = str(nid)
    if "." in s:
        parts = s.split(".")
        return f"{int(parts[0]):03d}.{parts[1]}"
    try:
        val = int(s)
        return f"{val:03d}"
    except ValueError:
        return s

class BookCompiler:
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent.parent
        self.output_dir = self.base_dir / "output"
        self.compiled_dir = self.output_dir / "compiled"
        self.compiled_dir.mkdir(parents=True, exist_ok=True)
        self.loader = CatalogLoader(self.base_dir)
        self.validator = ChapterValidator()

    def find_chapter_file(self, khanda_folder: Path, nid: Any) -> Optional[Path]:
        s = str(nid)
        if "." in s:
            parts = s.split(".")
            target_prefix = f"chapter_{int(parts[0]):03d}_{parts[1]}_"
        else:
            try:
                target_prefix = f"chapter_{int(s):03d}_"
            except ValueError:
                target_prefix = f"chapter_{s}_"

        for f in khanda_folder.glob("chapter_*.md"):
            if "." in s:
                if f.name.startswith(target_prefix):
                    return f
            else:
                if f.name.startswith(target_prefix):
                    remainder = f.name[len(target_prefix):]
                    if not (remainder and remainder[0].isdigit()):
                        return f
        return None

    def generate_toc(self) -> str:
        khandas = self.loader.get_khandas()
        book_cfg = self.loader.get_book_config().get("book", {})
        title = book_cfg.get("title", "નય-ચક્ષુ")
        subtitle = book_cfg.get("subtitle", "નયનું જ્ઞાન, સંશયનું સમાધાન")
        toc_lines = [
            f"# {title}: વિષય-સૂચિ (સંક્ષિપ્ત ૨-પેજ A5 આવૃત્તિ)",
            "",
            f"> **{subtitle}**",
            "",
            "---",
            ""
        ]

        # Preface (પ્રસ્તાવના)
        preface_dir = self.output_dir / "preface"
        if preface_dir.exists():
            pref_files = sorted(preface_dir.glob("*.md"))
            if pref_files:
                toc_lines.append("## પ્રસ્તાવના અને ગ્રંથ-પરિચય")
                for pf in pref_files:
                    pf_content = pf.read_text(encoding="utf-8")
                    words = self.validator.count_words(pf_content)
                    first_line = pf_content.strip().split("\n")[0].replace("#", "").strip()
                    toc_lines.append(f"  - 📖 **[{first_line}](preface/{pf.name})** `({words} શબ્દો)`")
                toc_lines.append("")

        # General Chapters (સામાન્ય પ્રવેશ પ્રકરણો - પૂર્વભૂમિકા)
        samanya_dir = self.output_dir / "samanya_prakaran"
        if samanya_dir.exists():
            toc_lines.append("## પૂર્વભૂમિકા: ૫ સામાન્ય પ્રવેશ પ્રકરણો")
            gen_files = sorted(samanya_dir.glob("prakaran_*_gu.md"))
            for gf in gen_files:
                gf_content = gf.read_text(encoding="utf-8")
                words = self.validator.count_words(gf_content)
                first_line = gf_content.strip().split("\n")[0].replace("#", "").strip()
                toc_lines.append(f"  - 📖 **[{first_line}](samanya_prakaran/{gf.name})** `({words} શબ્દો)`")
            toc_lines.append("")

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
            for idx, n in enumerate(nayas, 1):
                f = self.find_chapter_file(khanda_folder, n.id)
                if f:
                    content = f.read_text(encoding="utf-8")
                    words = self.validator.count_words(content)
                    novella_info = self.validator.extract_novella(content)
                    story_title = f" — *નવલિકા: {novella_info['title']}*" if novella_info else ""
                    toc_lines.append(f"  - [x] **પ્રકરણ {idx}**: [{n.name_hindi}]({k.slug}/{f.name}){story_title} `({words} શબ્દો / ૨ પાના)`")
                else:
                    toc_lines.append(f"  - [ ] **પ્રકરણ {idx}**: {n.name_hindi} — *{n.definition_brief}*")
            toc_lines.append("")

        # Appendices (પરિશિષ્ટ વિભાગ)
        parishishta_dir = self.output_dir / "parishishta"
        if parishishta_dir.exists():
            parish_files = sorted([f for f in parishishta_dir.glob("*.md") if f.is_file()])
            if parish_files:
                toc_lines.append("## પરિશિષ્ટ વિભાગ: સંદર્ભ, વિશ્લેષણ અને સમન્વય દર્શન")
                for pf in parish_files:
                    pf_content = pf.read_text(encoding="utf-8")
                    words = self.validator.count_words(pf_content)
                    first_line = pf_content.strip().split("\n")[0].replace("#", "").strip()
                    toc_lines.append(f"  - 📖 **[{first_line}](../parishishta/{pf.name})** `({words} શબ્દો)`")
                toc_lines.append("")

        toc_content = "\n".join(toc_lines)
        toc_path = self.compiled_dir / "NayaPrakash_Sankshipt_TOC.md"
        with open(toc_path, "w", encoding="utf-8") as f:
            f.write(toc_content)

        return str(toc_path)

    def compile_full_book(self) -> str:
        khandas = self.loader.get_khandas()
        book_cfg = self.loader.get_book_config().get("book", {})
        title = book_cfg.get("title", "નય-ચક્ષુ")
        subtitle = book_cfg.get("subtitle", "નયનું જ્ઞાન, સંશયનું સમાધાન")
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

        # Preface (પ્રસ્તાવના)
        preface_dir = self.output_dir / "preface"
        if preface_dir.exists():
            pref_files = sorted(preface_dir.glob("*.md"))
            for pf in pref_files:
                pf_text = pf.read_text(encoding="utf-8")
                total_words_compiled += self.validator.count_words(pf_text)
                book_lines.append(pf_text)
                book_lines.append("\n\n---\n")

        # General Chapters (સામાન્ય પ્રવેશ પ્રકરણો - પૂર્વભૂમિકા)
        samanya_dir = self.output_dir / "samanya_prakaran"
        if samanya_dir.exists():
            book_lines.append("\n\n# પૂર્વભૂમિકા: ૫ સામાન્ય પ્રવેશ પ્રકરણો\n\n---\n")
            gen_files = sorted(samanya_dir.glob("prakaran_*_gu.md"))
            for gf in gen_files:
                gf_text = gf.read_text(encoding="utf-8")
                total_words_compiled += self.validator.count_words(gf_text)
                total_chapters_included += 1
                book_lines.append(gf_text)
                book_lines.append("\n\n---\n")

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
                ch_file = self.find_chapter_file(khanda_folder, n.id)
                if ch_file:
                    ch_text = ch_file.read_text(encoding="utf-8")
                    total_words_compiled += self.validator.count_words(ch_text)
                    total_chapters_included += 1

                    book_lines.append(f"\n\n<!-- START 2-PAGE SPREAD: NAYA {nid_str} -->\n")
                    book_lines.append(ch_text)
                    book_lines.append(f"\n<!-- END 2-PAGE SPREAD: NAYA {nid_str} -->\n\n---\n")

        # Appendices (પરિશિષ્ટ વિભાગ)
        parishishta_dir = self.output_dir / "parishishta"
        if parishishta_dir.exists():
            book_lines.append("\n\n# પરિશિષ્ટ વિભાગ : સંદર્ભ, વિશ્લેષણ અને સમન્વય દર્શન\n\n---\n")
            parish_files = sorted([f for f in parishishta_dir.glob("*.md") if f.is_file()])
            for pf in parish_files:
                pf_text = pf.read_text(encoding="utf-8")
                total_words_compiled += self.validator.count_words(pf_text)
                for target in parish_files:
                    pf_text = pf_text.replace(f"]({target.name})", f"](../parishishta/{target.name})")
                book_lines.append(pf_text)
                book_lines.append("\n\n---\n")

        master_filename = "NayaPrakash_Sankshipt_Book.md"
        master_book_path = self.compiled_dir / master_filename
        with open(master_book_path, "w", encoding="utf-8") as f:
            f.write("\n".join(book_lines))

        # Regenerate TOC
        self.generate_toc()

        return str(master_book_path)
