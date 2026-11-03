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

कृपया 10 बिंदुओं के सटीक शीर्षकों के साथ पूरा विस्तृत अध्याय लिखें (न्यूनतम 1800-2200 शब्द), जिसमें उपर्युक्त संदर्भ ग्रंथों और सूत्रों का प्रामाणिक समन्वय अवश्य हो।
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
