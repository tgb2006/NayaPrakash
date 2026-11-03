"""Workflow Orchestrator coordinating drafting prompts, validation, registry, and compilation."""

from pathlib import Path
from typing import Dict, Any, Optional, List
from src.core.catalog_loader import CatalogLoader
from src.core.registry_manager import RegistryManager
from src.core.validator import ChapterValidator
from src.core.reference_retriever import ReferenceRetriever
from src.workflow.compiler import BookCompiler

class WorkflowOrchestrator:
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path(__file__).resolve().parent.parent.parent
        self.loader = CatalogLoader(self.base_dir)
        self.registry = RegistryManager(self.base_dir)
        self.validator = ChapterValidator()
        self.compiler = BookCompiler(self.base_dir)
        self.retriever = ReferenceRetriever(self.base_dir / "references")
        self.prompts_dir = self.base_dir / "prompts"
        self.sections_prompts_dir = self.prompts_dir / "sections"

    SECTION_FILES = {
        1: "01_naya.md",
        2: "02_samanya_arth.md",
        3: "03_tarkik_vivechan.md",
        4: "04_udaharan.md",
        5: "05_vyavaharik_samaj.md",
        6: "06_darshanik_samaj.md",
        7: "07_saiddhantik_samaj.md",
        8: "08_sadhanakiya_samaj.md",
        9: "09_deep_dive.md",
        10: "10_manzilgami_valan.md",
    }

    SECTION_TITLES = {
        1: ("નય", "नय"),
        2: ("સામાન્ય અર્થ અને શબ્દાર્થ", "सामान्य अर्थ एवं शब्दार्थ"),
        3: ("તાર્કિક વિવેચન", "तार्किक विवेचन"),
        4: ("ઉદાહરણ", "उदाहरण"),
        5: ("વ્યવહારિક સમજ", "व्यवहारिक समझ"),
        6: ("દાર્શનિક સમજ", "दार्शनिक समझ"),
        7: ("સૈદ્ધાંતિક સમજ", "सैद्धांतिक समझ"),
        8: ("સાધનાકીય સમજ", "साधनाकीय समझ"),
        9: ("ડીપ ડાઈવ", "डीप डाइव"),
        10: ("મંઝિલગામી વલણ", "मंजिलगामी रुख"),
    }

    def get_prompt_for_section(self, naya_id: int, section_num: int, previous_context: str = "", lang: str = "gu") -> str:
        """Generate a focused prompt for a specific section with required context and guidelines."""
        if section_num not in self.SECTION_FILES:
            raise ValueError(f"અમાન્ય સેક્શન નંબર: {section_num} (૧ થી ૧૦ હોવો જોઈએ)")

        naya = self.loader.get_naya_by_id(naya_id)
        if not naya:
            raise ValueError(f"નય આઈડી {naya_id} કેટેલોગમાં મળ્યો નથી.")

        khanda = self.loader.get_khanda_by_id(naya.khanda_id)
        if not khanda:
            raise ValueError(f"ખંડ આઈડી {naya.khanda_id} મળ્યો નથી.")

        section_file = self.sections_prompts_dir / self.SECTION_FILES[section_num]
        base_instructions = section_file.read_text(encoding="utf-8") if section_file.exists() else ""

        target_lang = "ગુજરાતી (સાહિત્યિક અને કુદરતી પ્રવાહી શૈલી)" if lang == "gu" else "हिन्दी (प्रौढ़ एवं शास्त्रीय शैली)"
        title_gu, title_hi = self.SECTION_TITLES[section_num]
        target_heading = f"## {title_gu}" if lang == "gu" else f"## {title_hi}"

        context_blocks = []
        if previous_context:
            context_blocks.append(f"""
----------------------------------------------------------------------
પૂર્વવર્તી સેક્શન્સનો સાર અને સાતત્ય (PREVIOUS CONTEXT FOR CONTINUITY):
{previous_context}
----------------------------------------------------------------------""")

        if section_num == 4:
            used_examples_context = self.registry.get_used_themes_context(max_recent=30)
            context_blocks.append(f"""
----------------------------------------------------------------------
પુનરાવર્તન નિવારણ (EXAMPLES DEDUPLICATION GUARD):
નીચે પૂર્વે વપરાયેલા ઉદાહરણોની સૂચિ છે. આ તમામથી તદ્દન અલગ, મૌલિક ૩ ઉદાહરણો લખવાના છે:
{used_examples_context}
----------------------------------------------------------------------""")

        if section_num in [2, 3, 6, 7]:
            reference_context = self.retriever.format_reference_context_for_prompt(
                naya.id, naya.name_hindi, naya.khanda_id
            )
            context_blocks.append(f"""
----------------------------------------------------------------------
સંદર્ભ ગ્રંથાલયમાંથી શાસ્ત્રીય સામગ્રી (SCRIPTURAL EXCERPTS):
{reference_context}
----------------------------------------------------------------------""")

        extra_context = "\n".join(context_blocks)

        prompt = f"""
{base_instructions}

======================================================================
આ સેક્શન માટે વિશિષ્ટ વિગતો (ASSIGNMENT FOR SECTION {section_num}):
======================================================================
- **લક્ષ્ય ભાષા**: {target_lang}
- **સેક્શન હેડિંગ**: `{target_heading}` (કોઈ નંબર કે ક્રમાંક વગર)
- **નય ક્રમાંક**: {naya.id}
- **નયનું નામ**: {naya.name_hindi} / {naya.name_sanskrit}
- **ખંડ**: {khanda.name_hindi} (ખંડ {khanda.id})
- **મૂળ નય**: {khanda.root_naya} ({khanda.sanskrit_name})
- **મુખ્ય શ્રેણી**: {naya.category} ({khanda.primary_division})
- **ત્રિવિધ વિભાગ**: {naya.aspect} ({khanda.tri_aspect})
- **પ્રાથમિક વ્યાખ્યા/લક્ષણ**: {naya.definition_brief}
{extra_context}

કૃપા કરીને આ સેક્શનનું સંપૂર્ણ લખાણ ઉપર્યુક્ત માર્ગદર્શિકા મુજબ જ લખો.
"""
        return prompt.strip()

    def assemble_chapter(self, naya_id: int, sections: Dict[int, str], lang: str = "gu") -> str:
        """Assemble all 10 individual sections into a unified chapter markdown text."""
        naya = self.loader.get_naya_by_id(naya_id)
        if not naya:
            raise ValueError(f"નય {naya_id} મળ્યો નથી")

        title_prefix = f"# અધ્યાય {naya.id:03d}: {naya.name_hindi}" if lang == "gu" else f"# अध्याय {naya.id:03d}: {naya.name_hindi}"
        
        parts = [title_prefix]
        for sec_num in range(1, 11):
            sec_content = sections.get(sec_num, "").strip()
            if not sec_content:
                title_gu, title_hi = self.SECTION_TITLES[sec_num]
                title = title_gu if lang == "gu" else title_hi
                sec_content = f"## {title}\n\n[વિષયવસ્તુ અપ્રાપ્ય]"
            parts.append(sec_content)

        return "\n\n---\n\n".join(parts) + "\n"

    def get_prompt_for_chapter(self, naya_id: int) -> str:
        naya = self.loader.get_naya_by_id(naya_id)
        if not naya:
            raise ValueError(f"नय आईडी {naya_id} कैटलॉग में नहीं मिली।")

        khanda = self.loader.get_khanda_by_id(naya.khanda_id)
        if not khanda:
            raise ValueError(f"खंड आईडी {naya.khanda_id} नहीं मिली।")

        writer_prompt_path = self.prompts_dir / "chapter_writer_prompt.md"
        base_instructions = writer_prompt_path.read_text(encoding="utf-8") if writer_prompt_path.exists() else ""

        used_examples_context = self.registry.get_used_themes_context(max_recent=30)
        reference_context = self.retriever.format_reference_context_for_prompt(
            naya.id, naya.name_hindi, naya.khanda_id
        )

        prompt = f"""
{base_instructions}

======================================================================
इस अध्याय के लिए विशिष्ट विवरण (SPECIFIC ASSIGNMENT FOR THIS CHAPTER):
======================================================================
- **नय क्रमांक (ID)**: {naya.id}
- **नय का नाम (Hindi)**: {naya.name_hindi}
- **संस्कृत नाम**: {naya.name_sanskrit}
- **खंड**: {khanda.name_hindi} (खंड {khanda.id})
- **मूल नय**: {khanda.root_naya} ({khanda.sanskrit_name})
- **मुख्य श्रेणी**: {naya.category} ({khanda.primary_division})
- **त्रिविध विभाग**: {naya.aspect} ({khanda.tri_aspect})
- **मूल आगम सूत्र**: `{khanda.core_sutra}`
- **प्राथमिक परिभाषा**: {naya.definition_brief}

----------------------------------------------------------------------
पुनरावृत्ति निवारण (EXAMPLES DEDUPLICATION GUARD):
नीचे पूर्व अध्यायों में प्रयुक्त कुछ उदाहरणों के शीर्षक व विषय दिए गए हैं।
आपको इन सभी से पूर्णतः भिन्न, नए और मौलिक 3 उदाहरण लिखने हैं:
{used_examples_context}
----------------------------------------------------------------------

----------------------------------------------------------------------
संदर्भ ग्रंथालय से उद्धृत शास्त्रीय सामग्री (SCRIPTURAL EXCERPTS):
{reference_context}
----------------------------------------------------------------------

----------------------------------------------------------------------
विशेष अनिवार्य निर्देश (STRICT CITATION RULES):
- अध्याय के किसी भी भाग में स्रोत पुस्तक का नाम, पीडीएफ फाइल का नाम (जैसे 1_2_3_4_5_merged.pdf) अथवा पृष्ठ संख्या का उल्लेख कदापि नहीं करना है।
- सेक्शन 1 में केवल 'मूल लक्षण' लिखना है। 'आगमिक आधार ग्रंथ' जैसी कोई पंक्ति नहीं होनी चाहिए।
- यह ग्रंथ एक स्वतंत्र, मौलिक व प्रामाणिक महाग्रंथ के रूप में प्रस्तुत होगा।
----------------------------------------------------------------------

कृपया 10 बिंदुओं के सटीक शीर्षकों के साथ पूरा विस्तृत अध्याय लिखें (न्यूनतम 1800-2200 शब्द), जिसमें उपर्युक्त शास्त्रीय भावों और सूत्रों का प्रामाणिक समन्वय अवश्य हो।
"""
        return prompt.strip()

    def get_prompt_for_khanda_intro(self, khanda_id: int) -> str:
        khanda = self.loader.get_khanda_by_id(khanda_id)
        if not khanda:
            raise ValueError(f"खंड आईडी {khanda_id} नहीं मिली।")

        intro_prompt_path = self.prompts_dir / "khanda_intro_prompt.md"
        base_instructions = intro_prompt_path.read_text(encoding="utf-8") if intro_prompt_path.exists() else ""

        nayas = self.loader.get_nayas_by_khanda(khanda_id)
        nayas_summary = "\n".join([f"- {n.id}. {n.name_hindi}: {n.definition_brief}" for n in nayas[:15]])

        ref_snippets = self.retriever.search([khanda.root_naya, khanda.sanskrit_name], max_snippets=4)
        ref_text = "\n\n".join([f"**{s['book']}**:\n> \"...{s['snippet']}...\"" for s in ref_snippets])

        prompt = f"""
{base_instructions}

======================================================================
इस खंड के लिए विवरण (KHANDA SPECIFICATION):
======================================================================
- **खंड क्रमांक**: {khanda.id}
- **खंड का नाम**: {khanda.name_hindi}
- **मूल नय**: {khanda.root_naya} ({khanda.sanskrit_name})
- **मुख्य श्रेणी**: {khanda.primary_division}
- **त्रिविध विभाग**: {khanda.tri_aspect}
- **आगम सूत्र**: `{khanda.core_sutra}`
- **आगमिक लक्षण**: {khanda.agamic_definition}
- **दार्शनिक सार**: {khanda.philosophical_essence}
- **अध्याय संख्या**: {khanda.chapters_count} (नय क्रमांक {khanda.range[0]} से {khanda.range[1]})

इस खंड के अंतर्गत आने वाले कुछ प्रमुख नय:
{nayas_summary}
...और अन्य।

----------------------------------------------------------------------
संदर्भ ग्रंथालय से इस मूल नय के प्रामाणिक संदर्भ (SCRIPTURAL EXCERPTS):
{ref_text}
----------------------------------------------------------------------

कृपया इस खंड के लिए लगभग 1000-1500 शब्दों का अत्यंत गंभीर, प्रामाणिक व मार्गदर्शक परिचयात्मक आलेख लिखें, जिसमें इन संदर्भ ग्रंथों के सिद्धांतों का यथोचित समावेश हो।
"""
        return prompt.strip()

    def process_and_register_chapter(self, file_path: Path, naya_id: int) -> Dict[str, Any]:
        if not file_path.exists():
            return {"success": False, "error": f"फ़ाइल नहीं मिली: {file_path}"}

        naya = self.loader.get_naya_by_id(naya_id)
        if not naya:
            return {"success": False, "error": f"नय {naya_id} नहीं मिला"}

        content = file_path.read_text(encoding="utf-8")
        val_report = self.validator.validate_content(content)

        if not val_report.is_valid:
            self.registry.update_chapter_status(
                chapter_id=naya_id,
                status="drafted_with_errors",
                file_path=str(file_path),
                word_count=val_report.total_words,
                is_valid=False
            )
            return {
                "success": False,
                "validation_report": val_report.model_dump(),
                "error": "समीक्षा में त्रुटियाँ पाई गईं।"
            }

        # Extract examples and register
        raw_examples = self.validator.extract_examples(content)
        parsed_examples = []
        for i, ex in enumerate(raw_examples, 1):
            parsed_examples.append({
                "title": ex.get("title", f"उदाहरण {i}"),
                "theme": f"नय {naya_id} दृष्टांत {i}",
                "summary": ex.get("summary", ""),
                "keywords": [w for w in ex.get("title", "").split() if len(w) > 3]
            })

        self.registry.add_examples_for_chapter(
            chapter_id=naya_id,
            naya_name=naya.name_hindi,
            examples=parsed_examples
        )

        self.registry.update_chapter_status(
            chapter_id=naya_id,
            status="completed",
            file_path=str(file_path),
            word_count=val_report.total_words,
            is_valid=True
        )

        # Trigger TOC regeneration
        self.compiler.generate_toc()

        return {
            "success": True,
            "validation_report": val_report.model_dump(),
            "extracted_examples_count": len(parsed_examples),
            "word_count": val_report.total_words
        }
