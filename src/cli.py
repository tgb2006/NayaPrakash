"""Command Line Interface for Naya Prakash Book Writing Workflow."""

import sys
import argparse
from pathlib import Path

from src.core.catalog_loader import CatalogLoader
from src.core.registry_manager import RegistryManager
from src.core.validator import ChapterValidator
from src.core.reference_retriever import ReferenceRetriever
from src.workflow.compiler import BookCompiler
from src.workflow.orchestrator import WorkflowOrchestrator

def cmd_status(args):
    reg = RegistryManager()
    summary = reg.get_dashboard_summary()

    print("\n" + "=" * 65)
    print(" 📖  नय प्रकाश: 203 नय महाग्रंथ — प्रगति स्थिति (STATUS)")
    print("=" * 65)
    print(f"  • कुल नय (अध्याय):          {summary['total_nayas']}")
    print(f"  • पूर्ण अध्याय (Completed):   {summary['completed']}")
    print(f"  • शेष अध्याय (Pending):      {summary['pending']}")
    print(f"  • प्रगति प्रतिशत (Progress):   {summary['percent_completed']}%")
    print(f"  • पंजीकृत अद्वितीय उदाहरण:   {summary['total_unique_examples']} (लक्ष्य 609)")
    print("-" * 65)
    print(" 📚 खंड-वार प्रगति (Khanda Progress):")

    loader = CatalogLoader()
    khandas = loader.get_khandas()
    kp = summary.get("khanda_progress", {})

    for k in khandas:
        p = kp.get(str(k.id), {"total": k.chapters_count, "completed": 0})
        bar_len = 20
        comp = p.get("completed", 0)
        tot = p.get("total", k.chapters_count)
        filled = int((comp / tot) * bar_len) if tot > 0 else 0
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"  [{k.id}] {k.name_hindi:<26} [{bar}] {comp:2d}/{tot:2d}")

    print("=" * 65 + "\n")

def cmd_khandas(args):
    loader = CatalogLoader()
    khandas = loader.get_khandas()
    print("\n" + "=" * 75)
    print(" 🏛️  सप्त खंड एवं मूल नय रूपरेखा (7 KHANDAS BLUEPRINT)")
    print("=" * 75)
    for k in khandas:
        print(f"\n[खंड {k.id}] {k.name_hindi} ({k.sanskrit_name})")
        print(f"  • श्रेणी: {k.primary_division} | त्रि-विभाग: {k.tri_aspect}")
        print(f"  • अध्याय विस्तार: नय {k.range[0]} से {k.range[1]} (कुल {k.chapters_count} अध्याय)")
        print(f"  • मूल सूत्र: {k.core_sutra}")
        print(f"  • आगमिक लक्षण: {k.agamic_definition}")
    print("\n" + "=" * 75 + "\n")

def cmd_catalog(args):
    loader = CatalogLoader()
    khanda_id = getattr(args, "khanda", None)
    if khanda_id:
        nayas = loader.get_nayas_by_khanda(int(khanda_id))
        print(f"\n--- खंड {khanda_id} के अंतर्गत नय सूची (कुल {len(nayas)}) ---")
    else:
        nayas = loader.get_all_nayas()
        print(f"\n--- संपूर्ण 203 नय सूची ---")

    for n in nayas:
        print(f"[{n.id:03d}] {n.name_hindi:<36} | {n.category} ({n.aspect})")
        print(f"      लक्षण: {n.definition_brief}")
    print()

def cmd_prompt(args):
    orch = WorkflowOrchestrator()
    if args.khanda_intro:
        prompt = orch.get_prompt_for_khanda_intro(int(args.khanda_intro))
        print(prompt)
    elif args.id:
        prompt = orch.get_prompt_for_chapter(int(args.id))
        print(prompt)
    else:
        print("कृपया --id <नय_आईडी> अथवा --khanda-intro <खंड_आईडी> निर्दिष्ट करें।")

