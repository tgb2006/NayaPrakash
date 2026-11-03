"""Unit tests for registry and deduplication."""

import unittest
import tempfile
import json
import shutil
from pathlib import Path
from src.core.registry_manager import RegistryManager

class TestRegistryAndDeduplication(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.data_dir = self.test_dir / "data"
        self.data_dir.mkdir(parents=True)
        self.config_dir = self.test_dir / "config"
        self.config_dir.mkdir(parents=True)

        # Initialize mock progress tracker
        progress = {
            "total_nayas": 203,
            "completed_count": 0,
            "pending_count": 203,
            "khanda_progress": {str(i): {"total": 10, "completed": 0} for i in range(1, 8)},
            "chapters_state": {
                "1": {"id": 1, "khanda_id": 1, "status": "pending", "file_path": None, "word_count": 0, "validation_passed": False}
            }
        }
        with open(self.data_dir / "progress_tracker.json", "w", encoding="utf-8") as f:
            json.dump(progress, f)

        self.reg = RegistryManager(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_add_examples_and_deduplication(self):
        examples_ch1 = [
            {
                "title": "डिजिटल आर्किटेक्ट का ब्लूप्रिंट",
                "theme": "सॉफ्टवेयर विकास",
                "summary": "एक इंजीनियर केवल कोड का खाका देखकर कहता है कि सॉफ्टवेयर तैयार हो गया।",
                "keywords": ["सॉफ्टवेयर", "आर्किटेक्ट", "ब्लूप्रिंट", "इंजीनियर"]
            },
            {
                "title": "मूर्तिकार की दृष्टि",
                "theme": "कला",
                "summary": "पत्थर की अनगढ़ शिला में मूर्तिकार पहले से ही भगवान की मूर्ति देखता है।",
                "keywords": ["मूर्तिकार", "शिला", "मूर्ति", "कला"]
            }
        ]

        self.reg.add_examples_for_chapter(1, "संकल्पग्राही नैगम नय", examples_ch1)
        all_ex = self.reg.get_all_examples()
        self.assertEqual(len(all_ex), 2)

        # Test duplicate detection by title
        dupes_title = self.reg.check_duplicate("डिजिटल आर्किटेक्ट का ब्लूप्रिंट", "कोई भिन्न विवरण")
        self.assertTrue(len(dupes_title) > 0, "Should detect duplicate title.")

        # Test duplicate detection by keywords
        dupes_kw = self.reg.check_duplicate("नया शीर्षक", "कुछ", ["सॉफ्टवेयर", "आर्किटेक्ट", "ब्लूप्रिंट"])
        self.assertTrue(len(dupes_kw) > 0, "Should detect duplicate keywords overlap.")

        # Non-duplicate should return empty
        no_dupes = self.reg.check_duplicate("किसान का बीज बोना", "पृथ्वी में अन्न का संकल्प", ["किसान", "बीज", "फसल"])
        self.assertEqual(len(no_dupes), 0)

    def test_update_chapter_status(self):
        self.reg.update_chapter_status(1, "completed", "output/ch1.md", 2150, True)
        summary = self.reg.get_dashboard_summary()
        self.assertEqual(summary["completed"], 1)
        self.assertEqual(summary["pending"], 202)

if __name__ == "__main__":
    unittest.main()
