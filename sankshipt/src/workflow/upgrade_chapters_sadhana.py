"""
Upgrade all 225 Sankshipt chapters:
1. Transform '## કાવ્યધારા' into side-by-side '## કાવ્યધારા અને સાધનાધારા' with authentic Adhyatma Upanaya / Sadhana-sutra.
2. In Chapters 21 to 30 (Dravyarthika in Vyavahara), add the clarifying reconciliation note (Problem 1 Solution).
3. Strictly maintain the masculine gender for 'પર્યાય'.
"""

import glob
import re
from pathlib import Path

BASE_DIR = Path(r"D:\PROJECT_WORK\NayaPrakash_Book")
SANKSHIPT_OUTPUT = BASE_DIR / "sankshipt" / "output"

# Explicit Adhyatmik Upanayas for key nayas from Dravya-Guna-Paryay no Ras & Canonical sources
EXPLICIT_SADHANA = {
    # Khanda 1: Naigama
    "chapter_001": "અતીતના પશ્ચાત્તાપ કે મોહમાં અટવાયા વિના, તેના પરિપાકને વર્તમાન આત્મજાગૃતિનું સબળ પ્રેરકબળ બનાવવું.",
    "chapter_002": "ભવિષ્યની ચિંતા કે આકાંક્ષાઓ છોડી, મુક્તિના દિવ્ય સંકલ્પને વર્તમાન સાધનામાં પુરુષાર્થરૂપે ઢાળવો.",
    "chapter_003": "આ પળમાં જ આત્માની સાચી પ્રાપ્તિ છે એવા પ્રબળ પુરુષાર્થ સાથે વર્તમાન ક્ષણમાં સદા જાગ્રત રહેવું.",
    "chapter_062": "અતીતની શુભ સાધનાના સંસ્કારોનું સ્મરણ કરી વર્તમાન જીવનમાં ધર્મધ્યાનને દૃઢ બનાવવું.",
    "chapter_063": "આગામી કલ્યાણકારી અવસ્થાના વિશ્વાસ સાથે વર્તમાનમાં સદાચાર અને વ્રત-નિયમોનું પાલન કરવું.",
    "chapter_064": "પ્રત્યેક ક્રિયાના વર્તમાન પરિણામ પ્રત્યે સભાન રહી પ્રમાદનો ત્યાગ કરવો.",
    
    # Khanda 2: Sangraha
    "chapter_004": "વિશ્વના સર્વ જીવોમાં એક સમાન ચૈતન્ય સત્તા નિહાળી મૈત્રીભાવ અને અભેદ દૃષ્ટિ કેળવવી.",
    "chapter_005": "જીવ અને અજીવના મૂળભૂત ભેદને સમજી ચૈતન્ય સ્વરૂપમાં જ આત્મભાવ સ્થાપવો.",
    "chapter_006": "સમસ્ત આત્માઓ સ્વભાવથી શુદ્ધ છે એવા દર્શનથી સર્વ જીવો પ્રત્યે અહંકારશૂન્ય સમભાવ રાખવો.",
    "chapter_007": "મુક્ત સિદ્ધ ભગવંતોના ગુણોનું ચિંતન કરી પોતાના આત્મામાં પણ તે જ મુક્ત સ્વભાવ પ્રગટાવવો.",
    "chapter_008": "સંસારી જીવોના વિવિધ ભવ-ભ્રમણને જોઈ સંસાર પ્રત્યે પરમ વૈરાગ્યભાવ દૃઢ કરવો.",
    
    # Khanda 3: Vyavahara (including Dravyarthika 21-30)
    "chapter_021": "પોતાને પાપી કે દીન માનવાને બદલે, રાગ-દ્વેષના કાદવથી સદા અસ્પૃષ્ટ સિદ્ધસ્વરૂપનું અંતરંગ આત્મગૌરવ જગાડવું.",
    "chapter_022": "પર્યાયના ક્ષણિક ઉતાર-ચઢાવથી અપ્રભાવિત રહી, ત્રિકાળી ધ્રુવ ચૈતન્ય સત્તામાં ચિત્તને અડગ સ્થિર કરવું.",
    "chapter_023": "ગુણ અને ગુણીના માનસિક વિકલ્પો છોડી, અખંડ એકત્વરૂપ શુદ્ધ આત્મદ્રવ્યમાં લીન થવું.",
    "chapter_024": "વર્તમાન વિભાવ અને દોષોને સ્વીકારીને પ્રમાદ ત્યજી આત્મશુદ્ધિના પુરુષાર્થમાં સદા જાગ્રત થવું.",
    "chapter_024_1": "ઉપાધિઓના અભાવે પ્રગટ થતી સહજ શુદ્ધતાને ઓળખી અસંગ ભાવમાં સ્થિર રહેવું.",
    "chapter_024_2": "શુદ્ધ ભાવોની ઉપેક્ષા કર્યા વિના નિષ્કપટ ભાવે સ્વરૂપ તરફ ડગ માંડવા.",
    "chapter_025": "એક જ સમયમાં કર્મ-ક્ષય અને ગુણ-પ્રાગટ્યના ક્રમને ઓળખી અધ્યાત્મ પંથે ધીરજપૂર્વક આગળ વધવું.",
    "chapter_026": "સાધનાના પ્રારંભે ગુણભેદ દ્વારા આત્મગુણોની ઉપાસના કરી ક્રમશઃ પરમ અભેદ તરફ વળવું.",
    "chapter_027": "તમામ બાહ્ય અને આંતરિક પરિવર્તનો વચ્ચે આત્માના સતત વહેતા અન્વય ચૈતન્ય પ્રવાહને અનુભવવો.",
    "chapter_028": "સ્વસ્વરૂપની અનંત ગુણ-સંપત્તિમાં જ સંતોષ માની, પરદ્રવ્યની તમામ વાસનાઓથી મુક્ત થવું.",
    "chapter_029": "પરભાવો મારા નથી એવા નિર્મળ ભેદજ્ઞાન વડે પરભાવોથી ચિત્તને તત્કાળ પાછું વાળી લેવું.",
    "chapter_030": "ક્ષાયિક-ઔપશમિક આદિ સર્વ અવસ્થાઓથી પર કેવળ શુદ્ધ પારિણામિક પરમભાવમાં આત્મવિશ્રામ પામવો.",
    "chapter_030_1": "કર્મજન્ય સર્વ ઉપાધિઓથી રહિત શુદ્ધ પારિણામિક ચૈતન્ય ધાતુમાં જ અનન્ય શરણ શોધવું.",
    "chapter_069_1": "આત્મા અને જ્ઞાન-દર્શન ગુણોની અભેદતા ઓળખી આંતરિક રત્નત્રયની આરાધનામાં લીન થવું.",
    "chapter_103": "દેહ અને મનની ક્રિયાઓને ઉપાધિજન્ય જાણી તેના કર્તાપણાના અભિમાનમાંથી મુક્ત થવું.",
    "chapter_104": "જ્ઞાનમાં પ્રતિબિંબિત થતા જ્ઞેયોમાં રાગ-દ્વેષ કર્યા વિના કેવળ સાક્ષીભાવ જાળવવો.",
    "chapter_105": "આત્માના સ્વાભાવિક પરિણામોનું સેવન કરી પરભાવોના ભારમાંથી સહજ મુક્તિ પામવી.",
    "chapter_129": "શરીર અને બાહ્ય ઉપકરણો સાથેના સંબંધને સાધન માત્ર સમજી મોહના બંધનો શિથિલ કરવાં.",
    
    # Khanda 4: Rjusutra
    "chapter_035": "જગતની અકૃત્રિમ અનંત રચના વચ્ચે લોકાલોકના સાક્ષીરૂપ બની પોતાના શાશ્વત ચૈતન્યભાવને અનુભવવો.",
    "chapter_036": "મોક્ષપર્યાય સાદિ-અનંત છે એવા વિશ્વાસથી આત્મસાધનામાં અડગ નિષ્ઠા કેળવવી.",
    "chapter_057": "ક્ષણભંગુર બાહ્ય સૃષ્ટિમાં અડગ મેરુ સમાન પોતાના ત્રિકાળી ધ્રુવ આત્મસ્વભાવમાં સ્થિર થવું.",
    "chapter_058": "મુક્ત અવસ્થા અવિનાશી છે તે લક્ષ્ય રાખી વર્તમાન પરિણામોને નિર્મળ બનાવવાનો પુરુષાર્થ કરવો.",
    "chapter_059": "સંસારના ક્ષણિક સુખ-દુઃખના પર્યાયોમાં મોહિત થયા વિના સદા અલિપ્ત સાક્ષીભાવ કેળવવો.",
    "chapter_060": "પ્રત્યેક પળે ઉત્પન્ન-વિનષ્ટ થતા જ્ઞાનપર્યાયમાં અંતર્ગત જ્ઞાયક સ્વભાવને અખંડ નિહાળવો.",
    "chapter_061": "શરીરાદિ ઉપાધિ વચ્ચે પણ આત્માના મૂળ ધર્મ અને સત્ય પ્રત્યે સદા સજાગ રહેવું.",
    "chapter_153": "પર્યાયના ક્ષણિક ઉદયને જોઈ વ્યથિત ન થતાં અંતર્ગત અમર ચૈતન્યદ્રવ્યનું શરણ લેવું.",
    
    # Khanda 5: Shabda
    "chapter_041": "શબ્દો અને વચનોના વ્યામોહથી મુક્ત થઈ શબ્દાતીત આત્મતત્વમાં ધ્યાનાવસ્થિત થવું.",
    "chapter_154": "આત્મા સત્ સ્વરૂપ છે એવા દૃઢ નિશ્ચય સાથે પોતાના અસ્તિત્વના અનંત આનંદને માણવો.",
    "chapter_155": "પરભાવો મારામાં નથી એવા નાસ્તિત્વ બોધથી પરના આકર્ષણમાંથી મુક્ત થવું.",
    "chapter_156": "સ્વમાં અસ્તિ અને પરમાં નાસ્તિના સમન્વયથી પરમ સ્વાધીનતાનો અનુભવ કરવો.",
    
    # Khanda 6: Samabhirudha
    "chapter_042": "રૂઢિગત સંજ્ઞાઓ ઓળંગીને પદાર્થના સૂક્ષ્મ પરમાર્થ સ્વરૂપમાં પ્રવેશ કરવો.",
    "chapter_161": "સાધનાના વિવિધ વિકલ્પોનો વિવેકપૂર્વક ઉપયોગ કરી ચિત્તને શુદ્ધ બનાવવું.",
    "chapter_162": "સર્વ વિકલ્પો શાંત થતાં નિર્વિકલ્પ આત્મસમાધિમાં પરમ વિશ્રામ પામવો.",
    "chapter_169": "આત્મા નિત્ય અને અવિનાશી છે એવા બોધથી મૃત્યુ અને વિનાશના ભયમાંથી મુક્ત થવું.",
    "chapter_170": "પરિસ્થિતિઓ અનિત્ય છે તે સમજી અનુકૂળ-પ્રતિકૂળ સંજોગોમાં સદા સમતા ધારણ કરવી.",
    
    # Khanda 7: Evambhuta
    "chapter_043": "કેવળ નામના સાધુ કે જ્ઞાની બનવાને બદલે વાસ્તવિક આત્મગુણોના આચરણમાં તન્મય થવું.",
    "chapter_195": "વ્યવહારની ધાર્મિક ક્રિયાઓ અને સદાચારને મોક્ષમહેલની પવિત્ર સીડી સમજી સાદર આચરવાં.",
    "chapter_196": "બંધ અને મોક્ષના વિકલ્પોથી પર થઈ, ત્રિકાળ અસંગ અને નિત્ય શુદ્ધ આત્મતત્વમાં પરમ વિશ્રામ પામવો.",
    "chapter_197": "સાંસારિક વિભાવો પ્રત્યે સભાન થઈ અંતરંગ શુદ્ધિ અર્થે તપ-સંયમનો માર્ગ અંગીકાર કરવો.",
    "chapter_198": "સર્વ ઉપાધિઓથી મુક્ત કેવળ નિરુપાધિક જ્ઞાતા-દ્રષ્ટા સ્વભાવમાં સ્થિર રહેવું."
}

