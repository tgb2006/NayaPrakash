import re
import json
from pathlib import Path
from typing import Dict, Any, Optional
try:
    from .gender_fixer import sanitize_paryaya_gender
except ImportError:
    from gender_fixer import sanitize_paryaya_gender

def parse_markdown_chapter(md_path: Path, img_record: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    text = md_path.read_text(encoding="utf-8")
    text, fixes = sanitize_paryaya_gender(text)

    # 1. Title & Meta
    title_m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else md_path.stem

    meta_m = re.search(r'^\*\((.+?)\)\*', text, re.MULTILINE)
    khanda_label = "નૈગમ નય"
    aspect_label = "જ્ઞાનનય"
    category_label = "દ્રવ્યાર્થિક નય"
    sutra_text = "अनिष्पन्नेऽर्थे संकल्पमात्रग्राही नैगमः।"

    if meta_m:
        meta_str = meta_m.group(1)
        # Parse: મૂળ નય: ... | મુખ્ય શ્રેણી: ... | વ્યાખ્યા-સૂત્ર: ...
        parts = [p.strip() for p in meta_str.split('|')]
        for p in parts:
            if 'મૂળ નય:' in p:
                khanda_label = p.replace('મૂળ નય:', '').strip()
            elif 'મુખ્ય શ્રેણી:' in p:
                cat_val = p.replace('મુખ્ય શ્રેણી:', '').strip()
                if '-' in cat_val:
                    cparts = cat_val.split('-')
                    category_label = cparts[0].strip()
                    aspect_label = cparts[1].strip()
                else:
                    category_label = cat_val
            elif 'વ્યાખ્યા-સૂત્ર:' in p:
                sutra_text = p.replace('વ્યાખ્યા-સૂત્ર:', '').strip()

    # 2. Tattvadhara (4 Cards)
    # Rupak
    rupak_m = re.search(r'\*\*૧\.\s*રૂપક-દ્રષ્ટિ:\s*([^*]+)\*\*\s*\n([\s\S]*?)(?=\*\*૨\.|\n##)', text)
    rupak_sub = rupak_m.group(1).strip() if rupak_m else ""
    rupak_body = rupak_m.group(2).strip() if rupak_m else ""

    # Swarup
    swarup_m = re.search(r'\*\*૨\.\s*સ્વરૂપ-સૃષ્ટિ:\s*([^*]+)\*\*\s*\n([\s\S]*?)(?=\*\*૩\.|\n##)', text)
    swarup_sub = swarup_m.group(1).strip() if swarup_m else ""
    swarup_body = swarup_m.group(2).strip() if swarup_m else ""

    # Vyavahar
    vyavahar_m = re.search(r'\*\*૩\.\s*વ્યવહાર-પૃષ્ટિ:\s*([^*]+)\*\*\s*\n([\s\S]*?)(?=\*\*૪\.|\n##)', text)
    vyavahar_sub = vyavahar_m.group(1).strip() if vyavahar_m else ""
    vyavahar_body = vyavahar_m.group(2).strip() if vyavahar_m else ""

    # Marm
    marm_m = re.search(r'\*\*૪\.\s*મર્મ-તુષ્ટિ:\s*([^*]+)\*\*\s*\n([\s\S]*?)(?=\n##|---)', text)
    marm_sub = marm_m.group(1).strip() if marm_m else ""
    marm_body = marm_m.group(2).strip() if marm_m else ""

    # 3. Kavyadhara & Sadhanadhara
    kavya_m = re.search(r'\|\s*📜\s*કાવ્યધારા\s*\|\s*✦\s*સાધનાધારા\s*\|\s*\n\|[-:| ]+\|\s*\n\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', text)
    if kavya_m:
        kavya_text = kavya_m.group(1).strip().replace('<br>', '\n').replace('<br/>', '\n')
        sadhana_text = kavya_m.group(2).strip()
    else:
        kavya_text = "સહજ નય પ્રકાશે, આતમ રસ ભાસે."
        sadhana_text = "પર્યાયની ક્ષણિકતા જાણી અવિનાશી આત્મસ્વભાવમાં લીન થવું."

    # 4. Kathadhara
    katha_sec_m = re.search(r'## કથાધારા[\s\S]*?###\s*([^\n]+)\s*\n\s*###\s*પિપાસા\s*\n([\s\S]*?)\s*###\s*પાન\s*\n([\s\S]*?)(?=\n##|---)', text)
    if katha_sec_m:
        story_title = katha_sec_m.group(1).strip()
        pipasa_body = katha_sec_m.group(2).strip()
        paan_body = katha_sec_m.group(3).strip()
    else:
        story_title = img_record.get('story_title', 'ઓલવાયેલા દીવાનું અમૃત-તેજ') if img_record else "કથા શીર્ષક"
        pipasa_body = "પિપાસા વિવરણ..."
        paan_body = "પાન વિવરણ..."

    # 5. Vivekdhara
    vivek_m = re.search(r'## વિવેકધારા[\s\S]*?###\s*એકાંત દર્શન\s*\n([\s\S]*?)\s*###\s*અનેકાંત દર્શન\s*\n([\s\S]*?)(?=\n##|---)', text)
    if vivek_m:
        ekant_body = vivek_m.group(1).strip()
        anekant_body = vivek_m.group(2).strip()
    else:
        ekant_body = "એકાંત દર્શન લખાણ..."
        anekant_body = "અનેકાંત દર્શન લખાણ..."

    # 6. Darshandhara (4 pillars)
    darshan_m1 = re.search(r'-\s*\*\*૧\.\s*નય-ઉન્મેષ\*\*:\s*([^\n]+)', text)
    darshan_m2 = re.search(r'-\s*\*\*૨\.\s*પ્રાચીન-વિશેષ\*\*:\s*([^\n]+)', text)
    darshan_m3 = re.search(r'-\s*\*\*૩\.\s*અર્વાચીન-પ્રવેશ\*\*:\s*([^\n]+)', text)
    darshan_m4 = re.search(r'-\s*\*\*૪\.\s*સમન્વય-અશેષ\*\*:\s*([^\n]+)', text)

    darshan_p1 = darshan_m1.group(1).strip() if darshan_m1 else ""
    darshan_p2 = darshan_m2.group(1).strip() if darshan_m2 else ""
    darshan_p3 = darshan_m3.group(1).strip() if darshan_m3 else ""
    darshan_p4 = darshan_m4.group(1).strip() if darshan_m4 else ""

    # Image
    image_path = img_record['press_file'] if img_record else "Image/press/K01_C001_chapter_001_bhuta_naigam_naya_katha_r01_press.png"

    return {
        "title": title,
        "khanda_label": khanda_label,
        "aspect_label": aspect_label,
        "category_label": category_label,
        "sutra_text": sutra_text,
        "rupak_sub": rupak_sub,
        "rupak_body": rupak_body,
        "swarup_sub": swarup_sub,
        "swarup_body": swarup_body,
        "vyavahar_sub": vyavahar_sub,
        "vyavahar_body": vyavahar_body,
        "marm_sub": marm_sub,
        "marm_body": marm_body,
        "kavya_text": kavya_text,
        "sadhana_text": sadhana_text,
        "story_title": story_title,
        "pipasa_body": pipasa_body,
        "paan_body": paan_body,
        "ekant_body": ekant_body,
        "anekant_body": anekant_body,
        "darshan_p1": darshan_p1,
        "darshan_p2": darshan_p2,
        "darshan_p3": darshan_p3,
        "darshan_p4": darshan_p4,
        "image_path": image_path,
        "gender_fixes": fixes
    }

print("Chapter parser ready.")
