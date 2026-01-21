"""
Unit tests for the text_extractor module.
"""

import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock, mock_open

try:
    from src.app.text_extractor import (
        clean_word_list,
        extract_text_from_pdf,
        extract_text_from_txt,
        extract_text_from_word,
        extract_text
    )
except ImportError:
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from src.app.text_extractor import (
        clean_word_list,
        extract_text_from_pdf,
        extract_text_from_txt,
        extract_text_from_word,
        extract_text
    )


class TestCleanWordList(unittest.TestCase):
    """Test cases for the clean_word_list function."""
    
    def test_basic_word_list(self):
        """Test that basic words pass through unchanged."""
        words = ["hello", "world", "test"]
        result = clean_word_list(words)
        self.assertEqual(result, ["hello", "world", "test"])
    
    def test_remove_punctuation_only_words(self):
        """Test that words consisting only of punctuation are removed."""
        words = ["hello", "...", "world", "!!!", "test"]
        result = clean_word_list(words)
        self.assertEqual(result, ["hello", "world", "test"])
    
    def test_remove_parentheses(self):
        """Test that parentheses are replaced with spaces."""
        words = ["(hello)", "world"]
        result = clean_word_list(words)
        self.assertEqual(result, ["hello", "world"])
    
    def test_remove_commas(self):
        """Test that commas are replaced with spaces."""
        words = ["hello,world", "test"]
        result = clean_word_list(words)
        self.assertEqual(result, ["hello", "world", "test"])
    
    def test_mixed_punctuation(self):
        """Test words with mixed punctuation."""
        words = ["(hello,world)", "test"]
        result = clean_word_list(words)
        self.assertEqual(result, ["hello", "world", "test"])
    
    def test_combine_hyphenated_words(self):
        """Test that hyphenated words at line breaks are combined."""
        words = ["dis-", "connected", "more", "inter-", "national"]
        result = clean_word_list(words)
        self.assertEqual(result, ["disconnected", "more", "international"])
    
    def test_preserve_mid_word_hyphens(self):
        """Test that hyphens in the middle of words are preserved."""
        words = ["well-known", "test"]
        result = clean_word_list(words)
        self.assertEqual(result, ["well-known", "test"])
    
    def test_complex_cleaning(self):
        """Test a complex combination of cleaning operations."""
        words = ["Hello", "(world,", "foo)", "test-", "case", "...", "end"]
        result = clean_word_list(words)
        self.assertEqual(result, ["Hello", "world", "foo", "testcase", "end"])
    
    def test_empty_list(self):
        """Test that empty list returns empty list."""
        words = []
        result = clean_word_list(words)
        self.assertEqual(result, [])
    
    def test_single_word(self):
        """Test single word in list."""
        words = ["hello"]
        result = clean_word_list(words)
        self.assertEqual(result, ["hello"])


class TestExtractTextFromTxt(unittest.TestCase):
    """Test cases for extract_text_from_txt function."""
    
    def test_extract_simple_text(self):
        """Test extracting text from a simple text file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("Hello world\nThis is a test")
            temp_path = f.name
        
        try:
            result = extract_text_from_txt(temp_path)
            self.assertIsNotNone(result)
            self.assertEqual(result, ["Hello", "world", "This", "is", "a", "test"])
        finally:
            os.unlink(temp_path)
    
    def test_extract_text_with_punctuation(self):
        """Test extracting text with punctuation that should be cleaned."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("Hello, world! (Test)")
            temp_path = f.name
        
        try:
            result = extract_text_from_txt(temp_path)
            self.assertIsNotNone(result)
            # Should clean commas and parentheses
            self.assertEqual(result, ["Hello", "world!", "Test"])
        finally:
            os.unlink(temp_path)
    
    def test_extract_empty_file(self):
        """Test extracting from an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            temp_path = f.name
        
        try:
            result = extract_text_from_txt(temp_path)
            self.assertIsNotNone(result)
            self.assertEqual(result, [])
        finally:
            os.unlink(temp_path)
    
    def test_extract_nonexistent_file(self):
        """Test that nonexistent file returns None."""
        result = extract_text_from_txt("/nonexistent/file.txt")
        self.assertIsNone(result)
    
    def test_extract_unicode_text(self):
        """Test extracting text with unicode characters."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("Héllo wörld 你好")
            temp_path = f.name
        
        try:
            result = extract_text_from_txt(temp_path)
            self.assertIsNotNone(result)
            self.assertEqual(result, ["Héllo", "wörld", "你好"])
        finally:
            os.unlink(temp_path)


