"""Book compiler that unites all 7 Khandas, introductions, and 203 chapters into a complete work."""

from pathlib import Path
from typing import List, Dict, Any, Optional
from src.core.catalog_loader import CatalogLoader
from src.core.validator import ChapterValidator

class BookCompiler:
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent.parent
        self.output_dir = self.base_dir / "output"
        self.compiled_dir = self.output_dir / "compiled"
        self.compiled_dir.mkdir(parents=True, exist_ok=True)
        self.loader = CatalogLoader(self.base_dir)
        self.validator = ChapterValidator()

    def generate_toc(self, lang: str = "gu") -> str:
        khandas = self.loader.get_khandas()
        is_gu = (lang == "gu")

        if is_gu:
            toc_lines = [
                "# નય પ્રકાશ: વિષય-સૂચિ (Table of Contents - ગુજરાતી સંસ્કરણ)",
                "",
                "> **સપ્ત મૂળ નયોના આલોકમાં ૨૦૩ નયોનું સમગ્ર અનુશીલન**",
                "",
                "---",
                ""
            ]
        else:
            toc_lines = [
                "# नय प्रकाश: विषय-सूची (Table of Contents - हिन्दी संस्करण)",
                "",
                "> **सप्त मूल नयों के आलोक में 203 नयों का समग्र अनुशीलन**",
                "",
                "---",
                ""
            ]

        for k in khandas:
            khanda_title = k.name_hindi
            if is_gu:
                toc_lines.append(f"## {khanda_title}")
                toc_lines.append(f"- **મૂળ નય**: {k.root_naya} ({k.sanskrit_name})")
                toc_lines.append(f"- **મુખ્ય શ્રેણી**: {k.primary_division} | **સ્વરૂપ**: {k.tri_aspect}")
                toc_lines.append(f"- **અધ્યાય વિસ્તાર**: નય ક્રમાંક {k.range[0]} થી {k.range[1]} (કુલ {k.chapters_count} નય)")
            else:
                toc_lines.append(f"## {khanda_title}")
                toc_lines.append(f"- **मूल नय**: {k.root_naya} ({k.sanskrit_name})")
                toc_lines.append(f"- **मुख्य श्रेणी**: {k.primary_division} | **स्वरूप**: {k.tri_aspect}")
                toc_lines.append(f"- **अध्याय विस्तार**: नय क्रमांक {k.range[0]} से {k.range[1]} (कुल {k.chapters_count} नय)")
            toc_lines.append("")

            # Khanda intro file check
            khanda_folder = self.output_dir / k.slug
            intro_filename = f"000_{k.slug}_parichay_gu.md" if is_gu else f"000_{k.slug}_parichay.md"
            intro_file = khanda_folder / intro_filename
            if intro_file.exists():
                intro_label = "ખંડ પરિચય અને મૂળ નય મીમાંસા" if is_gu else "खंड परिचय एवं मूल नय मीमांसा"
                toc_lines.append(f"  - 📖 **[{intro_label}]({k.slug}/{intro_file.name})**")
            else:
                waiting_label = "ખંડ પરિચય પૃષ્ઠ: પ્રતીક્ષિત" if is_gu else "खंड परिचय पृष्ठ: प्रारूपण हेतु प्रतीक्षित"
                toc_lines.append(f"  - ⏳ *{waiting_label}*")

            # Sub-nayas in this khanda
            nayas = self.loader.get_nayas_by_khanda(k.id)
            for n in nayas:
                if is_gu:
                    matching_files = list(khanda_folder.glob(f"chapter_{n.id:03d}_*_gu.md"))
                else:
                    matching_files = [f for f in khanda_folder.glob(f"chapter_{n.id:03d}_*.md") if not f.name.endswith("_gu.md")]

                word_label = "શબ્દો" if is_gu else "शब्द"
                naya_prefix = "નય" if is_gu else "नय"

                if matching_files:
                    f = matching_files[0]
                    content = f.read_text(encoding="utf-8")
                    words = self.validator.count_words(content)
                    toc_lines.append(f"  - [x] **{naya_prefix} {n.id:03d}**: [{n.name_hindi}]({k.slug}/{f.name}) `({words} {word_label})`")
                else:
                    toc_lines.append(f"  - [ ] **{naya_prefix} {n.id:03d}**: {n.name_hindi} — *{n.definition_brief}*")
            toc_lines.append("")

        toc_content = "\n".join(toc_lines)
        toc_filename = "NayaPrakash_TOC_Gujarati.md" if is_gu else "NayaPrakash_TOC.md"
        toc_path = self.compiled_dir / toc_filename
        with open(toc_path, "w", encoding="utf-8") as f:
            f.write(toc_content)
        if is_gu:
            with open(self.compiled_dir / "NayaPrakash_TOC.md", "w", encoding="utf-8") as f:
                f.write(toc_content)

        return str(toc_path)

    def compile_full_book(self, lang: str = "gu") -> str:
        khandas = self.loader.get_khandas()
        is_gu = (lang == "gu")

        if is_gu:
            book_lines = [
                "# નય પ્રકાશ: જૈન દર્શનના ૨૦૩ નયોનું સમગ્ર અનુશીલન",
                "### સપ્ત મૂળ નયોના આલોકમાં ૨૦૩ નયોનો તાર્કિક, દાર્શનિક, વ્યવહારિક તેમજ સાધનાકીય મહાગ્રંથ (ગુજરાતી આવૃત્તિ)",
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
        else:
            book_lines = [
                "# नय प्रकाश: जैन दर्शन के 203 नयों का समग्र अनुशीलन",
                "### सप्त मूल नयों के आलोक में 203 नयों का तार्किक, दार्शनिक, व्यावहारिक एवं साधनाकीय महाग्रंथ (हिन्दी संस्करण)",
                "",
                "---",
                "",
                "## मंगलाचरण",
                "",
                "```",
                "णमो अरिहंताणं, णमो सिद्धाणं, णमो आइरियाणं।",
                "णमो उवज्झायाणं, णमो लोए सव्वसाहूणं।।",
                "",
                "अनेकांतमयी मूर्तिः सत्या सत्यविभाविनी।",
                "नयप्रकाशिका भूयाज्जिनेन्द्रवदनाम्बुजात्।।",
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
            if is_gu:
                book_lines.append(f"> **મૂળ સૂત્ર**: `{k.core_sutra}`")
                book_lines.append(f"> **વર્ગીકરણ**: {k.primary_division} ({k.tri_aspect})")
            else:
                book_lines.append(f"> **मूल सूत्र**: `{k.core_sutra}`")
                book_lines.append(f"> **वर्गीकरण**: {k.primary_division} ({k.tri_aspect})")
            book_lines.append("\n---\n")

            khanda_folder = self.output_dir / k.slug
            intro_filename = f"000_{k.slug}_parichay_gu.md" if is_gu else f"000_{k.slug}_parichay.md"
            intro_file = khanda_folder / intro_filename
            if intro_file.exists():
                intro_text = intro_file.read_text(encoding="utf-8")
                total_words_compiled += self.validator.count_words(intro_text)
                book_lines.append(intro_text)
                book_lines.append("\n\n---\n")

            nayas = self.loader.get_nayas_by_khanda(k.id)
            for n in nayas:
                if is_gu:
                    matching_files = list(khanda_folder.glob(f"chapter_{n.id:03d}_*_gu.md"))
                else:
                    matching_files = [f for f in khanda_folder.glob(f"chapter_{n.id:03d}_*.md") if not f.name.endswith("_gu.md")]

                if matching_files:
                    ch_file = matching_files[0]
                    ch_text = ch_file.read_text(encoding="utf-8")
                    total_words_compiled += self.validator.count_words(ch_text)
                    total_chapters_included += 1

                    book_lines.append(f"\n\n<!-- START CHAPTER {n.id} ({'GUJARATI' if is_gu else 'HINDI'}) -->\n")
                    book_lines.append(ch_text)
                    book_lines.append(f"\n<!-- END CHAPTER {n.id} -->\n\n---\n")

        master_filename = "NayaPrakash_Complete_Book_Gujarati.md" if is_gu else "NayaPrakash_Complete_Book.md"
        master_book_path = self.compiled_dir / master_filename
        with open(master_book_path, "w", encoding="utf-8") as f:
            f.write("\n".join(book_lines))
        if is_gu:
            with open(self.compiled_dir / "NayaPrakash_Complete_Book.md", "w", encoding="utf-8") as f:
                f.write("\n".join(book_lines))

        # Regenerate TOC as well
        self.generate_toc(lang=lang)

        return str(master_book_path)
