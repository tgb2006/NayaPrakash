"""Validator for Sankshipt 2-Page A5 Chapter Markdown, word counts, and Jain ethics."""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from src.models.review import ValidationReport, SectionWordReport

SECTION_PATTERNS = [
    (1, r"^#{1,3}\s*(?:૧[\.\s\)]+|)(?:સૂત્રાર્થ\s+અને\s+જોવાનો\s+અભિગમ|સૂત્રાર્થ|દર્શન\s+અને\s+સૂત્રાર્થ)(?:[:\s]|$)"),
    (2, r"^#{1,3}\s*(?:૨[\.\s\)]+|)(?:વ્યવહારિક\s+જીવનમાં\s+વિનિયોગ|વ્યવહારિક\s+સમજ|જીવન-વ્યવહાર)(?:[:\s]|$)"),
    (3, r"^#{1,3}\s*(?:૩[\.\s\)]+|)(?:સાધના-મર્મ|સાધનાકીય\s+સમજ|ભીતરનો\s+વળાંક)(?:[:\s]|$)"),
    (4, r"^(?:#{1,3}\s*(?:૪[\.\s\)]+|)(?:બોધ-સૂત્ર|નયાતીત\s+બોધ-સૂત્ર)(?:[:\s]|$)|>\s*(?:🌟\s*)?\*\*બોધ-સૂત્ર\*\*)"),
    (5, r"^#{1,3}\s*(?:૫[\.\s\)]+|)(?:નવલિકા|ટૂંકી\s+નવલિકા)(?:[:\s]|$)")
]

PROHIBITED_ETHICAL_PATTERNS = [
    (r"(?:कसाई|કસાઈ)\s+(?:का\s+काम\s+अच्छा|सराहनीय|प्रशंसनीय|कुशल\s+धर्म|નું\s+કામ\s+સારું|પ્રશંસનીય)", "કસાઈ કર્મના સમર્થનનો નિષેધ છે"),
    (r"(?:शिकार|શિકાર)\s+(?:करना\s+उचित|का\s+महिमामंडन|કરવો\s+યોગ્ય)", "શિકાર અથવા પ્રાણીહિંસાનો મહિમા વર્જિત છે"),
    (r"(?:मांसाहार|मद्यपान|માંસાહાર|મદિરાપાન)\s+(?:उत्तम|आवश्यक|श्रेष्ठ|ઉત્તમ|શ્રેષ્ઠ)", "માંસાહાર કે મદિરાપાનનું સમર્થન જૈન સિદ્ધાંતો વિરુદ્ધ છે")
]

