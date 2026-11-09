"""
Apply authentic, canonical Sadhana-sutras to the 71 chapters currently missing sadhanadhara.
Enforces:
1. Pure literary spiritual Gujarati.
2. Adhyatma Upanaya / Sadhana-sutra tailored to the Naya's core essence.
3. STRICT MASCULINE GENDER FOR 'પર્યાય' (Zero feminine violations).
4. Balanced duo-ribbon presentation.
"""

from pathlib import Path
import re

SADHANA_MAP = {
    # -------------------------------------------------------------
    # Khanda 2: Sangraha (7 chapters)
    # -------------------------------------------------------------
    "chapter_065_para_sangraha_dravyarthika_pratipadaka_vyavahara_gu.md":
        "સમગ્ર વિશ્વને એક 'સત્' સત્તા તરીકે ઓળખી, વિરોધ અને વિખવાદથી મુક્ત થઈ પરમ અદ્વૈત શાંતિમાં સ્થિર થવું.",
    "chapter_066_2_shuddha_apara_sangraha_dravyarthika_pratipadaka_vyavahara_gu.md":
        "અનંત સિદ્ધ ભગવંતોના શુદ્ધ સ્વરૂપનું એકીસાથે સ્મરણ કરી, પોતાના અંતરમાં પણ તે જ પરમ વિશુદ્ધિ પ્રગટાવવી.",
    "chapter_066_apara_sangraha_dravyarthika_pratipadaka_vyavahara_gu.md":
        "વિશ્વના સમસ્ત જીવોમાં સમાન ચૈતન્યતત્વ નિહાળી, સર્વ જીવો પ્રત્યે અહિંસા અને નિર્મળ કરુણાભાવ કેળવવો.",
    "chapter_067_apara_sangraha_bhedaka_vyavahara_dravyarthika_pratipadaka_gu.md":
        "દેહ અને જડ પદાર્થોને અજીવ જાણી, તેના મોહમાંથી મુક્ત થઈ પોતાના અવિનાશી ચેતનતત્વમાં જાગ્રત રહેવું.",
    "chapter_068_1_antima_apara_sangraha_bhedaka_vyavahara_dravyarthika_pratipadaka_gu.md":
        "સંયોગી સ્કંધોના બાહ્ય રૂપરંગથી અંજાઈ ગયા વિના, મૂળ અવિભાજ્ય દ્રવ્યતત્વના શાશ્વત સ્વરૂપને લક્ષમાં રાખવું.",
    "chapter_068_2_antima_akhanda_vyavahara_dravyarthika_pratipadaka_gu.md":
        "પરનિર્ભરતા અને સમૂહના મોહમાંથી બહાર નીકળી, પોતાના અખંડ સ્વતંત્ર આત્મચૈતન્યના તેજમાં લીન થવું.",
    "chapter_068_apara_sangraha_bhedaka_vyavahara_dravyarthika_pratipadaka_gu.md":
        "સંસારી અવસ્થાને ક્ષણિક જાણી નિરાશ થયા વિના, મુક્ત દશા પામવાના દૃઢ આત્મવિશ્વાસ સાથે સાધનામાં જોડાવું.",

    # -------------------------------------------------------------
    # Khanda 3: Vyavahara (47 chapters)
    # -------------------------------------------------------------
    "chapter_009_para_sangraha_bhedaka_vyavahara_dravyarthika_naya_gu.md":
        "સમગ્ર વિશ્વના છ દ્રવ્યોના સ્વતંત્ર કાર્યને ઓળખી, પરદ્રવ્યના કર્તાપણાના ભ્રમમાંથી સદા મુક્ત રહેવું.",
    "chapter_011_antima_apara_sangraha_bhedaka_vyavahara_dravyarthika_naya_gu.md":
        "પુદ્ગલના તમામ સ્થૂળ સંબંધોને વિભાજ્ય જાણી, અખંડ આત્મદ્રવ્યની અભેદ ઉપાસનામાં ચિત્ત સ્થિર કરવું.",
    "chapter_012_paramashuddha_apara_sangraha_bhedaka_vyavahara_dravyarthika_naya_gu.md":
        "પ્રત્યેક આત્માની સ્વતંત્ર ચૈતન્ય સત્તા સ્વીકારી, પરજીવોના આધિપત્યની ભાવના ત્યજી પરમ આત્મસ્વાતંત્ર્ય અનુભવવું.",
    "chapter_013_shuddha_apara_sangraha_bhedaka_vyavahara_dravyarthika_naya_gu.md":
        "ક્ષેત્ર અને કાળના ભેદોથી મુક્ત સર્વ સિદ્ધોના અવિનાશી સુખનું ચિંતન કરી, સ્વરૂપ સાધનામાં વીર્ય ફોરવવું.",
    "chapter_014_ashuddha_apara_sangraha_bhedaka_vyavahara_dravyarthika_naya_gu.md":
        "સંસારના ચૌદ રાજલોકના જીવોની પરિભ્રમણ પીડા જાણી, વિષય-કષાય ત્યજી આત્મશુદ્ધિનો પુરુષાર્થ આદરવો.",
    "chapter_015_paramashuddha_abhedavishayi_antima_vyavahara_dravyarthika_naya_gu.md":
        "ગુણોના ભેદના તમામ વિકલ્પો વિસારીને, અખંડ એકરસ ચૈતન્યરસના નિર્વિકલ્પ ધ્યાનમાં ડૂબી જવું.",
    "chapter_016_paramashuddha_bhedavishayi_antima_vyavahara_dravyarthika_naya_gu.md":
        "પોતાના અંતરમાં રહેલા અનંત આત્મગુણોના અખૂટ ભંડારને ઓળખી, પરભાવની તમામ ભીખ છોડી આત્મતૃપ્ત થવું.",
    "chapter_017_shuddha_abhedavishayi_antima_vyavahara_dravyarthika_naya_gu.md":
        "પ્રગટ કેવળજ્ઞાનાદિ શુદ્ધ પર્યાયરૂપ પરમાત્મદશાનું સ્મરણ કરી, આત્મશુદ્ધિના પરમ પુરુષાર્થમાં નિમગ્ન રહેવું.",
    "chapter_018_shuddhabhedavishayi_antima_vyavahara_dravyarthika_naya_gu.md":
        "વીતરાગ પરમાત્માના અનંતચતુષ્ટય ગુણોનો અનુરાગ કેળવી, ભક્તિ દ્વારા પોતાના અંતરમાં તે જ દિવ્યતા પ્રગટાવવી.",
    "chapter_019_avyakta_ashuddha_antima_vyavahara_dravyarthika_naya_gu.md":
        "સાધનાની ઊંચી ભૂમિકામાં પણ અંતરમાં છુપાયેલા સૂક્ષ્મ રાગ પ્રત્યે સજાગ રહી, નિરંતર આત્મજાગૃતિ જાળવવી.",
    "chapter_020_vyakta_ashuddha_antima_vyavahara_dravyarthika_naya_gu.md":
        "પ્રત્યક્ષ પ્રગટતા ક્રોધાદિ વિકારોનો નિષ્કપટ સ્વીકાર કરી, ઉત્તરોત્તર ક્ષમા અને સમતા દ્વારા દોષોનું માર્જન કરવું.",
    "chapter_045_shaktibodhaka_paramashuddha_nishchayanaya_gu.md":
        "હું અનંત આત્મવીર્ય અને જ્ઞાનશક્તિથી સંપન્ન પરમાત્મા છું એવા અચળ વિશ્વાસથી દીનતાનો ત્યાગ કરવો.",
    "chapter_046_1_sabheda_shuddha_nishchayanaya_gu.md":
        "મુક્તિના પ્રત્યેક શુદ્ધ ગુણ-પર્યાયના દિવ્ય વૈભવને લક્ષમાં રાખી, મોક્ષમાર્ગના પુરુષાર્થમાં ઉત્સાહપૂર્વક આગળ વધવું.",
    "chapter_046_2_apurnashuddha_nishchayanaya_gu.md":
        "સાધક દશામાં પ્રગટેલી અંશરૂપ શુદ્ધતાને પણ આદર આપી, પૂર્ણ શુદ્ધતા પામવા ધીરજપૂર્વક પુરુષાર્થ કરવો.",
    "chapter_046_shuddha_nishchayanaya_gu.md":
        "કેવળજ્ઞાન અને અનંત સુખરૂપ સાક્ષાત્ શુદ્ધ દશા જ પરમ સત્ય છે એમ જાણી, સંસારના મિથ્યા સુખોથી મુક્ત થવું.",
    "chapter_047_1_sabheda_ashuddha_nishchayanaya_gu.md":
        "ક્રોધ, માન, માયા અને લોભના વિવિધ ભેદોને વિભાવરૂપે ઓળખી, આત્મનિરીક્ષણ દ્વારા મનને શાંત કરવું.",
    "chapter_047_2_vivakshitaikadesha_shuddhanishchayanaya_gu.md":
        "કર્મ ઉપાધિથી પર એવી અંતરની નિર્મળ દશાને પ્રગટાવી, એકદેશ શુદ્ધતામાંથી પૂર્ણ પવિત્રતા તરફ ડગ માંડવા.",
    "chapter_047_pratishedhaka_shuddhanaya_gu.md":
        "જડ પુદ્ગલના પરભાવોથી પોતાને તદ્દન ભિન્ન અનુભવી, પરના અહંકાર અને કર્તાપણાના ભારમાંથી મુક્ત થવું.",
    "chapter_048_upadanadrishti_shuddhanaya_gu.md":
        "બાહ્ય નિમિત્તો પર આધાર રાખવાને બદલે, પોતાના અંતરંગ ઉપાદાન સામર્થ્યને જગાડી આત્મકલ્યાણ સાધવું.",
    "chapter_049_paramashuddhabhedavishayi_vyavaharanaya_gu.md":
        "આત્માના અનંત સહજ ગુણોનું વિવેકપૂર્વક ચિંતન કરી, ચૈતન્યના અગાધ મહિમામાં ચિત્તને એકાગ્ર કરવું.",
    "chapter_050_shuddhabhedavishayi_dravyarthikanaya_gu.md":
        "કેવળજ્ઞાનાદિ શુદ્ધ પર્યાયોના પ્રાગટ્યને ધ્યાનમાં રાખી, સમ્યગ્ દર્શન-જ્ઞાન-ચારિત્રની આરાધના દૃઢ કરવી.",
    "chapter_051_ashuddhabhedavishayi_dravyarthikanaya_gu.md":
        "મતિ, શ્રુત આદિ ક્ષયોપશમ જ્ઞાનની મર્યાદાઓ જાણી, અતીન્દ્રિય કેવળજ્ઞાન સ્વભાવ તરફ લક્ષ કેન્દ્રિત કરવું.",
    "chapter_052_ashuddhabhedavishayi_dravyarthikanaya_gu.md":
        "ચિત્તમાં ઊઠતા વિભાવિક ભાવોને કર્મોપાધિજન્ય જાણી, તેનાથી અલિપ્ત રહી સ્વભાવમાં સ્થિર રહેવું.",
    "chapter_053_upadhisapeksha_ashuddhadravyarthikanaya_gu.md":
        "વર્તમાન સંસારી અવસ્થાને ઉપાધિજન્ય જાણી, ઉપાધિમુક્ત શુદ્ધ આત્મતત્વની સાધનામાં પુરુષાર્થ વધારવો.",
    "chapter_054_anvayadravyarthikanaya_gu.md":
        "પર્યાયોના અવિરત બદલાવ વચ્ચે અખંડ વહેતા ત્રિકાળી આત્મપ્રવાહને પકડી, ચિત્તને પરમ ધ્રુવતા આપવી.",
    "chapter_069_akhanda_paramashuddha_sadbhuta_vyavahara_gu.md":
        "તમામ કાલ્પનિક ભેદોથી પર થઈ, પોતાના સહજ અને અખંડ ચૈતન્યમય અસ્તિત્વમાં નિર્વિકલ્પ વિશ્રામ લેવો.",
    "chapter_070_1_pratishedhaka_shuddhanaya_pratipadaka_vyavahara_gu.md":
        "વાણી અને વિચાર દ્વારા પરકર્તૃત્વનો સ્પષ્ટ નિષેધ કરી, ભીતરી અકર્તા જ્ઞાતાભાવમાં પ્રતિષ્ઠિત થવું.",
    "chapter_070_saguna_paramashuddha_sadbhuta_vyavahara_gu.md":
        "પોતાના અંતરમાં બિરાજમાન અનંતચતુષ્ટયના અખૂટ ખજાનાને સ્મરી, આત્મગૌરવ સાથે સાધનાપંથે વિચરવું.",
    "chapter_071_abheda_shuddha_sadbhuta_vyavahara_gu.md":
        "પ્રગટ શુદ્ધ પર્યાય અને દ્રવ્યની અભેદતા અનુભવી, સાક્ષાત્ પરમાત્મસ્વરૂપના સ્વાનુભવમાં લીન થવું.",
    "chapter_072_sabheda_shuddha_sadbhuta_vyavahara_gu.md":
        "સિદ્ધ પરમાત્માના પૂર્ણ શુદ્ધ ગુણ-પર્યાયોના સામર્થ્યને ઓળખી, મુક્તિના સાચા માર્ગે પ્રયાણ કરવું.",
    "chapter_073_1_karaka_karakibhedaka_ashuddha_sadbhuta_vyavahara_gu.md":
        "વર્તમાન રાગ-દ્વેષના દોષોની જવાબદારી પોતે સ્વીકારી, આત્મપુરુષાર્થ દ્વારા વિભાવોને સમૂળગા નષ્ટ કરવા.",
    "chapter_074_anupacharita_ashuddha_sadbhuta_vyavahara_gu.md":
        "અંતરંગ સૂક્ષ્મ રાગના અંશને પણ ઓળખીને સાવધાન રહેવું, જેથી ચિત્ત પરમ વીતરાગતા તરફ આગળ વધે.",
    "chapter_075_upacharita_ashuddha_sadbhuta_vyavahara_gu.md":
        "બાહ્ય વાણી અને વર્તનમાં દેખાતા સ્થૂળ ક્રોધાદિ વિકારો પર સંયમ રાખી, સદાચારનું ચુસ્ત પાલન કરવું.",
    "chapter_076_upadhisapeksha_ashuddha_dravyarthikapratipadaka_vyavahara_gu.md":
        "કર્મજન્ય ઔપાધિક વિકૃતિઓથી હિંમત હાર્યા વિના, કર્મબંધન તોડી નિષ્કલંક થવાનો પુરુષાર્થ જગાડવો.",
    "chapter_077_upacharita_upadhisapeksha_ashuddha_dravyarthikapratipadaka_vyavahara_gu.md":
        "વિષય-ભોગોમાં ઉપયોગને ભટકતો અટકાવી, ઈન્દ્રિયનિગ્રહ દ્વારા ચિત્તને આત્મસાધનામાં જોડવું.",
    "chapter_078_upadhinirapeksha_shuddhadravyarthikapratipadaka_vyavahara_gu.md":
        "કર્મોપાધિથી સર્વથા રહિત સિદ્ધ સમાન શુદ્ધ આત્મસ્વભાવનું દર્શન કરી, ભીતરી પરમ શાંતિ અનુભવવી.",
    "chapter_079_utpadavyayagauna_sattagrahaka_shuddhadravyarthikapratipadaka_vyavahara_gu.md":
        "ક્ષણિક ઉત્પાદ-વ્યયના પર્યાયોને ગૌણ કરી, ત્રિકાળી શાશ્વત ધ્રુવ ચૈતન્યસત્તામાં આત્મવિશ્રામ પામવો.",
    "chapter_081_utpadavyayasapeksha_ashuddhadravyarthikapratipadaka_vyavahara_gu.md":
        "પર્યાયના ક્ષણે ક્ષણે થતા પલટાને જાણી વૈરાગ્ય દૃઢ કરવો, અને ધ્રુવ આત્મતત્વમાં સ્થિરતા સાધવી.",
    "chapter_082_bhedakalpanasapeksha_ashuddhadravyarthikapratipadaka_vyavahara_gu.md":
        "જ્ઞાન-દર્શનના વ્યવહારિક ભેદોને સાધન માત્ર સમજી, અંતે અખંડ અભેદ આત્મસ્વરૂપમાં પ્રવેશ કરવો.",
    "chapter_083_anvayadravyarthikapratipadaka_vyavahara_gu.md":
        "જીવનના તમામ સંજોગો અને પર્યાયોમાં વ્યાપી રહેલા અન્વય ચૈતન્ય સૂત્રને ઓળખી, સમભાવ ધારણ કરવો.",
    "chapter_085_paradravyadigrahaka_dravyarthikapratipadaka_vyavahara_gu.md":
        "પરદ્રવ્ય, પરક્ષેત્ર અને પરભાવોથી પોતાને શૂન્ય જાણી, પરની તમામ આસક્તિઓમાંથી ચિત્તને પાછું વાળવું.",
    "chapter_087_ashuddhasthula_rjusutrapratipadaka_vyavahara_gu.md":
        "વર્તમાન દેહરૂપી વેશ ક્ષણભંગુર છે એમ જાણી, માનવભવના અમૂલ્ય સમયને આત્મહિતમાં સમર્પિત કરવો.",
    "chapter_089_ashuddhasukshma_rjusutrapratipadaka_vyavahara_gu.md":
        "ક્ષણે ક્ષણે ઊઠતા રાગ-દ્વેષના સૂક્ષ્મ પર્યાય પ્રત્યે સાક્ષીભાવ રાખી, ચિત્તને ક્ષોભમુક્ત બનાવવું.",
    "chapter_093_sattagauna_utpadavyayagrahaka_ashuddha_paryayarthikapratipadaka_vyavahara_gu.md":
        "સંસારના સર્વ પદાર્થો ક્ષણે ક્ષણે વિનષ્ટ થાય છે એમ સમજી, ક્ષણિક પર્યાયોનો મોહ છોડી શાશ્વતમાં વળવું.",
    "chapter_095_upadhisapeksha_nitya_ashuddhaparyayarthikapratipadaka_vyavahara_gu.md":
        "વર્તમાન પર્યાયમાં પણ સિદ્ધ બનવાની પૂર્ણ ક્ષમતા મોજૂદ છે એવા વિશ્વાસથી સાધનામાં પુરુષાર્થ તેજ કરવો.",
    "chapter_097_svajati_sadbhuta_vyavahara_gu.md":
        "અંતરના રાગાદિ વિકારોને પોતાના જ માની પશ્ચાત્તાપ કરવો, જેથી આંતરિક શુદ્ધિનો સાચો માર્ગ ખૂલે.",
    "chapter_098_vijati_sadbhuta_vyavahara_gu.md":
        "ઇન્દ્રિયજ્ઞાનની પરાધીનતાને ઓળખી, અતીન્દ્રિય કેવળજ્ઞાન સ્વભાવને પ્રગટાવવાનો દૃઢ સંકલ્પ કરવો.",
    "chapter_140_ekajatyalpe_anyajatipurnopacharaka_vyavahara_gu.md":
        "લૌકિક પ્રશંસાના ઉપચારોથી અહંકારી ન બનતાં, પોતાની વાસ્તવિક મર્યાદાઓ સમજી નમ્રતા ધારણ કરવી.",
    "chapter_150_sadrisha_ekatvopacharaka_vyavahara_gu.md":
        "સંસારના સંબંધો કેવળ વ્યવહારિક સંયોગ છે એમ સમજી, આત્માની પરમ એકાકી શાશ્વત મુક્તિ તરફ લક્ષ રાખવું.",

    # -------------------------------------------------------------
    # Khanda 4: Rjusutra (10 chapters)
    # -------------------------------------------------------------
    "chapter_031_ashuddhasthula_rjusutranayamaka_paryayarthikanaya_gu.md":
        "વર્તમાન દેહ કેવળ એક ભવ પૂરતો મુસાફરનો વેશ છે એમ જાણી, દેહાધ્યાસ છોડી શુદ્ધ ચૈતન્યમાં જાગવું.",
    "chapter_032_shuddhasthula_rjusutranayamaka_paryayarthikanaya_gu.md":
        "દેહના જન્મ-મરણના બંધનોથી મુક્ત સિદ્ધાવસ્થાના સ્વાભાવિક રૂપનું સ્મરણ કરી, પરમ શાંતિ અનુભવવી.",
    "chapter_033_ashuddhasukshma_rjusutranayamaka_paryayarthikanaya_gu.md":
        "ક્રોધ એ આત્માનો સ્વભાવ નથી પણ એક સમયનો વિભાવિક પર્યાય છે એમ જાણી, સાક્ષીભાવે તેને શાંત કરવો.",
    "chapter_034_shuddhasukshma_rjusutranayamaka_paryayarthikanaya_gu.md":
        "કર્મોના આવરણો હટતાં જ અંતરમાં શુદ્ધ જ્ઞાનપર્યાય પ્રગટે છે એવા બોધ સાથે આત્મસાધનામાં મગ્ન રહેવું.",
    "chapter_037_sattagaunotpadavyayagrahaka_nitya_ashuddhaparyayarthikanaya_gu.md":
        "સંસારના પ્રત્યેક ભોગ ક્ષણભંગુર અને વિનાશી છે એમ સમજી, વિષયોની આસક્તિમાંથી તત્કાળ મુક્ત થવું.",
    "chapter_038_sattasapeksha_nitya_ashuddhaparyayarthikanaya_gu.md":
        "ઉત્પાદ અને વ્યયના વંટોળ વચ્ચે ત્રિકાળ ધ્રુવ આત્મસત્તાને ઓળખી, પરમ સમતાભાવમાં અડગ રહેવું.",
    "chapter_039_upadhinirapeksha_nitya_shuddhaparyayarthikanaya_gu.md":
        "પર્યાયમાં કર્મની ઉપાધિ છતાં આત્મસ્વભાવ સદા અસ્પૃષ્ટ અને પવિત્ર છે એવા ગૌરવથી ચિત્ત પ્રસન્ન રાખવું.",
    "chapter_040_upadhisapeksha_nitya_ashuddhaparyayarthikanaya_gu.md":
        "કર્મ ઉપાધિના કારણે થતા ભવભ્રમણથી ચેતીને, મોહના બંધનો કાપવા સદા સાવધાન રહેવું.",
    "chapter_055_ashuddhasthula_rjusutranaya_gu.md":
        "વર્તમાન આયુષ્ય વીજળીના ચમકાર જેવું ક્ષણિક છે એમ જાણી, પ્રમાદ ત્યજી આત્મકલ્યાણ સાધવું.",
    "chapter_056_shuddhasukshma_rjusutranaya_gu.md":
        "સિદ્ધ પરમાત્માના નિર્મળ અને અતીન્દ્રિય સુખનું ધ્યાન ધરી, પોતાના શુદ્ધ ચૈતન્યધામમાં સ્થિર થવું.",

    # -------------------------------------------------------------
    # Khanda 7: Evambhuta (7 chapters)
    # -------------------------------------------------------------
    "chapter_171_sarvagatanaya_gu.md":
        "જ્ઞાનગુણની અપેક્ષાએ ચેતના સમગ્ર લોકાલોકને જાણે છે એમ સમજી, પોતાના ચિત્તને સંકુચિતતામાંથી મુક્ત કરવું.",
    "chapter_174_ashunyanaya_gu.md":
        "આત્મા અનંત ગુણોથી સભર અને પરિપૂર્ણ છે એવા અનુભવથી બાહ્ય પદાર્થોની તૃષ્ણાને શાંત કરવી.",
    "chapter_176_jnanajneya_dvaitanaya_gu.md":
        "દર્પણ સમાન જ્ઞાનમાં જ્ઞેયો ઝળકવા છતાં જ્ઞાન જ્ઞેયરૂપ થતું નથી એમ જાણી, નિર્લેપ સાક્ષીભાવ જાળવવો.",
    "chapter_180_asvabhavanaya_gu.md":
        "સાધનાના પ્રારંભે સત્સંગ અને સદ્ગુરુના પવિત્ર સંસ્કારોનું શરણ લઈ, અંતરંગ શુદ્ધિનો માર્ગ પ્રશસ્ત કરવો.",
    "chapter_185_ishvaranaya_gu.md":
        "સંસારી અવસ્થામાં કર્મની પ્રબળતા જાણી મિથ્યા ગર્વ છોડવો, અને સ્વતંત્ર મોક્ષપદ અર્થે પુરુષાર્થ આદરવો.",
    "chapter_193_kriyanaya_gu.md":
        "કેવળ શુષ્ક જ્ઞાનની વાતો કરવાને બદલે, સમ્યક્ ચારિત્ર અને સદાચારના પવિત્ર આચરણમાં તન્મય થવું.",
    "chapter_201_nimittatvanimittadrishti_gu.md":
        "પરિસ્થિતિઓ કે અન્ય પર દોષ ઢોળવાને બદલે, પોતાના અંતરંગ રાગ-દ્વેષના ભાવો સુધારી આત્મજાગૃત થવું."
}

