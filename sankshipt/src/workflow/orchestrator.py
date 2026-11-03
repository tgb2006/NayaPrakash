"""Workflow Orchestrator for Sankshipt 2-Page A5 Edition."""

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

    def get_prompt_for_chapter(self, naya_id: int) -> str:
        naya = self.loader.get_naya_by_id(naya_id)
        if not naya:
            raise ValueError(f"નય આઈડી {naya_id} કેટેલોગમાં મળ્યો નથી.")

        khanda = self.loader.get_khanda_by_id(naya.khanda_id)
        if not khanda:
            raise ValueError(f"ખંડ આઈડી {naya.khanda_id} મળ્યો નથી.")

        writer_prompt_path = self.prompts_dir / "chapter_writer_prompt.md"
        base_instructions = writer_prompt_path.read_text(encoding="utf-8") if writer_prompt_path.exists() else ""

        used_examples_context = self.registry.get_used_themes_context(max_recent=30)
        reference_context = self.retriever.format_reference_context_for_prompt(
            naya.id, naya.name_hindi, naya.khanda_id
        )

        prompt = f"""
{base_instructions}

======================================================================
આ સંક્ષિપ્ત ૨-પેજ અધ્યાય માટે વિશિષ્ટ વિગતો (SPECIFIC ASSIGNMENT):
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
નવલિકા પુનરાવર્તન નિવારણ (NOVELLA DEDUPLICATION GUARD):
નીચે પૂર્વે પ્રયુક્ત નવલિકાઓના શીર્ષક અને વિષય આપેલા છે.
આ તમામથી સર્વથા ભિન્ન, નવી અને મૌલિક ૧ નવલિકા જમણા પાના માટે લખવાની છે:
{used_examples_context}
----------------------------------------------------------------------

----------------------------------------------------------------------
સંદર્ભ ગ્રંથાલયમાંથી શાસ્ત્રીય સામગ્રી (SCRIPTURAL EXCERPTS):
{reference_context}
----------------------------------------------------------------------

----------------------------------------------------------------------
અનિવાર્ય લે-આઉટ નિર્દેશ (STRICT 2-PAGE SPREAD FORMAT):
- પ્રથમ પૃષ્ઠ (ડાબું પાનું - PAGE 1: સંપૂર્ણ નય વિવેચન & કાવ્યાત્મક બોધસૂત્ર):
  1. # {naya.id:03d}. {naya.name_hindi}
  2. ## નય વિવેચન (આબાલગોપાલ સુબોધ શૈલી, સુંદર વિભાજન પૂર્વક રોચક સમજૂતી, અતિ-સરળ ઉદાહરણો: ~૨૪૦-૨૭૦ શબ્દો)
  3. ## કાવ્યાત્મક બોધસૂત્ર (નયનું સ્વરૂપ અને સાધના સંકેત બંને વણી લેતી કેવળ ૨ પંક્તિનો ગેય દોહરો: ~૨૦-૨૫ શબ્દો)
  (ડાબા પાનાનું કુલ લખાણ: ૨૬૦ થી ૩૦૦ શબ્દો)

- દ્વિતીય પૃષ્ઠ (જમણું પાનું - PAGE 2: પ્રસંગ & વિવેક-દર્શન):
  1. ## પ્રસંગ: [કથાનું વિશિષ્ટ આધ્યાત્મિક શીર્ષક] (૫૦% થી ૬૦% ભાગ: ~૧૫૦-૧૮૦ શબ્દો)
     - ### પિપાસા (મૂંઝવણ, અટકળો, વલયો અને પ્રશ્નાર્થ "આમાંથી શું રસ્તો?": ~૭૫-૯૦ શબ્દો)
     - ### પાન (નય-દ્રષ્ટિથી સમાધાન, માર્ગ, મંઝિલ અને ભીતરનો અપૂર્વ વિશ્રામ: ~૭૫-૯૦ શબ્દો)
  2. ## વિવેક-દર્શન: એકાંત અને અનેકાંત (૪૦% ભાગ: ~૧૧૦-૧૩૦ શબ્દો)
     - ### એકાંત દર્શન (જો આ નય જીદ/કદાગ્રહ/જડ બને તો કેવું નુકસાન/સંકુચિતતા: ~૫૫-૬૫ શબ્દો)
     - ### અનેકાંત દર્શન (જો આ નય યાત્રા/સમન્વય/મંઝિલગામી બને તો કેવું સૌંદર્ય: ~૫૫-૬૫ શબ્દો)
  (જમણા પાનાનું કુલ લખાણ: ૨૬૦ થી ૩૧૦ શબ્દો)

- સમગ્ર પ્રકરણ કુલ શબ્દ મર્યાદા: ૫૩૦ થી ૬૨૦ શબ્દો (A5 સાઇઝના ૨ પાનામાં સચોટ સમાવેશ).
----------------------------------------------------------------------

કૃપા કરીને આ સંક્ષિપ્ત ૨-પેજ અધ્યાય સંપૂર્ણપણે શુદ્ધ સાહિત્યિક ગુજરાતી ભાષામાં લખો.
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

----------------------------------------------------------------------
શ્વેતામ્બર પરંપરાના સર્વોચ્ચ આધારભૂત સંદર્ભો (SHVETAMBARA CANONICAL AUTHORITIES):
આ ખંડ પરિચયમાં શ્વેતામ્બર પરંપરાના સિદ્ધાંતો અંતિમ અને સર્વોચ્ચ ગણીને ચાલવાનું છે.
મુખ્ય આધાર ગ્રંથો:
૧. દ્રવ્યગુણપર્યાયનો રાસ (મહોપાધ્યાય યશોવિજયજી / અભયશેખરસૂરિજી)
૨. સપ્તભંગી નયપ્રદીપ
૩. નય રહસ્ય (મહોપાધ્યાય યશોવિજયજી)
૪. નયોપદેશ
(આલાપપદ્ધતિ, નયચક્ર વગેરે પૂરક સહાય માટે જ વાપરવા)

સંદર્ભ ગ્રંથાલયમાંથી પ્રામાણિક અવતરણો:
{ref_text}
----------------------------------------------------------------------

અનિવાર્ય માળખું (૪-PAGE A5 KHANDA INTRO BLUEPRINT - 'આર' પ્રાસ શ્રેણી):
૧. શીર્ષક અને આગમિક મંગલાચરણ (મૂળ સૂત્ર, વર્ગીકરણ, મુખ્ય આધાર ગ્રંથો)
૨. ## ૧. આગમ-આધાર (~૨૦૦-૨૪૦ શબ્દો)
૩. ## ૨. તત્વ-વિસ્તાર (~૨૦૦-૨૪૦ શબ્દો)
૪. ## ૩. શાખા-પ્રસાર (~૨૫૦-૩૦૦ શબ્દો - સમગ્ર ખંડના નયોનો સુગ્રથિત નકશો)
૫. ## ૪. વિવેક-વિચાર (~૧૫૦-૧૮૦ શબ્દો - નયાભાસ વિવેક)
૬. ## ૫. સાધના-સાક્ષાત્કાર (~૧૦૦-૧૨૦ શબ્દો)
૭. ## ૬. સૂત્ર-સાર (~૨૦-૩૦ શબ્દો - ૨ પંક્તિનો ગેય દોહરો)

કુલ શબ્દ મર્યાદા: ૯૦૦ થી ૧૧૫૦ શબ્દો (A5 સાઇઝના ૪ પાના). બિનજરૂરી લંબાણ વગર ગંભીર અને પ્રામાણિક શૈલીમાં લખવું.
"""
        return prompt.strip()

    def process_and_register_chapter(self, file_path: Path, naya_id: int) -> Dict[str, Any]:
        if not file_path.exists():
            return {"success": False, "error": f"ફાઇલ મળી નથી: {file_path}"}

        naya = self.loader.get_naya_by_id(naya_id)
        if not naya:
            return {"success": False, "error": f"નય {naya_id} મળ્યો નથી"}

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
                "error": "સમીક્ષામાં ભૂલો જણાઈ છે."
            }

        # Extract novella and register as example
        novella_item = self.validator.extract_novella(content)
        registered_count = 0
        if novella_item:
            self.registry.add_examples_for_chapter(
                chapter_id=naya_id,
                naya_name=naya.name_hindi,
                examples=[{
                    "title": novella_item["title"],
                    "theme": f"નય {naya_id} નવલિકા",
                    "summary": novella_item["summary"],
                    "keywords": [w for w in novella_item["title"].split() if len(w) > 3]
                }]
            )
            registered_count = 1

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
            "extracted_examples_count": registered_count,
            "word_count": val_report.total_words
        }