def cmd_validate(args):
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"त्रुटि: फ़ाइल नहीं मिली - {file_path}")
        return

    content = file_path.read_text(encoding="utf-8")
    validator = ChapterValidator()
    report = validator.validate_content(content)

    print("\n" + "=" * 60)
    print(f" 🔍  अध्याय समीक्षा रिपोर्ट: {file_path.name}")
    print("=" * 60)
    print(f"  • परिणाम (Verdict):    {'✅ उत्तीर्ण (PASS)' if report.is_valid else '❌ संशोधन अपेक्षित (REVISE)'}")
    print(f"  • कुल शब्द (Words):    {report.total_words}")
    print(f"  • अहिंसा व नैतिकता:   {'✅ शुद्ध (Compliant)' if report.ahimsa_passed else '❌ उल्लंघन पाया गया'}")

    print("\n 📊 अनुभाग शब्द-संख्या विश्लेषण:")
    for name, r in report.word_count_reports.items():
        status_sym = "✅" if r.passed else "❌"
        print(f"   {status_sym} {name}: {r.actual_words} शब्द ({r.expected_range})")

    if report.missing_sections:
        print("\n ⚠️ अनुपस्थित अनिवार्य अनुभाग:")
        for sec in report.missing_sections:
            print(f"   - {sec}")

    if report.errors:
        print("\n ❌ मुख्य त्रुटियाँ:")
        for err in report.errors:
            print(f"   - {err}")

    if report.warnings:
        print("\n ⚠️ चेतावनियाँ:")
        for w in report.warnings:
            print(f"   - {w}")

    print("=" * 60 + "\n")

def cmd_register(args):
    file_path = Path(args.file)
    naya_id = int(args.id)
    orch = WorkflowOrchestrator()
    result = orch.process_and_register_chapter(file_path, naya_id)

    if result.get("success"):
        print(f"\n✅ नय {naya_id} का अध्याय सफलतापूर्वक सत्यापित व पंजीकृत किया गया!")
        print(f"   • शब्द संख्या: {result['word_count']}")
        print(f"   • पंजीकृत उदाहरण: {result['extracted_examples_count']}")
    else:
        print(f"\n❌ पंजीकरण असफल: {result.get('error')}")
        val = result.get("validation_report", {})
        for err in val.get("errors", []):
            print(f"   - {err}")

def cmd_compile(args):
    compiler = BookCompiler()
    print("\nपुस्तक संकलन प्रारंभ हो रहा है...")
    master_path = compiler.compile_full_book()
    print(f"✅ संपूर्ण ग्रंथ सफलतापूर्वक संकलित: {master_path}")
    toc_path = compiler.generate_toc()
    print(f"✅ विषय-सूची (TOC) अद्यतित: {toc_path}\n")

def cmd_examples(args):
    reg = RegistryManager()
    examples = reg.get_all_examples()
    print(f"\n--- पंजीकृत उदाहरण सूची (कुल {len(examples)} उदाहरण) ---")
    for ex in examples:
        print(f"[{ex.id:03d}] [नय {ex.chapter_id:03d}: {ex.naya_name}] {ex.title} ({ex.theme})")
    print()

def cmd_refs_list(args):
    retriever = ReferenceRetriever()
    books = retriever.get_available_books()
    print("\n" + "=" * 70)
    print(f" 📚 संदर्भ ग्रंथालय सूची (REFERENCE LIBRARY - {len(books)} SOURCES)")
    print("=" * 70)
    for idx, b in enumerate(books, 1):
        print(f"  [{idx:02d}] {b['title']}")
        print(f"       फ़ाइल: {b['filename']} ({b['extension']})")
    print("=" * 70 + "\n")

