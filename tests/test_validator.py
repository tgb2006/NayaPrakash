"""Unit tests for chapter validator."""

import unittest
from src.core.validator import ChapterValidator

class TestChapterValidator(unittest.TestCase):
    def setUp(self):
        self.validator = ChapterValidator()

    def test_missing_sections_detection(self):
        incomplete_text = """
## 1. नय
संकल्पग्राही नैगम नय

## 2. सामान्य अर्थ एवं शब्दार्थ
संकल्प मात्र को ग्रहण करने वाला।
"""
        report = self.validator.validate_content(incomplete_text)
        self.assertFalse(report.is_valid)
        self.assertIn("सेक्शन 3", report.missing_sections)
        self.assertIn("सेक्शन 10", report.missing_sections)

    def test_word_count_and_ahimsa_failure(self):
        # Text with ethical violation
        bad_text = """
## 1. नय
संकल्पग्राही नैगम नय
## 2. सामान्य अर्थ एवं शब्दार्थ
अर्थ
## 3. तार्किक विवेचन
""" + " शब्द" * 460 + """
## 4. 3 उदाहरण
उदाहरण विवरण
## 5. व्यवहारिक समज
समझ
## 6. दार्शनिक समज़
दर्शन
## 7. सैद्धांतिक समज़
सिद्धांत
## 8. साधनाकिय समज़
साधना
## 9. डीप डाईव
""" + " शब्द" * 310 + """
## 10. मंझिलगामी रूख
यहाँ कसाई का काम अच्छा बताया गया है जो हिंसा करता है।
""" + " शब्द" * 190

        report = self.validator.validate_content(bad_text)
        self.assertFalse(report.is_valid)
        self.assertFalse(report.ahimsa_passed)
        self.assertTrue(len(report.prohibited_issues_found) > 0)

    def test_valid_chapter(self):
        valid_text = """
## 1. नय
संकल्पग्राही नैगम नय (ज्ञाननय - द्रव्यार्थिक)

## 2. सामान्य अर्थ एवं शब्दार्थ
अनिष्पन्न कार्य में केवल संकल्प मात्र को मुख्य कर वस्तु का ग्रहण करना।

## 3. तार्किक विवेचन
""" + "तार्किक विवेचन के अंतर्गत जैन न्याय की दृष्टि से प्रमाण और नय का संबंध स्थापित किया जाता है। " * 45 + """

## 4. 3 उदाहरण
### उदाहरण 1: अंतरिक्ष वैज्ञानिक का संकल्प
मंगलयान के निर्माण से पूर्व वैज्ञानिकों का संकल्प।
### उदाहरण 2: मूर्तिकार की अंतर्दृष्टि
पाषाण खंड में तीर्थंकर की प्रतिमा का दर्शन।
### उदाहरण 3: किसान का बीज-वपन
भूमि में बीज डालते हुए अन्न-राशि का संकल्प।

## 5. व्यवहारिक समज
दैनिक जीवन में किसी भी कार्य की सिद्धि के मूल में संकल्प शक्ति का कार्य करना।

## 6. दार्शनिक समज़
जैन दर्शन के अनुसार ज्ञान की संकल्प-शक्ति बाह्य क्रिया से पूर्ववर्ती होती है।

## 7. सैद्धांतिक समज़
षट्द्रव्यों में जीव द्रव्य की चेतना का संकल्प रूप परिणमन।

## 8. साधनाकिय समज़
मोक्ष मार्ग में प्रथम पग आत्म-साधना का संकल्प ही है।

## 9. डीप डाईव
""" + "एकांत और अनेकांत का सूक्ष्म संतुलन साधते हुए जब हम इस नय का अनुशीलन करते हैं तब सुनय और कुनय का भेद स्पष्ट होता है। " * 28 + """

## 10. मंझिलगामी रूख
""" + "इस नय का चरम प्रयोजन मात्र बौद्धिक जिज्ञासा शांत करना नहीं, अपितु आत्मोपलब्धि के मोक्ष मार्ग पर अग्रसर होना है। " * 18 + """
"""
        report = self.validator.validate_content(valid_text)
        self.assertTrue(report.is_valid, f"Validation errors: {report.errors}")
        self.assertTrue(report.ahimsa_passed)
        self.assertEqual(len(report.missing_sections), 0)

if __name__ == "__main__":
    unittest.main()
