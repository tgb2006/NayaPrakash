"""Module to format and enrich all chapters of Sankshipt 2-Page A5 edition.

Rules enforced:
1. Reset chapter numbering after every khanda (1..N).
2. Consistent metadata header: *(મૂળ નય: ... | મુખ્ય શ્રેણી: ... | વ્યાખ્યા-સૂત્ર: ...)*
3. વ્યાખ્યા-સૂત્ર in Devanagari Sanskrit.
4. '## કથાધારા' on its own line, with story title as a subheading '### [વાર્તાનું નામ]'.
5. Global expansion of Vivekadhara (એકાંત દર્શન & અનેકાંત દર્શન) to full substantial paragraphs.
6. Everywhere 'પર્યાય' treated as masculine (પુલ્લિંગ: મારો પર્યાય, બદલાતો પર્યાય, વગેરે).
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, Tuple
from src.core.catalog_loader import CatalogLoader
from src.core.validator import ChapterValidator
from src.workflow.compiler import BookCompiler
from src.core.registry_manager import RegistryManager

GUJARATI_DIGITS = str.maketrans("0123456789", "૦૧૨૩૪૫૬૭૮૯")

def to_guj(n: int) -> str:
    return str(n).translate(GUJARATI_DIGITS)

def guj_to_dev(text: str) -> str:
    """Converts Gujarati script Sanskrit to Devanagari script."""
    res = []
    for ch in text:
        code = ord(ch)
        if 0x0A81 <= code <= 0x0AFF:
            res.append(chr(code - 0x0180))
        else:
            res.append(ch)
    return "".join(res)

def fix_paryaya_masculine(text: str) -> str:
    """Ensures all grammatical agreements with 'પર્યાય' are masculine (પુલ્લિંગ)."""
    t = text
    replacements = [
        (r'મારી\s+પર્યાય', 'મારો પર્યાય'),
        (r'તારી\s+પર્યાય', 'તારો પર્યાય'),
        (r'પોતાની\s+પર્યાય', 'પોતાનો પર્યાય'),
        (r'આવી\s+પર્યાય', 'આવો પર્યાય'),
        (r'તેવી\s+પર્યાય', 'તેવો પર્યાય'),
        (r'જેવી\s+પર્યાય', 'જેવો પર્યાય'),
        (r'બદલાતી\s+પર્યાય', 'બદલાતો પર્યાય'),
        (r'બદલાતી\s+પર્યાયો', 'બદલાતા પર્યાયો'),
        (r'પર્યાય\s+બદલાતી', 'પર્યાય બદલાતો'),
        (r'પર્યાયો\s+બદલાતી', 'પર્યાયો બદલાતા'),
        (r'બીજી\s+પર્યાય', 'બીજો પર્યાય'),
        (r'બીજી\s+પર્યાયો', 'બીજા પર્યાયો'),
        (r'નવી\s+પર્યાય', 'નવો પર્યાય'),
        (r'નવી\s+પર્યાયો', 'નવા પર્યાયો'),
        (r'જૂની\s+પર્યાય', 'જૂનો પર્યાય'),
        (r'મુક્તિની\s+પર્યાય', 'મુક્તિનો પર્યાય'),
        (r'સિદ્ધિની\s+પર્યાય', 'સિદ્ધિનો પર્યાય'),
        (r'આત્માની\s+પર્યાય', 'આત્માનો પર્યાય'),
        (r'જીવની\s+પર્યાય', 'જીવનો પર્યાય'),
        (r'પુદ્ગલની\s+પર્યાય', 'પુદ્ગલનો પર્યાય'),
        (r'શરીરની\s+પર્યાય', 'શરીરનો પર્યાય'),
        (r'દેહની\s+પર્યાય', 'દેહનો પર્યાય'),
        (r'જ્ઞાનની\s+પર્યાય', 'જ્ઞાનનો પર્યાય'),
        (r'સમયની\s+પર્યાય', 'સમયનો પર્યાય'),
        (r'ભવિષ્યની\s+પર્યાય', 'ભવિષ્યનો પર્યાય'),
        (r'અતીતની\s+પર્યાય', 'અતીતનો પર્યાય'),
        (r'વર્તમાનની\s+પર્યાય', 'વર્તમાનનો પર્યાય'),
        (r'બાળપણની\s+પર્યાય', 'બાળપણનો પર્યાય'),
        (r'રોગની\s+પર્યાય', 'રોગનો પર્યાય'),
        (r'પદાર્થની\s+પર્યાય', 'પદાર્થનો પર્યાય'),
        (r'કાળની\s+પર્યાય', 'કાળનો પર્યાય'),
        (r'ક્ષણની\s+પર્યાય', 'ક્ષણનો પર્યાય'),
        (r'પર્યાય\s+હતી', 'પર્યાય હતો'),
        (r'પર્યાય\s+પ્રગટેલી', 'પર્યાય પ્રગટેલો'),
        (r'પર્યાય\s+કેવી', 'પર્યાય કેવો'),
        (r'પર્યાય\s+સાચી', 'પર્યાય સાચો'),
        (r'એક\s+પર્યાયમાંથી\s+બીજી\s+પર્યાયમાં', 'એક પર્યાયમાંથી બીજા પર્યાયમાં'),
        (r'પુદ્ગલની\s+ક્ષણિક\s+પર્યાય', 'પુદ્ગલનો ક્ષણિક પર્યાય'),
        (r'જડ\s+પુદ્ગલની\s+બાહ્ય\s+પર્યાય', 'જડ પુદ્ગલનો બાહ્ય પર્યાય'),
        (r'પુદ્ગલની\s+પર્યાયનો', 'પુદ્ગલના પર્યાયનો'),
        (r'પર્યાયોની\s+અસ્થિરતા', 'પર્યાયોનો અસ્થિર પ્રવાહ'),
    ]
    for pattern, replacement in replacements:
        t = re.sub(pattern, replacement, t)
    return t

def enrich_vivekadhara_sections(text: str, kid: int, naya_name: str, validator: ChapterValidator) -> str:
    """Expands short Vivekadhara subsections to substantial, deep paragraphs while respecting word count budgets."""
    p = validator.parse_sections(text)
    if 4 not in p:
        return text
    viveka_body = p[4][1]
    
    total_w = validator.count_words(text)
    right_w = sum(p.get(i, ("", "", 0))[2] for i in [3, 4])
    avail_budget = min(655 - total_w, 345 - right_w)
    
    # If already at capacity, do not add more words
    if avail_budget < 20:
        return text
    
    m_ekanta = re.search(r'(###\s*\*{0,2}એકાંત[^\n]*\n+)(.*?)(?=\n+###\s*\*{0,2}અનેકાંત|\Z)', viveka_body, re.DOTALL)
    m_anekanta = re.search(r'(###\s*\*{0,2}અનેકાંત[^\n]*\n+)(.*)', viveka_body, re.DOTALL)
    
    if not (m_ekanta and m_anekanta):
        return text
        
    ekanta_txt = m_ekanta.group(2).strip()
    anekanta_txt = m_anekanta.group(2).strip()
    
    # Determine expansion style based on available budget
    is_concise = (avail_budget < 40)
    
    # Enrich Ekanta if short (< 36 words)
    if validator.count_words(ekanta_txt) < 36:
        if is_concise:
            add_e = 'આવી એકાંગી જીદથી સાધક મૂળ આત્મસત્તાને વિસરી જઈ સંકુચિતતામાં સબડે છે.'
        elif kid in [1, 2] or 'શુદ્ધ' in naya_name or 'નિશ્ચય' in naya_name:
            add_e = 'આવી એકાંત જડતાથી જીવ વર્તમાન વ્યવહારિક સાધના અને કર્તવ્યોની ઉપેક્ષા કરી બેસે છે અને ક્રમિક પરિણામોને સુધાર્યા વિના અકાળે પૂર્ણતાના મિથ્યા સંતોષમાં રાચે છે.'
        elif 'ઉપચાર' in naya_name or 'અસદ્ભૂત' in naya_name or 'પર્યાય' in naya_name:
            add_e = 'પરદ્રવ્યો કે ક્ષણિક સંયોગોને જ સર્વસ્વ માની લેવાથી મમત્વ અને પરિગ્રહનો ભાર વધે છે, જે ચિત્તને સદા આકુળ-વ્યાકુળ રાખી આધ્યાત્મિક જાગૃતિને રૂંધી નાખે છે.'
        elif kid in [5, 6]:
            add_e = 'શબ્દો કે વ્યાકરણના બાહ્ય નિયમોમાં જ અટવાઈ રહેવાથી અંતરંગ ભાવશુદ્ધિ ખોવાઈ જાય છે અને જીવ શુષ્ક વાદવિવાદ કે જડ ક્રિયાજડતામાં સબડતો રહે છે.'
        else:
            add_e = 'એક જ પાસાને પકડી રાખવાથી વસ્તુની સમગ્ર અનેકાંતમય સત્તા વિખંડિત થાય છે અને સાધક પોતાના જ એકાંગી આગ્રહના બંધનમાં ફસાઈને સાચી શાંતિ ગુમાવી બેસે છે.'
        ekanta_txt = ekanta_txt + ' ' + add_e
        
    # Enrich Anekanta if short (< 36 words)
    if validator.count_words(anekanta_txt) < 36:
        if is_concise:
            add_a = 'તે સમગ્રતાનો સમન્વય દર્શાવી સાધકને પરમ વિશ્રામમાં સ્થિર કરે છે.'
        elif kid in [1, 2] or 'શુદ્ધ' in naya_name or 'નિશ્ચય' in naya_name:
            add_a = 'તે આત્માની ત્રિકાળી ધ્રુવ સત્તાનો ભરોસો આપી સાધકને સંસારના ભયમાંથી મુક્ત કરે છે, જેથી ચેતના સહજ શાંતિમાં ડૂબી જઈ પરમ વિશ્રામ પામે છે.'
        elif 'ઉપચાર' in naya_name or 'અસદ્ભૂત' in naya_name or 'પર્યાય' in naya_name:
            add_a = 'તે વ્યવહારિક સંયોગોની મર્યાદા દર્શાવીને પણ આંતરિક ગુણો પ્રગટાવવાની પ્રેરણા આપે છે, જેથી સાધક નિજ ચૈતન્ય સ્વરૂપમાં મહામૌનમાં અંતર્લીન થઈ જાય છે.'
        elif kid in [5, 6]:
            add_a = 'તે વાણી અને સંજ્ઞાઓને આત્મજ્ઞાનનું સાધન બનાવી સાધકને નિર્વિકલ્પ અનુભૂતિ તરફ દોરી જાય છે, જેથી ચેતના નિરાકારમાં વિલીન થઈ પરમ તૃપ્તિ પામે છે.'
        else:
            add_a = 'તે સર્વ નયોના સંતુલન દ્વારા આત્માના વિરાટ સ્વરૂપનો સાક્ષાત્કાર કરાવે છે, જેથી જીવ સંસારના તમામ દ્વંદ્વો શમાવીને પરમાત્મામાં સમાઈ જાય છે.'
        anekanta_txt = anekanta_txt + ' ' + add_a
        
    new_viveka_sec = f'## વિવેકધારા\n\n### એકાંત દર્શન\n{ekanta_txt}\n\n### અનેકાંત દર્શન\n{anekanta_txt}'
    text = re.sub(r'##\s*વિવેકધારા.*$', new_viveka_sec, text, flags=re.DOTALL)
    return text

def process_chapter(content: str, kid: int, khanda_idx: int, naya_name: str, validator: ChapterValidator) -> str:
    """Transforms a chapter content to satisfy all requirements."""
    # 1. Update Title line: # {to_guj(khanda_idx)}. {clean_title}
    m_title = re.search(r'^#\s*[\d૦-૯\.]+\s*(.+)$', content, re.MULTILINE)
    clean_title = m_title.group(1).strip() if m_title else naya_name
    content = re.sub(r'^#\s*[\d૦-૯\.]+\s*.+$', f'# {to_guj(khanda_idx)}. {clean_title}', content, count=1, flags=re.MULTILINE)
    
    # 2. Update Metadata line: *(મૂળ નય: ... | મુખ્ય શ્રેણી: ... | વ્યાખ્યા-સૂત્ર: ...)*
    m_meta = re.search(r'\*\((.*?)\)\*', content)
    if m_meta:
        meta_content = m_meta.group(1)
        mul_naya = ''
        shreni = ''
        sutra = ''
        parts = meta_content.split('|')
        for p in parts:
            if 'મૂળ નય:' in p:
                mul_naya = p.split('મૂળ નય:')[1].strip()
            elif 'મુખ્ય શ્રેણી:' in p:
                shreni = p.split('મુખ્ય શ્રેણી:')[1].strip()
            elif any(k in p for k in ['આગમ સૂત્ર:', 'મૂળ સૂત્ર:', 'વ્યાખ્યા-સૂત્ર:']):
                for k in ['આગમ સૂત્ર:', 'મૂળ સૂત્ર:', 'વ્યાખ્યા-સૂત્ર:']:
                    if k in p:
                        sutra = p.split(k)[1].strip()
                        break
        dev_sutra = guj_to_dev(sutra)
        new_meta = f'*(મૂળ નય: {mul_naya} | મુખ્ય શ્રેણી: {shreni} | વ્યાખ્યા-સૂત્ર: {dev_sutra})*'
        content = content.replace(m_meta.group(0), new_meta)
        
    # 3. Update Kathadhara: ## કથાધારા\n\n### {story_title}
    m_katha = re.search(r'##\s*કથાધારા\s*:\s*([^\n]+)', content)
    if m_katha:
        story_name = m_katha.group(1).strip()
        content = content.replace(m_katha.group(0), f'## કથાધારા\n\n### {story_name}')
        
    # 4. Fix masculine 'પર્યાય'
    content = fix_paryaya_masculine(content)
    
    # 5. Enrich Vivekadhara
    content = enrich_vivekadhara_sections(content, kid, clean_title, validator)
    
    return content

def run_enrichment():
    bc = BookCompiler()
    cl = bc.loader
    val = ChapterValidator()
    reg = RegistryManager()
    
    total_processed = 0
    total_errors = 0
    
    for k in cl.get_khandas():
        kf = bc.output_dir / k.slug
        nayas = cl.get_nayas_by_khanda(k.id)
        print(f"\nProcessing Khanda {k.id}: {k.slug} ({len(nayas)} nayas)...")
        
        for idx, n in enumerate(nayas, 1):
            f = bc.find_chapter_file(kf, n.id)
            if not f:
                print(f"  [ERROR] File not found for naya ID {n.id}")
                total_errors += 1
                continue
                
            orig_text = f.read_text(encoding="utf-8")
            transformed_text = process_chapter(orig_text, k.id, idx, n.name_hindi, val)
            
            # Validate
            report = val.validate_content(transformed_text)
            if not report.is_valid:
                print(f"  [VALIDATION FAILED] K{k.id} Ch {idx} ({f.name}): {report.errors}")
                total_errors += 1
            else:
                f.write_text(transformed_text, encoding="utf-8")
                total_processed += 1
                
        print(f"Khanda {k.id} completed: {len(nayas)} chapters processed.")

    print(f"\n==========================================")
    print(f"Enrichment Complete: {total_processed} chapters updated, {total_errors} errors.")
    
    # Recompile Book and TOC
    print("\nRecompiling Master Book and Table of Contents...")
    master_path = bc.compile_full_book()
    toc_path = bc.generate_toc()
    print(f"Compiled Book: {master_path}")
    print(f"Generated TOC: {toc_path}")

if __name__ == "__main__":
    run_enrichment()