class TestExtractTextFromPdf(unittest.TestCase):
    """Test cases for extract_text_from_pdf function."""
    
    @patch('src.app.text_extractor.fitz')
    def test_extract_pdf_success(self, mock_fitz):
        """Test successful PDF text extraction."""
        # Mock PDF document
        mock_doc = MagicMock()
        mock_doc.__len__ = lambda self: 2
        mock_page1 = MagicMock()
        mock_page1.get_text.return_value = "Hello world"
        mock_page2 = MagicMock()
        mock_page2.get_text.return_value = "Test page"
        mock_doc.__getitem__ = lambda self, idx: [mock_page1, mock_page2][idx]
        mock_fitz.open.return_value = mock_doc
        
        result = extract_text_from_pdf("test.pdf")
        self.assertIsNotNone(result)
        self.assertEqual(result, ["Hello", "world", "Test", "page"])
        mock_fitz.open.assert_called_once_with("test.pdf")
        mock_doc.close.assert_called_once()
    
    @patch('src.app.text_extractor.fitz')
    def test_extract_pdf_empty_pages(self, mock_fitz):
        """Test PDF with empty pages."""
        mock_doc = MagicMock()
        mock_doc.__len__ = lambda self: 1
        mock_page = MagicMock()
        mock_page.get_text.return_value = ""
        mock_doc.__getitem__ = lambda self, idx: mock_page
        mock_fitz.open.return_value = mock_doc
        
        result = extract_text_from_pdf("empty.pdf")
        self.assertIsNotNone(result)
        self.assertEqual(result, [])
    
    @patch('src.app.text_extractor.fitz')
    def test_extract_pdf_exception(self, mock_fitz):
        """Test PDF extraction with exception."""
        mock_fitz.open.side_effect = Exception("PDF error")
        
        result = extract_text_from_pdf("bad.pdf")
        self.assertIsNone(result)
    
    @patch('src.app.text_extractor.fitz')
    def test_extract_pdf_with_punctuation_cleaning(self, mock_fitz):
        """Test PDF extraction with punctuation that needs cleaning."""
        mock_doc = MagicMock()
        mock_doc.__len__ = lambda self: 1
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Hello, (world)"
        mock_doc.__getitem__ = lambda self, idx: mock_page
        mock_fitz.open.return_value = mock_doc
        
        result = extract_text_from_pdf("test.pdf")
        self.assertIsNotNone(result)
        self.assertEqual(result, ["Hello", "world"])


class TestExtractTextFromWord(unittest.TestCase):
    """Test cases for extract_text_from_word function."""
    
    def test_word_extraction_not_implemented(self):
        """Test that Word extraction returns None (not yet implemented)."""
        result = extract_text_from_word("test.docx")
        self.assertIsNone(result)


class TestExtractText(unittest.TestCase):
    """Test cases for the main extract_text function."""
    
    def test_extract_text_nonexistent_file(self):
        """Test extract_text with nonexistent file."""
        result = extract_text("/nonexistent/file.txt")
        self.assertIsNone(result)
    
    @patch('src.app.text_extractor.extract_text_from_txt')
    def test_extract_text_txt_file(self, mock_extract_txt):
        """Test that txt files are routed to extract_text_from_txt."""
        mock_extract_txt.return_value = ["test", "words"]
        
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_path = f.name
        
        try:
            result = extract_text(temp_path)
            mock_extract_txt.assert_called_once_with(temp_path)
            self.assertEqual(result, ["test", "words"])
        finally:
            os.unlink(temp_path)
    
    @patch('src.app.text_extractor.extract_text_from_pdf')
    def test_extract_text_pdf_file(self, mock_extract_pdf):
        """Test that pdf files are routed to extract_text_from_pdf."""
        mock_extract_pdf.return_value = ["pdf", "words"]
        
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            temp_path = f.name
        
        try:
            result = extract_text(temp_path)
            mock_extract_pdf.assert_called_once_with(temp_path)
            self.assertEqual(result, ["pdf", "words"])
        finally:
            os.unlink(temp_path)
    
    @patch('src.app.text_extractor.extract_text_from_word')
    def test_extract_text_word_file(self, mock_extract_word):
        """Test that Word files are routed to extract_text_from_word."""
        mock_extract_word.return_value = None  # Not implemented yet
        
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as f:
            temp_path = f.name
        
        try:
            result = extract_text(temp_path)
            mock_extract_word.assert_called_once_with(temp_path)
            self.assertIsNone(result)
        finally:
            os.unlink(temp_path)
    
    def test_extract_text_unsupported_file_type(self):
        """Test that unsupported file types return None."""
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as f:
            temp_path = f.name
        
        try:
            result = extract_text(temp_path)
            self.assertIsNone(result)
        finally:
            os.unlink(temp_path)
    
    def test_extract_text_case_insensitive_extension(self):
        """Test that file extensions are case-insensitive."""
        with tempfile.NamedTemporaryFile(suffix='.TXT', delete=False) as f:
            f.write(b"Test content")
            temp_path = f.name
        
        try:
            # Should recognize .TXT as txt file
            result = extract_text(temp_path)
            self.assertIsNotNone(result)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
