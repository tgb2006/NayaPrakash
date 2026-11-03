"""Unit tests for prompt generation and orchestrator in Sankshipt 2-Page edition."""

import unittest
from src.workflow.orchestrator import WorkflowOrchestrator

class TestSankshiptOrchestrator(unittest.TestCase):
    def setUp(self):
        self.orchestrator = WorkflowOrchestrator()

    def test_chapter_prompt_generation(self):
        prompt = self.orchestrator.get_prompt_for_chapter(1)
        self.assertIn("સંક્ષિપ્ત ૨-પેજ અધ્યાય", prompt)
        self.assertIn("ડાબું પાનું", prompt)
        self.assertIn("જમણું પાનું", prompt)
        self.assertIn("નવલિકા", prompt)
        self.assertIn("ભૂતનૈગમ નય", prompt)

    def test_khanda_intro_prompt_generation(self):
        prompt = self.orchestrator.get_prompt_for_khanda_intro(1)
        self.assertIn("ખંડ પરિચય", prompt)
        self.assertIn("૯૦૦ થી ૧૧૫૦ શબ્દો", prompt)
        self.assertIn("શ્વેતામ્બર", prompt)
        self.assertIn("આગમ-આધાર", prompt)
        self.assertIn("તત્વ-વિસ્તાર", prompt)
        self.assertIn("શાખા-પ્રસાર", prompt)
        self.assertIn("नैगम नय", prompt)

if __name__ == "__main__":
    unittest.main()
