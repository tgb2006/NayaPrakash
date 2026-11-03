"""Command Line Interface for Sankshipt 2-Page A5 Edition of Naya Prakash."""

import sys
import argparse
from pathlib import Path

from src.core.catalog_loader import CatalogLoader
from src.core.registry_manager import RegistryManager
from src.core.validator import ChapterValidator
from src.core.reference_retriever import ReferenceRetriever
from src.workflow.compiler import BookCompiler
from src.workflow.orchestrator import WorkflowOrchestrator

def format_id(nid: Any) -> str:
    try:
        val = int(str(nid))
        return f"{val:03d}"
    except ValueError:
        return str(nid)

def cmd_status(args):
    reg = RegistryManager()
    summary = reg.get_dashboard_summary()

    print("\n" + "=" * 68)
    print(" 📖  રસપાન — નયનું જ્ઞાન નિર્વાણનું પાન (સંક્ષિપ્ત ૨-પેજ આવૃત્તિ) — STATUS")
    print("=" * 68)
    print(f"  • કુલ નય (અધ્યાય):          {summary['total_nayas']}")
    print(f"  • પૂર્ણ અધ્યાય (Completed):   {summary['completed']}")
    print(f"  • બાકી અધ્યાય (Pending):      {summary['pending']}")
    print(f"  • પ્રગતિ ટકાવારી (Progress):   {summary['percent_completed']}%")
    print(f"  • નોંધાયેલ અદ્વિતીય નવલિકાઓ:   {summary['total_unique_examples']} (લક્ષ્ય ૨૦૩)")
    print("-" * 68)
    print(" 📚 ખંડ-વાર પ્રગતિ (Khanda Progress):")

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

    print("=" * 68 + "\n")

def cmd_khandas(args):
    loader = CatalogLoader()
    khandas = loader.get_khandas()
    print("\n" + "=" * 75)
    print(" 🏛️  સપ્ત ખંડ તેમજ મૂળ નય રૂપરેખા (7 KHANDAS BLUEPRINT)")
    print("=" * 75)
    for k in khandas:
        print(f"\n[ખંડ {k.id}] {k.name_hindi} ({k.sanskrit_name})")
        print(f"  • શ્રેણી: {k.primary_division} | ત્રિવિધ સ્વરૂપ: {k.tri_aspect}")
        print(f"  • અધ્યાય વિસ્તાર: નય {k.range[0]} થી {k.range[1]} (કુલ {k.chapters_count} અધ્યાય)")
        print(f"  • મૂળ સૂત્ર: {k.core_sutra}")
        print(f"  • આગમિક લક્ષણ: {k.agamic_definition}")
    print("\n" + "=" * 75 + "\n")

def cmd_catalog(args):
    loader = CatalogLoader()
    khanda_id = getattr(args, "khanda", None)
    if khanda_id:
        nayas = loader.get_nayas_by_khanda(int(khanda_id))
        print(f"\n--- ખંડ {khanda_id} ના નયોની સૂચિ (કુલ {len(nayas)}) ---")
    else:
        nayas = loader.get_all_nayas()
        print(f"\n--- સંપૂર્ણ ૨૨૫ નય સૂચિ (૨૦૩ મુખ્ય + ૨૨ પેટા-નય) ---")

    for n in nayas:
        nid_str = format_id(n.id)
        print(f"[{nid_str}] {n.name_hindi:<36} | {n.category} ({n.aspect})")
        print(f"      લક્ષણ: {n.definition_brief}")
    print()

def cmd_prompt(args):
    orch = WorkflowOrchestrator()
    if args.khanda_intro:
        prompt = orch.get_prompt_for_khanda_intro(int(args.khanda_intro))
        print(prompt)
    elif args.id:
        try:
            nid = int(args.id)
        except ValueError:
            nid = str(args.id)
        prompt = orch.get_prompt_for_chapter(nid)
        print(prompt)
    else:
        print("કૃપા કરીને --id <નય_આઈડી> અથવા --khanda-intro <ખંડ_આઈડી> નિર્દિષ્ટ કરો.")

