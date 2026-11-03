"""Unit tests for catalog integrity."""

import unittest
from pathlib import Path
from src.core.catalog_loader import CatalogLoader

class TestCatalogIntegrity(unittest.TestCase):
    def setUp(self):
        self.loader = CatalogLoader()

    def test_total_nayas_count(self):
        nayas = self.loader.get_all_nayas()
        self.assertEqual(len(nayas), 225, "Catalog must contain exactly 225 nayas (203 primary + 22 sub-nayas).")

    def test_sequential_ids(self):
        nayas = self.loader.get_all_nayas()
        int_ids = [n.id for n in nayas if isinstance(n.id, int) or (isinstance(n.id, str) and n.id.isdigit())]
        int_ids_set = {int(x) for x in int_ids}
        for i in range(1, 204):
            self.assertIn(i, int_ids_set, f"Primary naya ID {i} should be present in catalog")
        
        sub_ids = [str(n.id) for n in nayas if "." in str(n.id)]
        self.assertEqual(len(sub_ids), 22, "Must contain exactly 22 decimal sub-nayas")
        self.assertIn("105.1", sub_ids)
        self.assertIn("106.1", sub_ids)

    def test_khanda_distribution(self):
        khandas = self.loader.get_khandas()
        self.assertEqual(len(khandas), 7, "There must be exactly 7 Khandas.")
        
        expected_counts = {
            1: 6,
            2: 14,
            3: 133,
            4: 18,
            5: 8,
            6: 11,
            7: 35
        }
        total = 0
        for k in khandas:
            self.assertEqual(k.chapters_count, expected_counts[k.id])
            k_nayas = self.loader.get_nayas_by_khanda(k.id)
            self.assertEqual(len(k_nayas), expected_counts[k.id])
            total += len(k_nayas)

        self.assertEqual(total, 225)

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
