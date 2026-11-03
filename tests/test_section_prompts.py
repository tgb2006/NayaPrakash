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

    def test_get_prompt_for_section_4_has_dedup_context(self):
        prompt = self.orchestrator.get_prompt_for_section(1, 4, lang="gu")
        self.assertIn("## ઉદાહરણ", prompt)
        self.assertIn("પુનરાવર્તન નિવારણ", prompt)

    def test_get_prompt_for_section_6_has_continuous_paragraph_rule(self):
        prompt = self.orchestrator.get_prompt_for_section(1, 6, lang="gu")
        self.assertIn("## દાર્શનિક સમજ", prompt)
        self.assertIn("કોઈ પણ `###` ઉપ-શીર્ષકો આપવાના નથી", prompt)

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
