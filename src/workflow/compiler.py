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

    def generate_toc(self) -> str:
        khandas = self.loader.get_khandas()
        toc_lines = [
            "# नय प्रकाश: विषय-सूची (Table of Contents)",
            "",
            "> **सप्त मूल नयों के आलोक में 203 नयों का समग्र अनुशीलन**",
            "",
            "---",
            ""
        ]

        for k in khandas:
            toc_lines.append(f"## {k.name_hindi}")
            toc_lines.append(f"- **मूल नय**: {k.root_naya} ({k.sanskrit_name})")
            toc_lines.append(f"- **मुख्य श्रेणी**: {k.primary_division} | **स्वरूप**: {k.tri_aspect}")
            toc_lines.append(f"- **अध्याय विस्तार**: नय क्रमांक {k.range[0]} से {k.range[1]} (कुल {k.chapters_count} नय)")
            toc_lines.append("")

            # Khanda intro file check
            khanda_folder = self.output_dir / k.slug
            intro_file = khanda_folder / f"000_{k.slug}_parichay.md"
            if intro_file.exists():
                toc_lines.append(f"  - 📖 **[खंड परिचय एवं मूल नय मीमांसा]({k.slug}/{intro_file.name})**")
            else:
                toc_lines.append(f"  - ⏳ *खंड परिचय पृष्ठ: प्रारूपण हेतु प्रतीक्षित*")

            # Sub-nayas in this khanda
            nayas = self.loader.get_nayas_by_khanda(k.id)
            for n in nayas:
                # Look for matching chapter file
                matching_files = list(khanda_folder.glob(f"chapter_{n.id:03d}_*.md"))
                if matching_files:
                    f = matching_files[0]
                    content = f.read_text(encoding="utf-8")
                    words = self.validator.count_words(content)
                    toc_lines.append(f"  - [x] **नय {n.id:03d}**: [{n.name_hindi}]({k.slug}/{f.name}) `({words} शब्द)`")
                else:
                    toc_lines.append(f"  - [ ] **नय {n.id:03d}**: {n.name_hindi} — *{n.definition_brief}*")
            toc_lines.append("")

        toc_content = "\n".join(toc_lines)
        toc_path = self.compiled_dir / "NayaPrakash_TOC.md"
        with open(toc_path, "w", encoding="utf-8") as f:
            f.write(toc_content)

        return str(toc_path)

    def compile_full_book(self) -> str:
        khandas = self.loader.get_khandas()
        config = self.loader.get_book_config()
        book_meta = config.get("book", {})

        book_lines = [
            f"# {book_meta.get('title', 'नय प्रकाश: जैन दर्शन के 203 नयों का समग्र अनुशीलन')}",
            f"### {book_meta.get('subtitle', '')}",
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
            book_lines.append(f"\n\n# {k.name_hindi}")
            book_lines.append(f"> **मूल सूत्र**: `{k.core_sutra}`")
            book_lines.append(f"> **वर्गीकरण**: {k.primary_division} ({k.tri_aspect})")
            book_lines.append("\n---\n")

            khanda_folder = self.output_dir / k.slug
            intro_file = khanda_folder / f"000_{k.slug}_parichay.md"
            if intro_file.exists():
                intro_text = intro_file.read_text(encoding="utf-8")
                total_words_compiled += self.validator.count_words(intro_text)
                book_lines.append(intro_text)
                book_lines.append("\n\n---\n")

            nayas = self.loader.get_nayas_by_khanda(k.id)
            for n in nayas:
                matching_files = list(khanda_folder.glob(f"chapter_{n.id:03d}_*.md"))
                if matching_files:
                    ch_file = matching_files[0]
                    ch_text = ch_file.read_text(encoding="utf-8")
                    total_words_compiled += self.validator.count_words(ch_text)
                    total_chapters_included += 1

                    book_lines.append(f"\n\n<!-- START CHAPTER {n.id} -->\n")
                    book_lines.append(ch_text)
                    book_lines.append(f"\n<!-- END CHAPTER {n.id} -->\n\n---\n")

        master_book_path = self.compiled_dir / "NayaPrakash_Complete_Book.md"
        with open(master_book_path, "w", encoding="utf-8") as f:
            f.write("\n".join(book_lines))

        # Regenerate TOC as well
        self.generate_toc()

        return str(master_book_path)