class ChapterValidator:
    def __init__(self):
        pass

    def count_words(self, text: str) -> int:
        """Counts words cleanly in text."""
        cleaned = re.sub(r"[#\*\-_`>|~]", " ", text)
        words = [w for w in cleaned.strip().split() if len(w) > 0]
        return len(words)

    def parse_sections(self, content: str) -> Dict[int, Tuple[str, str, int]]:
        """Splits 2-page chapter text into sections."""
        lines = content.splitlines()
        section_indices: List[Tuple[int, int, str]] = []

        for line_no, line in enumerate(lines):
            stripped = line.strip()
            for sec_num, pattern in SECTION_PATTERNS:
                if re.search(pattern, stripped, re.IGNORECASE):
                    section_indices.append((sec_num, line_no, stripped))
                    break

        unique_secs = {}
        for sec_num, l_no, title in section_indices:
            if sec_num not in unique_secs:
                unique_secs[sec_num] = (l_no, title)

        sorted_secs = sorted(unique_secs.items(), key=lambda x: x[1][0])
        parsed: Dict[int, Tuple[str, str, int]] = {}

        for i, (sec_num, (start_line, title)) in enumerate(sorted_secs):
            end_line = sorted_secs[i + 1][1][0] if i + 1 < len(sorted_secs) else len(lines)
            sec_body = "\n".join(lines[start_line + 1:end_line]).strip()
            word_count = self.count_words(sec_body)
            parsed[sec_num] = (title, sec_body, word_count)

        return parsed

    def validate_content(self, content: str) -> ValidationReport:
        errors: List[str] = []
        warnings: List[str] = []
        missing_sections: List[str] = []
        word_reports: Dict[str, SectionWordReport] = {}

        parsed = self.parse_sections(content)
        total_words = self.count_words(content)

        # 1. Required section presence
        section_names = {
            1: "સૂત્રાર્થ અને જોવાનો અભિગમ (ડાબું પાનું)",
            2: "વ્યવહારિક જીવનમાં વિનિયોગ (ડાબું પાનું)",
            3: "સાધના-મર્મ (ડાબું પાનું)",
            4: "બોધ-સૂત્ર (ડાબું પાનું)",
            5: "નવલિકા (જમણું પાનું)"
        }

        for sec_num, name in section_names.items():
            if sec_num not in parsed:
                missing_sections.append(name)
                errors.append(f"અનિવાર્ય વિભાગ ગેરહાજર છે: {name}")

        # 2. Left Page words (Sections 1-4 combined)
        left_words = sum(parsed.get(i, ("", "", 0))[2] for i in [1, 2, 3, 4])
        left_pass = (left_words >= 200 and left_words <= 380)
        word_reports["ડાબું પાનું (દર્શન, વ્યવહાર, સાધના)"] = SectionWordReport(
            section_name="ડાબું પાનું",
            expected_range="૨૫૦ થી ૩૨૦ શબ્દો (A5 પાનું ૧)",
            actual_words=left_words,
            passed=left_pass
        )
        if not left_pass and 1 in parsed:
            if left_words < 200:
                warnings.append(f"ડાબા પાના પર માત્ર {left_words} શબ્દો છે (લક્ષ્ય ૨૫૦-૩૨૦).")
            elif left_words > 380:
                errors.append(f"ડાબા પાના પર {left_words} શબ્દો છે, જે A5 સાઇઝના ૧ પાનાની ક્ષમતા કરતાં વધારે છે (મહત્તમ ૩૫૦).")

        # 3. Right Page words (Section 5 - Novella)
        novella_words = parsed.get(5, ("", "", 0))[2]
        novella_pass = (novella_words >= 250 and novella_words <= 400)
        word_reports["જમણું પાનું (સંપૂર્ણ નવલિકા)"] = SectionWordReport(
            section_name="જમણું પાનું (નવલિકા)",
            expected_range="૩૦૦ થી ૩૬૦ શબ્દો (A5 પાનું ૨)",
            actual_words=novella_words,
            passed=novella_pass
        )
        if not novella_pass and 5 in parsed:
            if novella_words < 250:
                warnings.append(f"નવલિકામાં માત્ર {novella_words} શબ્દો છે (લક્ષ્ય ૩૦૦-૩૬૦ શબ્દો).")
            elif novella_words > 400:
                errors.append(f"નવલિકા {novella_words} શબ્દોની છે, જે A5 સાઇઝના ૧ પાનામાં સમાઈ શકે નહીં (મહત્તમ ૩૮૦).")

        # 4. Total Chapter Words (Target 500-650 words)
        total_pass = (total_words >= 450 and total_words <= 720)
        if total_words < 450:
            errors.append(f"પ્રકરણનું કુલ લખાણ {total_words} શબ્દોનું છે (ન્યૂનતમ ૪૫૦ શબ્દો અનિવાર્ય).")
        elif total_words > 720:
            errors.append(f"પ્રકરણનું કુલ લખાણ {total_words} શબ્દો છે, જે ૨ પાનાની મહત્તમ મર્યાદા (૬૮૦-૭૦૦ શબ્દો) કરતાં વધારે છે.")

        # 5. Ethical checks
        ahimsa_passed = True
        prohibited_issues = []
        for pat, msg in PROHIBITED_ETHICAL_PATTERNS:
            if re.search(pat, content):
                ahimsa_passed = False
                prohibited_issues.append(msg)
                errors.append(f"નૈતિક ઉલ્લંઘન: {msg}")

        # 6. Source citation restriction check
        if re.search(r"1_2_3_4_5_merged|\.pdf|\.txt|\.docx|આગમિક આધાર ગ્રંથ", content, re.IGNORECASE):
            errors.append("સ્રોત ઉલ્લેખ નિષેધ: અધ્યાયમાં ફાઇલ નામ (જેમ કે .pdf) અથવા 'આગમિક આધાર ગ્રંથ' લખવું વર્જિત છે.")

        is_valid = (len(errors) == 0 and len(missing_sections) == 0 and ahimsa_passed)

        return ValidationReport(
            is_valid=is_valid,
            missing_sections=missing_sections,
            word_count_reports=word_reports,
            total_words=total_words,
            ahimsa_passed=ahimsa_passed,
            prohibited_issues_found=prohibited_issues,
            errors=errors,
            warnings=warnings
        )

    def extract_novella(self, content: str) -> Optional[Dict[str, str]]:
        """Extracts the short story (novella) from Section 5 of chapter content."""
        parsed = self.parse_sections(content)
        if 5 not in parsed:
            return None

        title, body, word_count = parsed[5]
        # Clean title from header
        clean_title = re.sub(r"^#{1,3}\s*(?:નવલિકા\s*[:\-\.]*\s*)?", "", title).strip()
        if not clean_title:
            clean_title = "અધ્યાય નવલિકા"

        first_para = body.split("\n\n")[0] if "\n\n" in body else body[:200]

        return {
            "title": clean_title,
            "summary": first_para[:250] + "...",
            "full_text": body,
            "word_count": word_count
        }