def cmd_validate(args):
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"ભૂલ: ફાઇલ મળી નથી - {file_path}")
        return

    content = file_path.read_text(encoding="utf-8")
    validator = ChapterValidator()
    report = validator.validate_content(content)

    print("\n" + "=" * 65)
    print(f" 🔍  અધ્યાય સમીક્ષા અહેવાલ (Sankshipt 2-Page): {file_path.name}")
    print("=" * 65)
    print(f"  • પરિણામ (Verdict):     {'✅ ઉત્તીર્ણ (PASS)' if report.is_valid else '❌ સંશોધન અપેક્ષિત (REVISE)'}")
    print(f"  • કુલ શબ્દો (Words):     {report.total_words} (લક્ષ્ય: ૫૫૦-૬૫૦)")
    print(f"  • અહિંસા અને નૈતિકતા:    {'✅ શુદ્ધ (Compliant)' if report.ahimsa_passed else '❌ ઉલ્લંઘન મળ્યું'}")

    print("\n 📊 પાના-વાર શબ્દ સંખ્યા વિશ્લેષણ:")
    for name, r in report.word_count_reports.items():
        status_sym = "✅" if r.passed else "❌"
        print(f"   {status_sym} {name}: {r.actual_words} શબ્દો ({r.expected_range})")

    if report.missing_sections:
        print("\n ⚠️ ગેરહાજર અનિવાર્ય વિભાગો:")
        for sec in report.missing_sections:
            print(f"   - {sec}")

    if report.errors:
        print("\n ❌ મુખ્ય ક્ષતિઓ:")
        for err in report.errors:
            print(f"   - {err}")

    if report.warnings:
        print("\n ⚠️ ચેતવણીઓ:")
        for w in report.warnings:
            print(f"   - {w}")

    print("=" * 65 + "\n")

def cmd_register(args):
    file_path = Path(args.file)
    try:
        naya_id = int(args.id)
    except ValueError:
        naya_id = str(args.id)
    orch = WorkflowOrchestrator()
    result = orch.process_and_register_chapter(file_path, naya_id)

    if result.get("success"):
        print(f"\n✅ નય {naya_id} નો સંક્ષિપ્ત અધ્યાય સફળતાપૂર્વક ચકાસીને રજિસ્ટર થયો!")
        print(f"   • શબ્દ સંખ્યા: {result['word_count']}")
        print(f"   • નોંધાયેલ નવલિકા: {result['extracted_examples_count']}")
    else:
        print(f"\n❌ રજિસ્ટ્રેશન અસફળ: {result.get('error')}")
        val = result.get("validation_report", {})
        for err in val.get("errors", []):
            print(f"   - {err}")

def cmd_compile(args):
    compiler = BookCompiler()
    print("\nસંક્ષિપ્ત પુસ્તક સંકલન પ્રારંભ થઈ રહ્યું છે (Sankshipt 2-Page A5 Edition)...")
    master_path = compiler.compile_full_book()
    print(f"✅ સંપૂર્ણ સંક્ષિપ્ત મહાગ્રંથ સંકલિત: {master_path}")
    toc_path = compiler.generate_toc()
    print(f"✅ વિષય-સૂચિ અદ્યતન: {toc_path}\n")

def cmd_examples(args):
    reg = RegistryManager()
    examples = reg.get_all_examples()
    print(f"\n--- નોંધાયેલ નવલિકાઓની સૂચિ (કુલ {len(examples)} નવલિકાઓ) ---")
    for ex in examples:
        cid_str = format_id(ex.chapter_id)
        print(f"[{ex.id:03d}] [નય {cid_str}: {ex.naya_name}] {ex.title}")
    print()

def cmd_refs_list(args):
    retriever = ReferenceRetriever()
    books = retriever.get_available_books()
    print("\n" + "=" * 70)
    print(f" 📚 સંદર્ભ ગ્રંથાલય સૂચિ ({len(books)} મૂળ આધારભૂત શાસ્ત્રો)")
    print("=" * 70)
    for idx, b in enumerate(books, 1):
        print(f"  [{idx:02d}] {b['title']}")
        print(f"       ફાઇલ: {b['filename']}")
    print("=" * 70 + "\n")