RECONCILIATION_NOTE = """*(વિશેષ શાસ્ત્રીય સમન્વય: આ નય વિષયની દ્રષ્ટિએ દ્રવ્યસ્વભાવગ્રાહી હોવાથી 'દ્રવ્ય-ગુણ-પર્યાયનો રાસ' (મહોપાધ્યાય શ્રી યશોવિજયજી) માં મૂળ **દ્રવ્યાર્થિકનય** તરીકે સ્થાપિત છે, જ્યારે પ્રતિપાદન પદ્ધતિ ભેદવિષયક હોવાથી પંચાધ્યાયી અનુસાર **વ્યવહાર ખંડ** માં મૂકાયો છે — બંને દ્રષ્ટિ પરસ્પર પૂરક છે.)*"""

def clean_sadhana_text(text: str) -> str:
    # Ensure correct Gujarati grammar: 'પર્યાય' is strictly masculine
    text = text.replace("પર્યાય થઈ", "પર્યાય થયો")
    text = text.replace("પર્યાય બદલાઈ", "પર્યાય બદલાયો")
    text = text.replace("દ્રવ્યની પર્યાય", "દ્રવ્યનો પર્યાય")
    text = text.replace("તેની પર્યાય", "તેનો પર્યાય")
    text = text.replace("બધી પર્યાયો", "બધા પર્યાયો")
    
    # Clean leading/trailing boilerplate
    text = re.sub(r'^(આ નય|તે સાધકને|આ વિચાર|આ નય દ્વારા|આથી|સાધકે|અહીં|તેથી)\s*', '', text)
    text = text.strip()
    return text

