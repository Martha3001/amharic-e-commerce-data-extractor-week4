import unittest
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from scripts.data_preprocess import DataPreprocess

class TestDataPreprocess(unittest.TestCase):
    def test_normalize_amharic_removes_size_patterns(self):
        text = "Size #3940#41#42#43 ይህ ሙከራ ነው"
        normalized = DataPreprocess.normalize_amharic(text)
        self.assertNotIn("Size", normalized)
        self.assertNotIn("#3940#41#42#43", normalized)
        self.assertIn("ይህ ሙከራ ነው", normalized)

    def test_normalize_amharic_removes_emojis(self):
        text = "ሰላም 😊 ይህ ሙከራ ነው"
        normalized = DataPreprocess.normalize_amharic(text)
        self.assertNotIn("😊", normalized)
        self.assertIn("ሰላም", normalized)

    def test_tokenize_amharic_only(self):
        text = "ይህ ሙከራ ነው"
        tokens = DataPreprocess.tokenize_amharic(text)
        self.assertIn("ይህ", tokens)
        self.assertIn("ሙከራ", tokens)
        self.assertIn("ነው", tokens)

    def test_tokenize_english_only(self):
        text = "This is a test"
        tokens = DataPreprocess.tokenize_amharic(text)
        self.assertEqual(tokens, ["This", "is", "a", "test"])

    def test_tokenize_mixed_amharic_english(self):
        text = "ይህ test ነው"
        tokens = DataPreprocess.tokenize_amharic(text)
        self.assertIn("ይህ", tokens)
        self.assertIn("test", tokens)
        self.assertIn("ነው", tokens)

if __name__ == "__main__":
    unittest.main()
