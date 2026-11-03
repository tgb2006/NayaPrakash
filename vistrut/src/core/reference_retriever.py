"""Reference search and retrieval engine for Jain Darshan scriptures and commentaries."""

import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

BOOK_DESCRIPTIONS = {
    "1_2_3_4_5_decoded_full.txt": "नयचक्रप्रकाश / नयप्रकाश (मूल आधार ग्रंथ - 1_2_3_4_5_merged.pdf)",
    "203_Nayas_List_From_Book.md": "203 नयों की प्रामाणिक सूची एवं लक्षण (नयप्रकाश आधार)",
    "Aalappaddhati_Acharya_Devasena.txt": "आलापपद्धति (आचार्य देवसेन) - नय एवं प्रमाण मूल लक्षण",
    "Nayavimshika_Acharya_Abhayshekharsuri.txt": "नयविंशिका (आचार्य अभयशेखरसूरिजी) - सप्त नय गंभीर विवेचन",
    "Panchadhyayi_Nayachakra_Original.txt": "पंचाध्यायी नयचक्र (पांडे राजमल्लजी) - निश्चय व व्यवहार नय",
    "Nayachakra_Pandit_Sumatprakash_Jain.md": "पंचाध्यायी के नय (पं. सुमतप्रकाशजी) - आध्यात्मिक नय वर्गीकरण",
    "saptabhangi_nayapradip_004070_ocr1.docx": "सप्तभंगी नयप्रदीप (महोपाध्याय यशोविजयजी गणिवर)",
    "Dravya_Guna_Paryay_no_Ras_Abhayshekharsuri.txt": "द्रव्य-गुण-पर्याय नो रास (यशोविजयजी / अभयशेखरसूरिजी)",
    "Dravya_Guna_Paryay_no_Ras_Paramarsh_Part01.txt": "द्रव्यानुयोग परामर्श भाग 1 (यशोविजयजी)",
    "Dravya_Guna_Paryay_no_Ras_Paramarsh_Part02.txt": "द्रव्यानुयोग परामर्श भाग 2 (यशोविजयजी)",
    "Dravya_Guna_Paryay_no_Ras_Paramarsh_Part03.txt": "द्रव्यानुयोग परामर्श भाग 3 (यशोविजयजी)",
    "Dravya_Guna_Paryay_no_Ras_Paramarsh_Part04.txt": "द्रव्यानुयोग परामर्श भाग 4 (यशोविजयजी)",
    "Dravya_Guna_Paryay_no_Ras_Paramarsh_Part05.txt": "द्रव्यानुयोग परामर्श भाग 5 (यशोविजयजी)",
    "Dravya_Guna_Paryay_no_Ras_Paramarsh_Part06.txt": "द्रव्यानुयोग परामर्श भाग 6 (यशोविजयजी)",
    "Dravya_Guna_Paryay_no_Ras_Paramarsh_Part07.txt": "द्रव्यानुयोग परामर्श भाग 7 (यशोविजयजी)"
}

HINDI_TO_GUJARATI_TERMS = {
    "नैगम": ["નૈગમ", "नैगम"],
    "संग्रह": ["સંગ્રહ", "संग्रह"],
    "व्यवहार": ["વ્યવહાર", "व्यवहार"],
    "ऋजुसूत्र": ["ઋજુસૂત્ર", "ऋजुसूत्र"],
    "शब्दनय": ["શબ્દનય", "शब्दनय"],
    "समभिरूढ़": ["સમભિરૂઢ", "समभिरूढ़", "સમભિરુઢ"],
    "एवंभूत": ["એવંભૂત", "एवंभूत"],
    "द्रव्यार्थिक": ["દ્રવ્યાર્થિક", "द्रव्यार्थिक"],
    "पर्यायार्थिक": ["પર્યાયાર્થિક", "पर्यायार्थिक"],
    "सामान्य": ["સામાન્ય", "सामान्य"],
    "विशेष": ["વિશેષ", "विशेष"],
    "संकल्प": ["સંકલ્પ", "संकल्प"],
    "अनिष्पन्न": ["અનિષ્પન્ન", "अनिष्पन्न", "निष्पन्न"]
}