def cmd_search_refs(args):
    retriever = ReferenceRetriever()
    keywords = [k.strip() for k in args.query.split() if len(k.strip()) > 0]
    book_filter = getattr(args, "book", None)
    max_snips = getattr(args, "limit", 4) or 4

    print(f"\n🔍 સંદર્ભ ગ્રંથાલયમાં શોધ: '{args.query}'...")
    results = retriever.search(keywords=keywords, max_snippets=max_snips, book_filter=book_filter)

    if not results:
        print("❌ કોઈ સંબંધિત શાસ્ત્રીય અવતરણ મળ્યું નથી.")
        return

    print("\n" + "=" * 75)
    print(f" 📖 પ્રાપ્ત શાસ્ત્રીય સંદર્ભો ({len(results)} પરિણામ):")
    print("=" * 75)
    for idx, r in enumerate(results, 1):
        print(f"\n[{idx}] 📜 {r['book']}")
        print(f"    પદ: '{r['match_term']}' (સ્કોર: {r['score']})")
        print(f"    અવતરણ: \"...{r['snippet']}...\"")
        print("-" * 75)
    print()

def main():
    parser = argparse.ArgumentParser(description="રસપાન: નયનું જ્ઞાન નિર્વાણનું પાન (સંક્ષિપ્ત ૨-પેજ A5 આવૃત્તિ CLI)")
    subparsers = parser.add_subparsers(dest="command", help="ઉપલબ્ધ કમાન્ડ્સ")

    p_status = subparsers.add_parser("status", help="પ્રગતિ સ્થિતિ ડેશબોર્ડ")
    p_status.set_defaults(func=cmd_status)

    p_khandas = subparsers.add_parser("khandas", help="૭ ખંડોની બ્લુપ્રિન્ટ")
    p_khandas.set_defaults(func=cmd_khandas)

    p_cat = subparsers.add_parser("catalog", help="૨૨૫ નયોની કેટેલોગ સૂચિ (૨૦૩ મુખ્ય + ૨૨ પેટા-નય)")
    p_cat.add_argument("--khanda", type=int, help="કોઈ વિશિષ્ટ ખંડ આઈડી")
    p_cat.set_defaults(func=cmd_catalog)

    p_prompt = subparsers.add_parser("prompt", help="અધ્યાય લેખન પ્રોમ્પ્ટ મેળવો")
    p_prompt.add_argument("--id", type=str, help="નય આઈડી (દા.ત. 1, 105, 105.1)")
    p_prompt.add_argument("--khanda-intro", type=int, help="ખંડ પરિચય આઈડી (૧ થી ૭)")
    p_prompt.set_defaults(func=cmd_prompt)

    p_val = subparsers.add_parser("validate", help="અધ્યાય ફાઇલનું પરીક્ષણ કરો")
    p_val.add_argument("--file", required=True, help="તપાસવા માટેની ફાઇલનો પાથ")
    p_val.set_defaults(func=cmd_validate)

    p_reg = subparsers.add_parser("register", help="અધ્યાયને ચકાસીને રજિસ્ટર કરો")
    p_reg.add_argument("--file", required=True, help="અધ્યાય ફાઇલનો પાથ")
    p_reg.add_argument("--id", type=str, required=True, help="નય આઈડી (દા.ત. 1, 105, 105.1)")
    p_reg.set_defaults(func=cmd_register)

    p_compile = subparsers.add_parser("compile", help="સંપૂર્ણ સંક્ષિપ્ત મહાગ્રંથ કમ્પાઇલ કરો")
    p_compile.set_defaults(func=cmd_compile)

    p_ex = subparsers.add_parser("examples", help="નોંધાયેલ નવલિકાઓની સૂચિ")
    p_ex.set_defaults(func=cmd_examples)

    p_refs = subparsers.add_parser("refs", help="સંદર્ભ ગ્રંથોની સૂચિ")
    p_refs.set_defaults(func=cmd_refs_list)

    p_srefs = subparsers.add_parser("search-refs", help="સંદર્ભ ગ્રંથોમાં શોધ કરો")
    p_srefs.add_argument("--query", required=True, help="શોધવા માટેનો શબ્દ કે પદ")
    p_srefs.add_argument("--limit", type=int, default=4, help="મહત્તમ પરિણામ સંખ્યા")
    p_srefs.add_argument("--book", type=str, help="વિશિષ્ટ પુસ્તક ફિલ્ટર")
    p_srefs.set_defaults(func=cmd_search_refs)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