def get_best_sadhana(fname: str, content: str) -> str:
    stem = Path(fname).stem
    for k, v in EXPLICIT_SADHANA.items():
        if k in stem:
            return v
            
    candidates = []
    
    # Check Marma-tushti
    m_marma = re.search(r'\*\*૪\.\s*મર્મ-તુષ્ટિ[^*]*\*\*[:\s]*(.*?)(?=\n##|\n\*\*|$)', content, re.S)
    if m_marma:
        raw = re.sub(r'[*_#]', '', m_marma.group(1)).replace('\n', ' ')
        raw = re.sub(r'\s+', ' ', raw).strip()
        for s in re.split(r'[.!?।]', raw):
            s = s.strip()
            if 30 <= len(s) <= 150 and not s.startswith("જો") and not s.startswith("આ નય વગર") and not s.startswith("આ નય વિના"):
                candidates.append((s, 2))
                
    # Check Anekanta Darshana
    m_an = re.search(r'### અનેકાંત દર્શન\s*(.*?)(?=\n##|\n---|---|$)', content, re.S)
    if m_an:
        raw = re.sub(r'[*_#]', '', m_an.group(1)).replace('\n', ' ')
        raw = re.sub(r'\s+', ' ', raw).strip()
        for s in re.split(r'[.!?।]', raw):
            s = s.strip()
            if 30 <= len(s) <= 150 and not s.startswith("જો") and not s.startswith("આ નય વગર"):
                candidates.append((s, 1))

    keywords = ["સાધક", "આત્મા", "ચૈતન્ય", "શાંતિ", "મુક્તિ", "વિવેક", "સમભાવ", "પુરુષાર્થ", "જાગૃતિ", "સ્થિર", "સ્વરૂપ", "સંસાર", "અભય", "ધ્યાન", "આત્મવિશ્વાસ"]
    best_candidate = None
    best_score = -1
    
    for c, weight in candidates:
        score = weight * 5
        for kw in keywords:
            if kw in c:
                score += 3
        if any(w in c for w in ["પ્રકરણ", "પુસ્તક", "લેખક"]):
            score -= 10
        if score > best_score:
            best_score = score
            best_candidate = c
            
    if best_candidate:
        s = clean_sadhana_text(best_candidate)
        s = re.sub(r'\s*છે\s*$', ' છે.', s)
        s = re.sub(r'\s*કરે છે\s*$', ' કરી આંતરિક શાંતિ અનુભવવી.', s)
        s = re.sub(r'\s*આપે છે\s*$', ' મેળવી સ્વરૂપમાં સ્થિર થવું.', s)
        s = re.sub(r'\s*જગાવે છે\s*$', ' જગાવી સાધનામાં સજાગ રહેવું.', s)
        if not s.endswith("."): s += "."
        return s

    return "સ્વરૂપની ગહન સ્થિરતા કેળવી આંતરિક જાગૃતિ સાથે પરમ સમભાવમાં લીન થવું."

