"""Validator for Sankshipt 2-Page A5 Chapter Markdown, word counts, and Jain ethics."""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from src.models.review import ValidationReport, SectionWordReport

SECTION_PATTERNS = [
    (1, r"^#{1,3}\s*\*{0,2}(?:૧[\.\s\)]+|)(?:તત્વધારા|નય\s*વિવેચન|વિવેચન)\*{0,2}(?:[:\s]|$)"),
    (2, r"^(?:#{1,3}\s*\*{0,2}(?:૨[\.\s\)]+|)(?:કાવ્યધારા|કાવ્યાત્મક\s+બોધસૂત્ર|બોધ-સૂત્ર|બોધસૂત્ર)\*{0,2}(?:[:\s]|$)|>\s*(?:🌟\s*)?\*\*(?:કાવ્યાત્મક\s+)?બોધસૂત્ર\*\*)"),
    (3, r"^#{1,3}\s*\*{0,2}(?:૩[\.\s\)]+|)(?:કથાધારા|પ્રસંગ|કથા)\*{0,2}(?:[:\s]|$)"),
    (4, r"^#{1,3}\s*\*{0,2}(?:૪[\.\s\)]+|)(?:વિવેકધારા|વિવેક-દર્શન|એકાંત\s+દર્શન|એકાંત)\*{0,2}(?:[:\s]|$)"),
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
        """Counts words cleanly in Indic/Gujarati text."""
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

        # 1. Required section presence (4 Dhara Sections)
        section_names = {
            1: "તત્વધારા (ડાબું પાનું - સંપૂર્ણ વિવેચન)",
            2: "કાવ્યધારા (ડાબું પાનું - ૨ પંક્તિનો દોહરો)",
            3: "કથાધારા (જમણું પાનું - પિપાસા અને પાન)",
            4: "વિવેકધારા (જમણું પાનું - એકાંત અને અનેકાંત)"
        }

        for sec_num, name in section_names.items():
            if sec_num not in parsed:
                missing_sections.append(name)
                errors.append(f"અનિવાર્ય વિભાગ ગેરહાજર છે: {name}")

        # Check sub-phases of Kathadhara: પિપાસા and પાન
        if 3 in parsed:
            katha_body = parsed[3][1]
            if not re.search(r"###\s*\*{0,2}પિપાસા", katha_body, re.IGNORECASE):
                warnings.append("કથાધારામાં '### પિપાસા' પેટા-વિભાગ સ્પષ્ટ હોવો આવશ્યક છે.")
            if not re.search(r"###\s*\*{0,2}પાન", katha_body, re.IGNORECASE):
                warnings.append("કથાધારામાં '### પાન' પેટા-વિભાગ સ્પષ્ટ હોવો આવશ્યક છે.")

        # Check sub-phases of Vivekadhara: એકાંત and અનેકાંત
        if 4 in parsed:
            vivek_body = parsed[4][1]
            if not re.search(r"###\s*\*{0,2}એકાંત", vivek_body, re.IGNORECASE):
                warnings.append("વિવેકધારામાં '### એકાંત દર્શન' પેટા-વિભાગ સ્પષ્ટ હોવો આવશ્યક છે.")
            if not re.search(r"###\s*\*{0,2}અનેકાંત", vivek_body, re.IGNORECASE):
                warnings.append("વિવેકધારામાં '### અનેકાંત દર્શન' પેટા-વિભાગ સ્પષ્ટ હોવો આવશ્યક છે.")

        # 2. Left Page words (Sections 1-2 combined: target ~240-300 words)
        left_words = sum(parsed.get(i, ("", "", 0))[2] for i in [1, 2])
        left_pass = (left_words >= 200 and left_words <= 360)
        word_reports["ડાબું પાનું (તત્વધારા & કાવ્યધારા)"] = SectionWordReport(
            section_name="ડાબું પાનું",
            expected_range="૨૩૦ થી ૩૨૦ શબ્દો (A5 પાનું ૧)",
            actual_words=left_words,
            passed=left_pass
        )
        if not left_pass and 1 in parsed:
            if left_words < 200:
                warnings.append(f"ડાબા પાના પર માત્ર {left_words} શબ્દો છે (લક્ષ્ય ૨૩૦-૩૨૦).")
            elif left_words > 360:
                errors.append(f"ડાબા પાના પર {left_words} શબ્દો છે, જે A5 સાઇઝના ૧ પાનાની ક્ષમતા કરતાં વધારે છે (મહત્તમ ૩૫૦).")

        # 3. Right Page words (Sections 3-4 combined: target ~250-320 words)
        right_words = sum(parsed.get(i, ("", "", 0))[2] for i in [3, 4])
        right_pass = (right_words >= 220 and right_words <= 370)
        word_reports["જમણું પાનું (કથાધારા & વિવેકધારા)"] = SectionWordReport(
            section_name="જમણું પાનું",
            expected_range="૨૪૦ થી ૩૩૦ શબ્દો (A5 પાનું ૨)",
            actual_words=right_words,
            passed=right_pass
        )
        if not right_pass and 3 in parsed:
            if right_words < 220:
                warnings.append(f"જમણા પાના પર માત્ર {right_words} શબ્દો છે (લક્ષ્ય ૨૪૦-૩૩૦ શબ્દો).")
            elif right_words > 370:
                errors.append(f"જમણા પાના પર {right_words} શબ્દો છે, જે A5 સાઇઝના ૧ પાનામાં સમાઈ શકે નહીં (મહત્તમ ૩૫૦).")

        # 4. Total Chapter Words (Target 500-650 words)
        total_pass = (total_words >= 460 and total_words <= 680)
        if total_words < 460:
            errors.append(f"પ્રકરણનું કુલ લખાણ {total_words} શબ્દોનું છે (ન્યૂનતમ ૪૬૦ શબ્દો અનિવાર્ય).")
        elif total_words > 680:
            errors.append(f"પ્રકરણનું કુલ લખાણ {total_words} શબ્દો છે, જે ૨ પાનાની મહત્તમ મર્યાદા (૬૬૦ શબ્દો) કરતાં વધારે છે.")

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
        """Extracts the story (Kathadhara: Pipasa & Paan) from Section 3 of chapter content."""
        parsed = self.parse_sections(content)
        if 3 not in parsed:
            return None

        title, body, word_count = parsed[3]
        clean_title = re.sub(r"^#{1,3}\s*\*{0,2}(?:કથાધારા|પ્રસંગ)\s*[:\-\.]*\s*", "", title).strip()
        clean_title = re.sub(r"\*{1,2}$", "", clean_title).strip()
        if not clean_title:
            clean_title = "અધ્યાય કથાધારા (પિપાસા-પાન)"

        first_para = body.split("\n\n")[0] if "\n\n" in body else body[:200]

        return {
            "title": clean_title,
            "summary": first_para[:250] + "...",
            "full_text": body,
            "word_count": word_count
        }