def cmd_search_refs(args):
    retriever = ReferenceRetriever()
    keywords = [k.strip() for k in args.query.split() if len(k.strip()) > 0]
    book_filter = getattr(args, "book", None)
    max_snips = getattr(args, "limit", 4) or 4

    print(f"\n🔍 संदर्भ ग्रंथालय में खोज: '{args.query}'...")
    results = retriever.search(keywords=keywords, max_snippets=max_snips, book_filter=book_filter)

    if not results:
        print("❌ कोई संबंधित शास्त्रीय उद्धरण नहीं मिला।")
        return

    print("\n" + "=" * 75)
    print(f" 📖 प्राप्त शास्त्रीय संदर्भ एवं उद्धरण ({len(results)} परिणाम):")
    print("=" * 75)
    for idx, r in enumerate(results, 1):
        print(f"\n[{idx}] 📜 {r['book']}")
        print(f"    प्रासंगिक पद: '{r['match_term']}' (स्कोर: {r['score']})")
        print(f"    उद्धरण: \"...{r['snippet']}...\"")
        print("-" * 75)
    print()

def main():
    parser = argparse.ArgumentParser(description="नय प्रकाश 203 नय महाग्रंथ एजंटिक वर्कफ्लो")
    subparsers = parser.add_subparsers(dest="command", help="उपलब्ध कमांड्स")

    subparsers.add_parser("status", help="वर्तमान पुस्तक लेखन स्थिति देखें")
    subparsers.add_parser("khandas", help="7 खंडों का विहंगावलोकन")
    
    cat_parser = subparsers.add_parser("catalog", help="203 नयों की कैटलॉग सूची")
    cat_parser.add_argument("--khanda", type=int, help="विशिष्ट खंड के नय देखें (1-7)")

    prompt_parser = subparsers.add_parser("prompt", help="अध्याय या खंड परिचय का लेखन प्रॉम्ट उत्पन्न करें")
    prompt_parser.add_argument("--id", type=int, help="नय आईडी (1-203)")
    prompt_parser.add_argument("--khanda-intro", type=int, help="खंड परिचय आईडी (1-7)")

    val_parser = subparsers.add_parser("validate", help="अध्याय फ़ाइल का सत्यापन करें")
    val_parser.add_argument("--file", required=True, help="मार्कडाउन फ़ाइल का पथ")

    reg_parser = subparsers.add_parser("register", help="सत्यापित अध्याय को पंजीकृत करें")
    reg_parser.add_argument("--file", required=True, help="मार्कडाउन फ़ाइल का पथ")
    reg_parser.add_argument("--id", required=True, type=int, help="नय आईडी (1-203)")

    subparsers.add_parser("compile", help="संपूर्ण पुस्तक और विषय-सूची संकलित करें")
    subparsers.add_parser("examples", help="पंजीकृत उदाहरणों की सूची देखें")

    subparsers.add_parser("refs", help="संदर्भ ग्रंथालय की उपलब्ध पुस्तकें देखें")

    search_parser = subparsers.add_parser("search-refs", help="संदर्भ ग्रंथों में शास्त्रीय उद्धरण खोजें")
    search_parser.add_argument("--query", required=True, help="खोज शब्द (जैसे 'संकल्प', 'अनिष्पन्ने')")
    search_parser.add_argument("--book", help="विशिष्ट पुस्तक का नाम फ़िल्टर")
    search_parser.add_argument("--limit", type=int, default=4, help="अधिकतम परिणाम (डिफ़ॉल्ट 4)")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "khandas":
        cmd_khandas(args)
    elif args.command == "catalog":
        cmd_catalog(args)
    elif args.command == "prompt":
        cmd_prompt(args)
    elif args.command == "validate":
        cmd_validate(args)
    elif args.command == "register":
        cmd_register(args)
    elif args.command == "compile":
        cmd_compile(args)
    elif args.command == "examples":
        cmd_examples(args)
    elif args.command == "refs":
        cmd_refs_list(args)
    elif args.command == "search-refs":
        cmd_search_refs(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
