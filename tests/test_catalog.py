"""Unit tests for catalog integrity."""

import unittest
from pathlib import Path
from src.core.catalog_loader import CatalogLoader

class TestCatalogIntegrity(unittest.TestCase):
    def setUp(self):
        self.loader = CatalogLoader()

    def test_total_nayas_count(self):
        nayas = self.loader.get_all_nayas()
        self.assertEqual(len(nayas), 203, "Catalog must contain exactly 203 nayas.")

    def test_sequential_ids(self):
        nayas = self.loader.get_all_nayas()
        for idx, naya in enumerate(nayas, start=1):
            self.assertEqual(naya.id, idx, f"Naya at index {idx} should have id {idx}")

    def test_khanda_distribution(self):
        khandas = self.loader.get_khandas()
        self.assertEqual(len(khandas), 7, "There must be exactly 7 Khandas.")
        
        expected_counts = {
            1: 35,
            2: 32,
            3: 38,
            4: 30,
            5: 24,
            6: 22,
            7: 22
        }
        total = 0
        for k in khandas:
            self.assertEqual(k.chapters_count, expected_counts[k.id])
            k_nayas = self.loader.get_nayas_by_khanda(k.id)
            self.assertEqual(len(k_nayas), expected_counts[k.id])
            total += len(k_nayas)

        self.assertEqual(total, 203)

    def test_categories_and_aspects(self):
        nayas = self.loader.get_all_nayas()
        valid_categories = {"द्रव्यार्थिक नय", "पर्यायार्थिक नय"}
        valid_aspects = {"ज्ञाननय", "अर्थनय", "शब्दनय"}

        for n in nayas:
            self.assertIn(n.category, valid_categories)
            self.assertIn(n.aspect, valid_aspects)
            self.assertTrue(len(n.name_hindi) > 0)
            self.assertTrue(len(n.definition_brief) > 0)

if __name__ == "__main__":
    unittest.main()
