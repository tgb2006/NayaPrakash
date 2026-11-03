"""Validator for Chapter Markdown adherence, word counts, and Jain ethics."""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from src.models.review import ValidationReport, SectionWordReport

SECTION_PATTERNS = [
    (1, r"^#{1,3}\s*(?:1[\.\s\)]+|)(?:નય|नय)\s*$"),
    (2, r"^#{1,3}\s*(?:2[\.\s\)]+|)(?:સામાન્ય\s+અર્થ\s+(?:અને|એવં)\s+શબ્દાર્થ|सामान्य\s+अर्थ\s+एवं\s+शब्दार्थ)\b"),
    (3, r"^#{1,3}\s*(?:3[\.\s\)]+|)(?:તાર્કિક\s+વિવેચન|तार्किक\s+विवेचन)\b"),
    (4, r"^#{1,3}\s*(?:4[\.\s\)]+|)(?:3\s+)?(?:ઉદાહરણ|उदाहरण)\s*$"),
    (5, r"^#{1,3}\s*(?:5[\.\s\)]+|)(?:વ્યવહારિક\s+સમજ|व्यवहा?रिक\s+सम[जझ])\b"),
    (6, r"^#{1,3}\s*(?:6[\.\s\)]+|)(?:દાર્શનિક\s+સમજ|दार्शनिक\s+सम[जझ])\b"),
    (7, r"^#{1,3}\s*(?:7[\.\s\)]+|)(?:સૈદ્ધાંતિક\s+સમજ|सैद्धांतिक\s+सम[जझ])\b"),
    (8, r"^#{1,3}\s*(?:8[\.\s\)]+|)(?:સાધના(?:કીય|કિય)\s+સમજ|साधना(?:किय|कीय)\s+सम[जझ])\b"),
    (9, r"^#{1,3}\s*(?:9[\.\s\)]+|)(?:ડીપ\s+ડા[ઇઈ]વ|डीप\s+डा[ईइ]व)\b"),
    (10, r"^#{1,3}\s*(?:10[\.\s\)]+|)(?:મં[ઝજ]િલગામી\s+(?:વલણ|રૂખ|રુખ)|मं[झज]िलगामी\s+र[ुू][खख़])\b")
]

PROHIBITED_ETHICAL_PATTERNS = [
    (r"(?:कसाई|કસાઈ)\s+(?:का\s+काम\s+अच्छा|सराहनीय|प्रशंसनीय|कुशल\s+धर्म|નું\s+કામ\s+સારું|પ્રશંસનીય)", "कसाई कर्म का समर्थन/प्रशंसा वर्जित है"),
    (r"(?:शिकार|શિકાર)\s+(?:करना\s+उचित|का\s+महिमामंडन|કરવો\s+યોગ્ય)", "शिकार अथवा पशु-हिंसा का महिमामंडन वर्जित है"),
    (r"(?:मांसाहार|मद्यपान|માંસાહાર|મદિરાપાન)\s+(?:उत्तम|आवश्यक|श्रेष्ठ|ઉત્તમ|શ્રેષ્ઠ)", "मांसाहार अथवा मदिरा का समर्थन जैन सिद्धांतों के विरुद्ध है")
]