def process_chapter(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    original = content
    fname = file_path.name

    # 1. Check if Problem 1 note is needed (Ch 21-30 in khanda_3_vyavahar)
    is_dravyarthika_in_khanda3 = (
        "khanda_3_vyavahar" in str(file_path) and 
        any(k in fname for k in ["chapter_021", "chapter_022", "chapter_023", "chapter_024", "chapter_025", 
                                "chapter_026", "chapter_027", "chapter_028", "chapter_029", "chapter_030"])
    )
    
    if is_dravyarthika_in_khanda3 and "વિશેષ શાસ્ત્રીય સમન્વય" not in content:
        # Insert reconciliation note after subtitle before the first '---'
        m_head = re.search(r'^(# [^\n]+\n\*\([^\n]+\)\*)\n\n---', content, re.M)
        if m_head:
            rep = m_head.group(1) + "\n" + RECONCILIATION_NOTE + "\n\n---"
            content = content[:m_head.start()] + rep + content[m_head.end():]

    # 2. Transform '## કાવ્યધારા' into side-by-side table '## કાવ્યધારા અને સાધનાધારા'
    m_kavya = re.search(r'## કાવ્યધારા\s*\n(.*?)(?=\n---|\n##|$)', content, re.S)
    if m_kavya:
        kavya_raw = m_kavya.group(1).strip()
        raw_lines = [l.strip() for l in kavya_raw.splitlines() if l.strip()]
        kavya_col = "<br>".join(l.replace("|", "\\|") for l in raw_lines)
        
        sadhana_text = get_best_sadhana(fname, original).replace("|", "\\|")
        
        new_kavya_sec = f"""## કાવ્યધારા અને સાધનાધારા

| 📜 કાવ્યધારા | ✦ સાધનાધારા |
|:---|:---|
| {kavya_col} | {sadhana_text} |"""

        start, end = m_kavya.span()
        content = content[:start] + new_kavya_sec + content[end:]
        
    if content != original:
        file_path.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    files = list(SANKSHIPT_OUTPUT.glob("**/chapter_*.md"))
    print(f"Found {len(files)} chapter files to process.")
    
    modified_count = 0
    for f in sorted(files):
        if process_chapter(f):
            modified_count += 1
            
    print(f"Successfully upgraded {modified_count} chapters!")

if __name__ == "__main__":
    main()
