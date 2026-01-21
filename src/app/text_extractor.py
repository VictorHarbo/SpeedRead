"""
Text extraction module for SpeedRead.
Handles extraction of text from various file formats (PDF, Word, TXT).
"""

from typing import Optional, List
import os
import fitz  # PyMuPDF
import string


def clean_word_list(words: List[str], citation_style: str = "none") -> List[str]:
    """
    Clean the word list by removing parentheses and commas, and combining hyphenated words.
    
    Args:
        words: List of words to clean
        citation_style: Citation style filter ("none", "notes", "parenthesis", "numeric")
        
    Returns:
        Cleaned list of words
    """
    cleaned_words = []
    
    for word in words:
        # Step 1: Skip words that consist only of punctuation marks
        if all(c in string.punctuation for c in word):
            continue
        
        # Step 2: Replace (, ), with spaces
        cleaned_word = word
        replacement_occurred = False
        
        for char in ['(', ')', ',']:
            if char in cleaned_word:
                cleaned_word = cleaned_word.replace(char, ' ')
                replacement_occurred = True
        
        # Step 3: If replacement occurred, trim leading/trailing spaces
        if replacement_occurred:
            cleaned_word = cleaned_word.strip()
            
            # Step 4 & 5: Check if spaces are present and split if needed
            if ' ' in cleaned_word:
                # Split into multiple words
                split_words = cleaned_word.split()
                cleaned_words.extend(split_words)
            else:
                # Single word after cleaning
                if cleaned_word:  # Only add non-empty strings
                    cleaned_words.append(cleaned_word)
        else:
            # No replacement, keep original word
            cleaned_words.append(word)
    
    # Step 6: Combine words ending with '-' with the following word
    i = 0
    while i < len(cleaned_words):
        if cleaned_words[i].endswith('-') and i + 1 < len(cleaned_words):
            # Remove the hyphen and combine with next word
            combined_word = cleaned_words[i][:-1] + cleaned_words[i + 1]
            cleaned_words[i] = combined_word
            # Remove the next word since it's been combined
            cleaned_words.pop(i + 1)
        i += 1
    
    return cleaned_words


def extract_text_from_pdf(file_path: str, citation_style: str = "none") -> Optional[List[str]]:
    """
    Extract all text from a PDF file using PyMuPDF.
    
    Args:
        file_path: Path to the PDF file
        citation_style: Citation style filter ("none", "notes", "parenthesis", "numeric")
        
    Returns:
        List of words, or None if extraction fails
    """
    try:        
        # Open the PDF
        doc = fitz.open(file_path)
        text_parts = []
        
        # Extract text from each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            if page_text:
                text_parts.append(page_text)
        
        # Combine all pages
        full_text = "\n\n".join(text_parts)
        
        # Store page count before closing
        total_pages = len(doc)
        
        # Close the document
        doc.close()
        
        # Split text into individual words
        words = full_text.split()
        
        # Clean the word list
        words = clean_word_list(words, citation_style)
        
        print(f"\n{'='*60}")
        print(f"PDF TEXT EXTRACTION: {os.path.basename(file_path)}")
        print(f"Total pages: {total_pages}")
        print(f"Total characters: {len(full_text)}")
        print(f"Total words: {len(words)}")
        print(f"{'='*60}")
        print(f"\nWord list:")
        print(words)
        print(f"\n{'='*60}\n")
        
        return words
        
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None


def extract_text_from_txt(file_path: str, citation_style: str = "none") -> Optional[List[str]]:
    """
    Read text from a plain text file.
    
    Args:
        file_path: Path to the text file
        citation_style: Citation style filter ("none", "notes", "parenthesis", "numeric")
        
    Returns:
        List of words, or None if reading fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        words = text.split()
        
        # Clean the word list
        words = clean_word_list(words, citation_style)
        
        print(f"\n{'='*60}")
        print(f"TEXT FILE LOADED: {os.path.basename(file_path)}")
        print(f"Total characters: {len(text)}")
        print(f"Total words: {len(words)}")
        print(f"{'='*60}")
        print(text)
        print(f"{'='*60}\n")
        
        return words
        
    except Exception as e:
        print(f"Error reading text file: {e}")
        return None


def extract_text_from_word(file_path: str, citation_style: str = "none") -> Optional[str]:
    """
    Extract text from a Word document (.doc or .docx).
    
    Args:
        file_path: Path to the Word document
        citation_style: Citation style filter ("none", "notes", "parenthesis", "numeric")
        
    Returns:
        Extracted text as a string, or None if extraction fails
    """
    # TODO: Implement Word document extraction
    # Will require python-docx library
    print(f"Word document extraction not yet implemented: {file_path}")
    return None


def extract_text(file_path: str, citation_style: str = "none") -> Optional[List[str]]:
    """
    Extract text from a file based on its extension.
    
    Args:
        file_path: Path to the file
        citation_style: Citation style filter ("none", "notes", "parenthesis", "numeric")
        
    Returns:
        List of words, or None if extraction fails
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return None
    
    file_extension = file_path.lower().split('.')[-1]
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(file_path, citation_style)
    elif file_extension == 'txt':
        return extract_text_from_txt(file_path, citation_style)
    elif file_extension in ['doc', 'docx']:
        return extract_text_from_word(file_path, citation_style)
    else:
        print(f"Unsupported file type: {file_extension}")
        return None