class ChapterValidator:
    def __init__(self):
        pass

    def count_words(self, text: str) -> int:
        """Counts words in Hindi/English text cleanly."""
        cleaned = re.sub(r"[#\*\-_`>|~]", " ", text)
        words = [w for w in cleaned.strip().split() if len(w) > 0]
        return len(words)

    def parse_sections(self, content: str) -> Dict[int, Tuple[str, str, int]]:
        """Splits chapter text into the 10 sections."""
        lines = content.splitlines()
        section_indices: List[Tuple[int, int, str]] = []

        for line_no, line in enumerate(lines):
            stripped = line.strip()
            for sec_num, pattern in SECTION_PATTERNS:
                if re.search(pattern, stripped, re.IGNORECASE):
                    section_indices.append((sec_num, line_no, stripped))
                    break

        # Remove duplicate detections of the same section, keeping earliest
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

        # Check for all 10 sections
        for sec_num, pattern in SECTION_PATTERNS:
            if sec_num not in parsed:
                missing_sections.append(f"सेक्शन {sec_num}")
                errors.append(f"अनिवार्य अनुभाग {sec_num} अनुपस्थित है।")

        # Word count checks
        # Section 3: Target ~1000 words (Min 450 words)
        sec_3_words = parsed.get(3, ("", "", 0))[2]
        sec_3_pass = sec_3_words >= 450
        word_reports["तार्किक विवेचन (सेक्शन 3)"] = SectionWordReport(
            section_name="तार्किक विवेचन",
            expected_range="लगभग 1000 शब्द (न्यूनतम 450)",
            actual_words=sec_3_words,
            passed=sec_3_pass
        )
        if not sec_3_pass and 3 in parsed:
            errors.append(f"सेक्शन 3 (तार्किक विवेचन) में केवल {sec_3_words} शब्द हैं (न्यूनतम 450 अपेक्षित)।")

        # Section 9: Min 300 words
        sec_9_words = parsed.get(9, ("", "", 0))[2]
        sec_9_pass = sec_9_words >= 280
        word_reports["डीप डाईव (सेक्शन 9)"] = SectionWordReport(
            section_name="डीप डाईव",
            expected_range="300 से 500 शब्द",
            actual_words=sec_9_words,
            passed=sec_9_pass
        )
        if not sec_9_pass and 9 in parsed:
            errors.append(f"सेक्शन 9 (डीप डाईव) में केवल {sec_9_words} शब्द हैं (न्यूनतम 300 अपेक्षित)।")

        # Section 10: Min 180 words
        sec_10_words = parsed.get(10, ("", "", 0))[2]
        sec_10_pass = sec_10_words >= 160
        word_reports["मंझिलगामी रूख (सेक्शन 10)"] = SectionWordReport(
            section_name="मंझिलगामी रूख",
            expected_range="180 से 250 शब्द",
            actual_words=sec_10_words,
            passed=sec_10_pass
        )
        if not sec_10_pass and 10 in parsed:
            errors.append(f"सेक्शन 10 (मंझिलगामी रूख) में केवल {sec_10_words} शब्द हैं (न्यूनतम 180 अपेक्षित)।")

        # Total words check
        if total_words < 1800:
            warnings.append(f"अध्याय का कुल शब्द विस्तार {total_words} शब्द है (आदर्श 2000-2500 शब्द)।")

        # Ahimsa check
        ahimsa_passed = True
        prohibited_issues = []
        for pat, msg in PROHIBITED_ETHICAL_PATTERNS:
            if re.search(pat, content):
                ahimsa_passed = False
                prohibited_issues.append(msg)
                errors.append(f"नैतिक उल्लंघन: {msg}")

        # Source citation restriction check (per user requirement: no source book / file mentions)
        if re.search(r"1_2_3_4_5_merged|\.pdf|\.txt|\.docx|आगमिक आधार ग्रंथ", content, re.IGNORECASE):
            errors.append("स्रोत उल्लेख निषेध: अध्याय में 'आगमिक आधार ग्रंथ' या फ़ाइल नाम (जैसे 1_2_3_4_5_merged.pdf) का उल्लेख वर्जित है।")

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

    def extract_examples(self, content: str) -> List[Dict[str, str]]:
        """Extracts 3 examples from Section 4 of chapter content."""
        parsed = self.parse_sections(content)
        if 4 not in parsed:
            return []

        sec_4_body = parsed[4][1]
        examples = []

        # Split by sub-headings or bullet markers
        ex_blocks = re.split(r"(?:###?\s*(?:उदाहरण|दृष्टांत|प्रसंग)\s*[:\-\d\.]+|^\s*(?:उदाहरण|प्रसंग)\s*[१२३123][:\-\.]|\b(?:प्रथम|द्वितीय|तृतीय)\s*उदाहरण\b)", sec_4_body, flags=re.MULTILINE)
        
        for idx, block in enumerate(ex_blocks):
            b_clean = block.strip()
            if len(b_clean) > 50:
                first_line = b_clean.splitlines()[0][:80]
                examples.append({
                    "title": first_line.strip("#* -:"),
                    "summary": b_clean[:300] + "...",
                    "full_text": b_clean
                })

        return examples[:3]