class ReferenceRetriever:
    def __init__(self, references_dir: Optional[Path] = None):
        self.ref_dir = references_dir or (Path(__file__).resolve().parent.parent.parent / "references")
        self._text_cache: Dict[str, str] = {}

    def get_available_books(self) -> List[Dict[str, str]]:
        books = []
        if not self.ref_dir.exists():
            return books

        for file_path in self.ref_dir.iterdir():
            if file_path.suffix.lower() in [".txt", ".md", ".docx"]:
                desc = BOOK_DESCRIPTIONS.get(file_path.name, file_path.stem)
                books.append({
                    "filename": file_path.name,
                    "title": desc,
                    "extension": file_path.suffix
                })
        return books

    def load_file_text(self, file_path: Path) -> str:
        if file_path.name in self._text_cache:
            return self._text_cache[file_path.name]

        text = ""
        ext = file_path.suffix.lower()
        try:
            if ext in [".txt", ".md"]:
                text = file_path.read_text(encoding="utf-8", errors="ignore")
            elif ext == ".docx":
                with zipfile.ZipFile(file_path) as z:
                    xml_content = z.read("word/document.xml")
                    tree = ET.fromstring(xml_content)
                    texts = [elem.text for elem in tree.iter() if elem.text]
                    text = " ".join(texts)
        except Exception as e:
            text = f"Error reading {file_path.name}: {e}"

        self._text_cache[file_path.name] = text
        return text

    def _stem_term(self, word: str) -> List[str]:
        stems = [word]
        # Strip common Sanskrit/Hindi case endings
        stripped = re.sub(r"[ेैोंंः्ािीुूोौ]+$", "", word)
        if len(stripped) >= 3 and stripped != word:
            stems.append(stripped)
        for suffix in ["ेऽर्थे", "ेअर्थे", "वत्", "स्य", "ात्", "ेण", "ाय", "योः", "ेषु", "ानि", "तया"]:
            if word.endswith(suffix):
                stem = word[:-len(suffix)]
                if len(stem) >= 3:
                    stems.append(stem)

        # Add bilingual Gujarati variants
        for hi_key, equivalents in HINDI_TO_GUJARATI_TERMS.items():
            if hi_key in word or any(stem in hi_key for stem in stems):
                stems.extend(equivalents)

        return list(dict.fromkeys(stems))

    def search(
        self,
        keywords: List[str],
        max_snippets: int = 4,
        book_filter: Optional[str] = None,
        snippet_radius: int = 350,
        exclude_filenames: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Searches across all reference files for keyword occurrences and returns contextual snippets."""
        if not keywords:
            return []

        expanded_terms = []
        for kw in keywords:
            kw_clean = kw.strip()
            if len(kw_clean) >= 2:
                expanded_terms.extend(self._stem_term(kw_clean))

        expanded_terms = list(dict.fromkeys(expanded_terms))
        if not expanded_terms:
            return []

        escaped_kws = [re.escape(k) for k in expanded_terms]

        # High priority classical books to search first
        priority_files = [
            "1_2_3_4_5_decoded_full.txt",
            "203_Nayas_List_From_Book.md",
            "Aalappaddhati_Acharya_Devasena.txt",
            "Nayavimshika_Acharya_Abhayshekharsuri.txt",
            "Panchadhyayi_Nayachakra_Original.txt",
            "saptabhangi_nayapradip_004070_ocr1.docx",
            "Nayachakra_Pandit_Sumatprakash_Jain.md",
            "Dravya_Guna_Paryay_no_Ras_Abhayshekharsuri.txt"
        ]

        all_files = list(self.ref_dir.iterdir())
        sorted_files = sorted(
            [f for f in all_files if f.suffix.lower() in [".txt", ".md", ".docx"]],
            key=lambda f: priority_files.index(f.name) if f.name in priority_files else 99
        )

        results = []
        combined_pattern = re.compile("|".join(escaped_kws), re.IGNORECASE)

        for f in sorted_files:
            if exclude_filenames and f.name in exclude_filenames:
                continue

            if book_filter and book_filter.lower() not in f.name.lower():
                continue

            content = self.load_file_text(f)
            matches = list(combined_pattern.finditer(content))
            if not matches:
                continue

            book_title = BOOK_DESCRIPTIONS.get(f.name, f.stem)
            used_spans = []

            for m in matches:
                pos = m.start()
                if any(start <= pos <= end for start, end in used_spans):
                    continue

                start_idx = max(0, pos - snippet_radius)
                end_idx = min(len(content), pos + snippet_radius)

                raw_snippet = content[start_idx:end_idx]
                cleaned = re.sub(r"[\r\n]+", " ", raw_snippet).strip()
                cleaned = re.sub(r"\s+", " ", cleaned)

                # Skip header-only lines like url links
                if "jainqq.org" in cleaned and len(cleaned) < 150:
                    continue

                term_hits = sum(1 for kw in escaped_kws if re.search(kw, cleaned, re.IGNORECASE))
                score = term_hits * 10 + (20 if f.name in priority_files else 5)

                results.append({
                    "book": book_title,
                    "filename": f.name,
                    "score": score,
                    "snippet": cleaned,
                    "match_term": m.group(0)
                })
                used_spans.append((start_idx, end_idx))

                if len(results) >= max_snippets * 4:
                    break

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:max_snippets]

    def get_references_for_naya(self, naya_id: Union[int, float, str], naya_name: str, khanda_id: int) -> List[Dict[str, Any]]:
        """Intelligently derives search terms based on Naya ID and name, then fetches relevant shastric text."""
        results = []

        # 1. Primary: Extract exact entry from main reference book 1_2_3_4_5_merged.pdf
        main_file = self.ref_dir / "1_2_3_4_5_decoded_full.txt"
        if main_file.exists():
            content = self.load_file_text(main_file)
            pages = content.split("=== PAGE ")
            list_text = "\n".join(pages[31:]) if len(pages) > 31 else content
            pat = re.compile(rf"(?:^|\n)\s*0?{re.escape(str(naya_id))}\s*[\.\-]\s*([^\n]+(?:\n\s*[^\n\d=][^\n]+)*)", re.MULTILINE)
            m_list = list(pat.finditer(list_text))
            if m_list:
                best = max(m_list, key=lambda m: len(m.group(1)))
                snippet_text = re.sub(r"\s+", " ", best.group(1)).strip()
                results.append({
                    "book": "नयचक्रप्रकाश (मुख्य आधार ग्रंथ - 1_2_3_4_5_merged.pdf)",
                    "filename": "1_2_3_4_5_merged.pdf",
                    "score": 1000,
                    "snippet": snippet_text,
                    "match_term": f"नय {naya_id}"
                })

        # 2. Secondary: Search other classical references (Aalappaddhati, Nayavimshika, Panchadhyayi, etc.)
        terms = [naya_name]
        cleaned_name = re.sub(r"नैगम|संग्रह|व्यवहार|ऋजुसूत्र|शब्द|समभिरूढ़|एवंभूत|नय", "", naya_name).strip()
        parts = [p.strip() for p in re.split(r"[\s\-_]+", cleaned_name) if len(p.strip()) > 2]
        terms.extend(parts)

        khanda_terms_map = {
            1: ["नैगम", "अनिष्पन्न", "संकल्प", "सामान्यविशेष"],
            2: ["संग्रह", "स्वजात्यविरोध", "महासत्ता", "अपरसंग्रह"],
            3: ["व्यवहार", "संग्रहगृहीत", "सद्भूत", "असद्भूत"],
            4: ["ऋजुसूत्र", "वर्तमानक्षण", "प्रगुणं", "पर्यायार्थिक"],
            5: ["शब्दनय", "कालकारक", "लिंगसंख्या", "वाच्यवाचक"],
            6: ["समभिरूढ़", "पर्यायवाचि", "व्युत्पत्तिभेद", "इन्द्रशक्र"],
            7: ["एवंभूत", "यथाशब्दप्रवृत्ति", "क्रियापरिणत", "तत्काल"]
        }

        k_terms = khanda_terms_map.get(khanda_id, [])
        query_terms = list(dict.fromkeys(terms + k_terms))

        secondary_snippets = self.search(
            keywords=query_terms,
            max_snippets=3,
            book_filter=None,
            exclude_filenames=[
                "1_2_3_4_5_decoded_full.txt",
                "203_Nayas_List_From_Book.md",
                "decoded_203_nayas_clean.txt",
                "decoded_203_nayas_raw.txt",
                "bharati_mapping.json"
            ]
        )
        for s in secondary_snippets:
            results.append(s)

        return results[:4]

    def format_reference_context_for_prompt(self, naya_id: Union[int, float, str], naya_name: str, khanda_id: int) -> str:
        """Formats classical reference excerpts into a markdown section to inject into generation prompts."""
        snippets = self.get_references_for_naya(naya_id, naya_name, khanda_id)
        if not snippets:
            return "उपलब्ध संदर्भ ग्रंथों में इस नय हेतु कोई प्रत्यक्ष उद्धरण प्राप्त नहीं हुआ।"

        lines = [
            "### संदर्भ ग्रंथालय से प्रामाणिक शास्त्रीय उद्धरण एवं सूत्र (CLASSICAL SCRIPTURAL EXCERPTS):",
            "लेखन करते समय इन शास्त्रीय संदर्भों, सूत्रों और आचार्यों के विचारों का अध्याय के तार्किक, दार्शनिक व सैद्धांतिक विवेचन में समुचित उद्धरण दें:",
            ""
        ]

        for idx, s in enumerate(snippets, 1):
            lines.append(f"**[{idx}] {s['book']}**:")
            lines.append(f"> \"...{s['snippet']}...\"")
            lines.append("")

        return "\n".join(lines)