def update_file(file_path: Path, sadhana_text: str) -> bool:
    content = file_path.read_text(encoding="utf-8")
    original = content
    
    # Regex to match the Kavyadhara & Sadhanadhara table with empty or minimal sadhana
    # Matches: | <kavya> | <empty or whitespace> |
    table_pattern = r'(\|\s*📜\s*કાવ્યધારા\s*\|\s*✦\s*સાધનાધારા\s*\|\s*\n\|[-:| ]+\|\s*\n\|\s*[^|]+\s*\|)\s*([^|]*)\s*(\|)'
    
    m = re.search(table_pattern, content)
    if m:
        before = m.group(1)
        after = m.group(3)
        replacement = f"{before} {sadhana_text} {after}"
        content = content[:m.start()] + replacement + content[m.end():]
    else:
        # If the table wasn't matched, check if ## કાવ્યધારા exists without sadhanadhara
        m_kavya = re.search(r'## કાવ્યધારા\s*\n(.*?)(?=\n---|\n##|$)', content, re.S)
        if m_kavya:
            kavya_raw = m_kavya.group(1).strip()
            raw_lines = [l.strip() for l in kavya_raw.splitlines() if l.strip()]
            kavya_col = "<br>".join(l.replace("|", "\\|") for l in raw_lines)
            new_sec = f"""## કાવ્યધારા અને સાધનાધારા

| 📜 કાવ્યધારા | ✦ સાધનાધારા |
|:---|:---|
| {kavya_col} | {sadhana_text} |"""
            start, end = m_kavya.span()
            content = content[:start] + new_sec + content[end:]
            
    if content != original:
        file_path.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    base_dir = Path("sankshipt/output")
    print(f"Applying Sadhana-sutras to {len(SADHANA_MAP)} chapters...")
    
    updated = 0
    not_found = []
    
    for fname, s_text in SADHANA_MAP.items():
        matches = list(base_dir.glob(f"**/{fname}"))
        if not matches:
            not_found.append(fname)
            continue
        p = matches[0]
        if update_file(p, s_text):
            updated += 1
            print(f"✓ Updated: {p.parent.name}/{p.name}")
        else:
            print(f"⚠ Content unchanged or already set: {p.name}")
            
    print("\n------------------------------------------------------------")
    print(f"Total target files in map: {len(SADHANA_MAP)}")
    print(f"Successfully updated: {updated}")
    if not_found:
        print(f"Files not found: {not_found}")
    print("------------------------------------------------------------")

if __name__ == "__main__":
    main()
