"""Unit tests for section-wise prompt generation and chapter assembly."""

import unittest
from pathlib import Path
from src.workflow.orchestrator import WorkflowOrchestrator

class TestSectionPrompts(unittest.TestCase):
    def setUp(self):
        self.orchestrator = WorkflowOrchestrator()

    def test_section_files_exist(self):
        sections_dir = self.orchestrator.sections_prompts_dir
        self.assertTrue(sections_dir.exists())
        for sec_num, filename in self.orchestrator.SECTION_FILES.items():
            file_path = sections_dir / filename
            self.assertTrue(file_path.exists(), f"Missing prompt file: {filename}")

    def test_get_prompt_for_section_1(self):
        prompt = self.orchestrator.get_prompt_for_section(1, 1, lang="gu")
        self.assertIn("## નય", prompt)
        self.assertIn("भूतनैगम नय", prompt)

    def test_get_prompt_for_section_3_has_updated_rules(self):
        prompt = self.orchestrator.get_prompt_for_section(1, 3, lang="gu")
        self.assertIn("## તાર્કિક વિવેચન", prompt)
        self.assertIn("૧૦૦૦ શબ્દો", prompt)
        self.assertIn("વિવેચકતા", prompt)
        self.assertIn("તાર્કિકતા", prompt)
        self.assertIn("વિષય પ્રતિપાદ્યતા", prompt)
        self.assertIn("પેરેગ્રાફ અંતર્ગત સબશીર્ષક", prompt)

    def test_get_prompt_for_section_4_has_dedup_context(self):
        prompt = self.orchestrator.get_prompt_for_section(1, 4, lang="gu")
        self.assertIn("## ઉદાહરણ", prompt)
        self.assertIn("પુનરાવર્તન નિવારણ", prompt)

    def test_get_prompt_for_section_5_has_updated_rules(self):
        prompt = self.orchestrator.get_prompt_for_section(1, 5, lang="gu")
        self.assertIn("## વ્યવહારિક સમજ", prompt)
        self.assertIn("૩૦૦ શબ્દો", prompt)
        self.assertIn("૨૫૦", prompt)
        self.assertIn("મુદ્દા પ્રમાણે", prompt)
        self.assertIn("સમન્વય", prompt)
        self.assertIn("સામંજસ્ય", prompt)
        self.assertIn("સૌહાર્દ", prompt)
        self.assertIn("નિર્ણયની ચોકસાઈ", prompt)
        self.assertIn("વિઝન", prompt)
        self.assertIn("મિશન", prompt)
        self.assertIn("ક્લેરિટી", prompt)
        self.assertIn("પ્યોરિટી", prompt)
        self.assertIn("બ્યુટી", prompt)

    def test_get_prompt_for_section_6_has_updated_rules(self):
        prompt = self.orchestrator.get_prompt_for_section(1, 6, lang="gu")
        self.assertIn("## દાર્શનિક સમજ", prompt)
        self.assertIn("૨૫૦ થી ૩૦૦ શબ્દો", prompt)
        self.assertIn("મુદ્દાસર", prompt)
        self.assertIn("જ્ઞેય", prompt)
        self.assertIn("જ્ઞાયક", prompt)
        self.assertIn("નંબર", prompt)
        self.assertIn("સ્યાદવાદ", prompt)

    def test_get_prompt_for_section_7_has_updated_rules(self):
        prompt = self.orchestrator.get_prompt_for_section(1, 7, lang="gu")
        self.assertIn("## સૈદ્ધાંતિક સમજ", prompt)
        self.assertIn("સામાચારી", prompt)
        self.assertIn("પ્રરૂપણા", prompt)
        self.assertIn("સિદ્ધાંત", prompt)
        self.assertIn("પરંપરા", prompt)
        self.assertIn("સમન્વય", prompt)
        self.assertIn("આગમિક સંદર્ભો", prompt)
        self.assertIn("જૈન પરંપરાનો ઇતિહાસ", prompt)
        self.assertIn("ચોકસાઈ", prompt)
        self.assertIn("ઉપલક માહિતીનો", prompt)

    def test_get_prompt_for_section_8_has_updated_rules(self):
        prompt = self.orchestrator.get_prompt_for_section(1, 8, lang="gu")
        self.assertIn("## સાધનાકીય સમજ", prompt)
        self.assertIn("પ્રયોગ", prompt)
        self.assertIn("પ્રેમ", prompt)
        self.assertIn("મૈત્રી", prompt)
        self.assertIn("સર્વસ્વીકાર", prompt)
        self.assertIn("અંતર્મુખતા", prompt)
        self.assertIn("અનાસક્તિ", prompt)
        self.assertIn("વૈરાગ્ય", prompt)
        self.assertIn("સમર્પણ", prompt)
        self.assertIn("જાગૃતિ", prompt)
        self.assertIn("નિર્લેપતા", prompt)
        self.assertIn("સહજતા", prompt)
        self.assertIn("ધ્યાન", prompt)
        self.assertIn("અસ્તિત્વની અનુભૂતિ", prompt)
        self.assertIn("પરમ વિશ્રામ", prompt)
        self.assertIn("નિર્વિકલ્પ દશા", prompt)
        self.assertIn("મૌન", prompt)
        self.assertIn("ગૂંઠાણા", prompt)
        self.assertIn("સાંપ્રદાયિક", prompt)
        self.assertIn("અસીમ", prompt)

    def test_get_prompt_for_section_9_has_updated_rules(self):
        prompt = self.orchestrator.get_prompt_for_section(1, 9, lang="gu")
        self.assertIn("## ડીપ ડાઈવ", prompt)
        self.assertIn("એકાંત વિરુદ્ધ અનેકાંત", prompt)
        self.assertIn("સુનય વિરુદ્ધ કુનય", prompt)
        self.assertIn("સાધના અને સાવધાની", prompt)
        self.assertIn("નદી", prompt)
        self.assertIn("મહાસાગર", prompt)
        self.assertIn("જીદ", prompt)
        self.assertIn("દ્વાર", prompt)
        self.assertIn("સમન્વય", prompt)
        self.assertIn("ચોકો", prompt)
        self.assertIn("બારી", prompt)
        self.assertIn("આકાશ સાથે અનુસંધાન", prompt)
        self.assertIn("દ્રષ્ટિરાગ", prompt)
        self.assertIn("પડી ન ભાંગે", prompt)
        self.assertIn("એકાંત શું", prompt)
        self.assertIn("અનેકાંત શું", prompt)
        self.assertIn("કુનય શું", prompt)
        self.assertIn("સુનય શું", prompt)
        self.assertIn("સાધના શું", prompt)
        self.assertIn("સાવધાની શું", prompt)

    def test_assemble_chapter(self):
        sections = {
            1: "## નય\n- વિગત ૧",
            2: "## સામાન્ય અર્થ અને શબ્દાર્થ\nઅર્થ વિગત",
            3: "## તાર્કિક વિવેચન\nતાર્કિક વિગત",
            4: "## ઉદાહરણ\nઉદાહરણ ૧",
            5: "## વ્યવહારિક સમજ\nવ્યવહાર વિગત",
            6: "## દાર્શનિક સમજ\nદાર્શનિક વિગત",
            7: "## સૈદ્ધાંતિક સમજ\nસિદ્ધાંત વિગત",
            8: "## સાધનાકીય સમજ\nસાધના વિગત",
            9: "## ડીપ ડાઈવ\nડીપ ડાઈવ વિગત",
            10: "## મંઝિલગામી વલણ\nમંઝિલ વિગત",
        }
        assembled = self.orchestrator.assemble_chapter(1, sections, lang="gu")
        self.assertTrue(assembled.startswith("# અધ્યાય 001: भूतनैगम नय"))
        for title_gu, _ in self.orchestrator.SECTION_TITLES.values():
            self.assertIn(f"## {title_gu}", assembled)

if __name__ == "__main__":
    unittest.main()
