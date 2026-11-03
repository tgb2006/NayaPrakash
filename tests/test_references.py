"""Unit tests for ReferenceRetriever and reference search."""

import unittest
from pathlib import Path
from src.core.reference_retriever import ReferenceRetriever

class TestReferenceRetriever(unittest.TestCase):
    def setUp(self):
        self.retriever = ReferenceRetriever()

    def test_books_detection(self):
        books = self.retriever.get_available_books()
        self.assertGreaterEqual(len(books), 5, "At least 5 reference books should be detected.")
        filenames = [b["filename"] for b in books]
        self.assertIn("Aalappaddhati_Acharya_Devasena.txt", filenames)
        self.assertIn("Nayavimshika_Acharya_Abhayshekharsuri.txt", filenames)
        self.assertIn("Panchadhyayi_Nayachakra_Original.txt", filenames)

    def test_search_stemming(self):
        # Search for inflected form 'अनिष्पन्ने'
        results = self.retriever.search(["अनिष्पन्ने"], max_snippets=2)
        self.assertGreater(len(results), 0, "Stemmed search for 'अनिष्पन्ने' should find matches in references.")
        self.assertTrue(any("Aalappaddhati" in r["filename"] or "Nayavimshika" in r["filename"] or "saptabhangi" in r["filename"] or "आलापपद्धति" in r["book"] for r in results))

    def test_naya_reference_formatting(self):
        context = self.retriever.format_reference_context_for_prompt(1, "संकल्पग्राही नैगम नय", 1)
        self.assertIn("CLASSICAL SCRIPTURAL EXCERPTS", context)
        self.assertIn("आलापपद्धति", context)

    def test_gujarati_and_hindi_bilingual_search(self):
        # Search with Gujarati or Hindi terms
        results = self.retriever.search(["સંગ્રહ", "संग्रह"], max_snippets=2)
        self.assertGreater(len(results), 0, "Search for Sangraha should return valid snippets.")

if __name__ == "__main__":
    unittest.main()
