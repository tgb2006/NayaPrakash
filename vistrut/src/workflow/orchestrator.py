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
આ અધ્યાય માટે વિશિષ્ટ વિગતો (SPECIFIC ASSIGNMENT FOR THIS CHAPTER):
======================================================================
- **નય ક્રમાંક (ID)**: {naya.id}
- **નયનું નામ**: {naya.name_hindi}
- **સંસ્કૃત/પ્રાકૃત નામ**: {naya.name_sanskrit}
- **ખંડ**: {khanda.name_hindi} (ખંડ {khanda.id})
- **મૂળ નય**: {khanda.root_naya} ({khanda.sanskrit_name})
- **મુખ્ય શ્રેણી**: {naya.category} ({khanda.primary_division})
- **ત્રિવિધ વિભાગ**: {naya.aspect} ({khanda.tri_aspect})
- **મૂળ આગમ સૂત્ર**: `{khanda.core_sutra}`
- **પ્રાથમિક વ્યાખ્યા/લક્ષણ**: {naya.definition_brief}

----------------------------------------------------------------------
પુનરાવર્તન નિવારણ (EXAMPLES DEDUPLICATION GUARD):
નીચે પૂર્વે પ્રયુક્ત ઉદાહરણોના શીર્ષક અને વિષય આપેલા છે.
આ તમામથી સર્વથા ભિન્ન, નવા અને મૌલિક ૩ ઉદાહરણો લખવાના છે:
{used_examples_context}
----------------------------------------------------------------------

----------------------------------------------------------------------
સંદર્ભ ગ્રંથાલયમાંથી શાસ્ત્રીય સામગ્રી (SCRIPTURAL EXCERPTS):
{reference_context}
----------------------------------------------------------------------

----------------------------------------------------------------------
વિશેષ અનિવાર્ય નિર્દેશ (STRICT CITATION RULES):
- અધ્યાયના કોઈપણ ભાગમાં સ્રોત પુસ્તકનું નામ, પીડીએફ ફાઇલનું નામ (જેમ કે 1_2_3_4_5_merged.pdf) અથવા પૃષ્ઠ સંખ્યાનો ઉલ્લેખ ક્યારેય ન કરવો.
- સેક્શન ૧ માં કેવળ 'મૂળ લક્ષણ' લખવું. 'આગમિક આધાર ગ્રંથ' જેવી કોઈ પંક્તિ ન હોવી જોઈએ.
- આ ગ્રંથ એક સ્વતંત્ર, મૌલિક અને પ્રામાણિક ગુજરાતી મહાગ્રંથ તરીકે શોભવો જોઈએ.
----------------------------------------------------------------------

કૃપા કરીને ૧૦ બિંદુઓના સચોટ શીર્ષકો સાથે સંપૂર્ણ વિગતવાર અધ્યાય શુદ્ધ સાહિત્યિક ગુજરાતી ભાષામાં લખો (આશરે ૨૫૦૦ થી ૩૫૦૦ શબ્દો), જેમાં ઉપર્યુક્ત શાસ્ત્રીય ભાવો અને સૂત્રોનો પ્રામાણિક સમન્વય અવશ્ય હોય.
"""
        return prompt.strip()

    def get_prompt_for_khanda_intro(self, khanda_id: int) -> str:
        khanda = self.loader.get_khanda_by_id(khanda_id)
        if not khanda:
            raise ValueError(f"ખંડ આઈડી {khanda_id} મળ્યો નથી.")

        intro_prompt_path = self.prompts_dir / "khanda_intro_prompt.md"
        base_instructions = intro_prompt_path.read_text(encoding="utf-8") if intro_prompt_path.exists() else ""

        nayas = self.loader.get_nayas_by_khanda(khanda_id)
        nayas_summary = "\n".join([f"- {n.id}. {n.name_hindi}: {n.definition_brief}" for n in nayas[:15]])

        ref_snippets = self.retriever.search([khanda.root_naya, khanda.sanskrit_name], max_snippets=4)
        ref_text = "\n\n".join([f"**{s['book']}**:\n> \"...{s['snippet']}...\"" for s in ref_snippets])

        prompt = f"""
{base_instructions}

======================================================================
આ ખંડ માટે વિગતો (KHANDA SPECIFICATION):
======================================================================
- **ખંડ ક્રમાંક**: {khanda.id}
- **ખંડનું નામ**: {khanda.name_hindi}
- **મૂળ નય**: {khanda.root_naya} ({khanda.sanskrit_name})
- **મુખ્ય શ્રેણી**: {khanda.primary_division}
- **ત્રિવિધ વિભાગ**: {khanda.tri_aspect}
- **આગમ સૂત્ર**: `{khanda.core_sutra}`
- **આગમિક લક્ષણ**: {khanda.agamic_definition}
- **દાર્શનિક સાર**: {khanda.philosophical_essence}
- **અધ્યાય સંખ્યા**: {khanda.chapters_count} (નય ક્રમાંક {khanda.range[0]} થી {khanda.range[1]})

આ ખંડ અંતર્ગત આવતા કેટલાક પ્રમુખ નય:
{nayas_summary}
...અને અન્ય.

----------------------------------------------------------------------
સંદર્ભ ગ્રંથાલયમાંથી આ મૂળ નયના પ્રામાણિક સંદર્ભો (SCRIPTURAL EXCERPTS):
{ref_text}
----------------------------------------------------------------------

કૃપા કરીને આ ખંડ માટે આશરે ૧૦૦૦ થી ૧૫૦૦ શબ્દોનો અત્યંત ગંભીર, પ્રામાણિક અને માર્ગદર્શક પરિચયાત્મક આલેખ સંપૂર્ણપણે શુદ્ધ સાહિત્યિક ગુજરાતી ભાષામાં લખો, જેમાં આ સંદર્ભ ગ્રંથોના સિદ્ધાંતોનો યથોચિત સમાવેશ હોય.
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
