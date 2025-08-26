#!/usr/bin/env python3
import sys
import argparse
import re
import json
import os
from datetime import datetime

class TextAnonymizer:
    def __init__(self, identifiers_file='identifiers.txt', replacements_dir='replacements'):
        """
        Initialize the anonymizer with identifiers file and replacements directory.
        
        :param identifiers_file: Text file containing words to anonymize (one per line)
        :param replacements_dir: Directory to store replacement files
        """
        self.identifiers_file = identifiers_file
        self.replacements_dir = replacements_dir
        self.word_to_code = {}
        self.code_to_word = {}
        self.current_code_index = 1
        self.identifiers = set()
        
        # Create replacements directory if it doesn't exist
        if not os.path.exists(replacements_dir):
            os.makedirs(replacements_dir)
        
        # Load identifiers from file
        self._load_identifiers()
    
    def _load_identifiers(self):
        """
        Load identifiers from the identifiers file.
        """
        if not os.path.exists(self.identifiers_file):
            print(f"Warning: Identifiers file '{self.identifiers_file}' not found.")
            print("Please create this file with one identifier per line.")
            return
        
        try:
            with open(self.identifiers_file, 'r', encoding='utf-8') as f:
                for line in f:
                    identifier = line.strip()
                    if identifier and not identifier.startswith('#'):  # Skip empty lines and comments
                        self.identifiers.add(identifier.lower())
            print(f"Loaded {len(self.identifiers)} identifiers from {self.identifiers_file}")
        except Exception as e:
            print(f"Error loading identifiers file: {e}")
            sys.exit(1)
    
    def _generate_replacement_filename(self, input_filename):
        """
        Generate a unique replacement filename with timestamp.
        
        :param input_filename: Name of the input file being processed
        :return: Unique replacement filename
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = os.path.splitext(os.path.basename(input_filename))[0]
        filename = f"replacements_{base_name}_{timestamp}.json"
        full_path = os.path.join(self.replacements_dir, filename)
        
        # Check if file already exists (unlikely but possible)
        counter = 1
        while os.path.exists(full_path):
            filename = f"replacements_{base_name}_{timestamp}_{counter:02d}.json"
            full_path = os.path.join(self.replacements_dir, filename)
            counter += 1
        
        return full_path
    
    def _generate_output_filename(self, input_filename, suffix=""):
        """
        Generate output filename based on input filename with timestamp.
        
        :param input_filename: Original input filename
        :param suffix: Optional suffix to add before timestamp
        :return: Generated output filename
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = os.path.splitext(input_filename)[0]
        extension = os.path.splitext(input_filename)[1]
        
        if suffix:
            return f"{base_name}_{suffix}_{timestamp}{extension}"
        else:
            return f"{base_name}_{timestamp}{extension}"
    
    def _generate_code(self):
        """
        Generate a unique code for anonymization.
        
        :return: Unique code (X01, X02, etc.)
        """
        code = f'X{self.current_code_index:02d}'
        self.current_code_index += 1
        return code
    
    def _should_anonymize_word(self, word):
        """
        Check if a single word should be anonymized based on the identifiers list.
        
        :param word: Word to check
        :return: True if word should be anonymized
        """
        return word.lower() in self.identifiers
    
    def _find_multi_word_matches(self, text):
        """
        Find multi-word identifiers in the text.
        
        :param text: Input text
        :return: List of tuples (start_pos, end_pos, original_phrase, identifier)
        """
        matches = []
        text_lower = text.lower()
        
        # Sort identifiers by length (longest first) to prioritize longer matches
        sorted_identifiers = sorted([id for id in self.identifiers if ' ' in id], 
                                  key=len, reverse=True)
        
        for identifier in sorted_identifiers:
            identifier_lower = identifier.lower()
            start = 0
            
            while True:
                # Find the identifier in the text (case-insensitive)
                pos = text_lower.find(identifier_lower, start)
                if pos == -1:
                    break
                
                # Check if it's a whole phrase (word boundaries)
                end_pos = pos + len(identifier)
                
                # Check start boundary
                if pos > 0 and text[pos-1].isalnum():
                    start = pos + 1
                    continue
                
                # Check end boundary
                if end_pos < len(text) and text[end_pos].isalnum():
                    start = pos + 1
                    continue
                
                # Extract the original phrase with its case
                original_phrase = text[pos:end_pos]
                
                # Check if this position is already covered by a longer match
                overlap = False
                for existing_start, existing_end, _, _ in matches:
                    if (pos >= existing_start and pos < existing_end) or \
                       (end_pos > existing_start and end_pos <= existing_end):
                        overlap = True
                        break
                
                if not overlap:
                    matches.append((pos, end_pos, original_phrase, identifier))
                
                start = pos + 1
        
        # Sort matches by position to process them in order
        return sorted(matches, key=lambda x: x[0])
    
    def anonymize(self, text, input_filename="unknown"):
        """
        Anonymize the given text by replacing identified words and phrases while preserving case.
        
        :param text: Input text to anonymize
        :param input_filename: Name of the input file (for replacement filename generation)
        :return: Tuple of (anonymized_text, replacement_file_path)
        """
        if not self.identifiers:
            print("No identifiers loaded. Text will not be anonymized.")
            return text, None
        
        anonymized_text = text
        items_to_anonymize = set()
        
        # First, find multi-word identifiers
        multi_word_matches = self._find_multi_word_matches(text)
        processed_positions = set()
        
        # Process multi-word matches first (they have priority)
        for start_pos, end_pos, original_phrase, identifier in multi_word_matches:
            # Mark these positions as processed
            for i in range(start_pos, end_pos):
                processed_positions.add(i)
            
            items_to_anonymize.add(original_phrase)
        
        # Then find single words that haven't been processed yet
        words_pattern = r'\b\w+\b'
        for match in re.finditer(words_pattern, text):
            word_start, word_end = match.span()
            word = match.group()
            
            # Skip if this word is part of a multi-word identifier already processed
            if any(pos in processed_positions for pos in range(word_start, word_end)):
                continue
            
            if self._should_anonymize_word(word):
                items_to_anonymize.add(word)
        
        if not items_to_anonymize:
            print("No identifiers found in text. No anonymization needed.")
            return text, None
        
        print(f"Found {len(items_to_anonymize)} identifiers to anonymize:")
        for item in sorted(items_to_anonymize, key=len, reverse=True):
            print(f"  - '{item}'")
        
        # Anonymize each item (longest first to avoid partial replacements)
        for item in sorted(items_to_anonymize, key=len, reverse=True):
            # Check if this item (case-insensitive) already has a code
            existing_code = None
            for existing_item, code in self.word_to_code.items():
                if existing_item.lower() == item.lower():
                    existing_code = code
                    break
            
            if existing_code is None:
                # Create new code for this item
                code = self._generate_code()
                self.word_to_code[item] = code
                self.code_to_word[code] = item
            else:
                # Use existing code
                code = existing_code
                # Store this specific case variant
                self.word_to_code[item] = code
            
            # Replace all occurrences of this item with its code
            # For multi-word phrases, we need word boundaries at start and end
            if ' ' in item:
                # Multi-word phrase - use word boundary at start and end only
                pattern = r'\b' + re.escape(item) + r'\b'
            else:
                # Single word
                pattern = r'\b' + re.escape(item) + r'\b'
            
            anonymized_text = re.sub(pattern, code, anonymized_text, flags=re.IGNORECASE)
        
        # Generate unique replacement file
        replacement_file = self._generate_replacement_filename(input_filename)
        
        # Save replacements
        replacement_data = {
            'metadata': {
                'created': datetime.now().isoformat(),
                'input_file': input_filename,
                'identifiers_file': self.identifiers_file,
                'total_replacements': len(self.word_to_code)
            },
            'word_to_code': self.word_to_code,
            'code_to_word': self.code_to_word
        }
        
        with open(replacement_file, 'w', encoding='utf-8') as f:
            json.dump(replacement_data, f, indent=2, ensure_ascii=False)
        
        print(f"Replacement mapping saved to: {replacement_file}")
        
        return anonymized_text, replacement_file
    
    def deanonymize(self, text, replacement_file):
        """
        Restore the original words from anonymized text using a specific replacement file.
        
        :param text: Anonymized text
        :param replacement_file: Path to the replacement JSON file
        :return: Original text
        """
        if not os.path.exists(replacement_file):
            print(f"Error: Replacement file '{replacement_file}' not found.")
            return text
        
        try:
            with open(replacement_file, 'r', encoding='utf-8') as f:
                replacement_data = json.load(f)
            
            code_to_word = replacement_data.get('code_to_word', {})
            
            if not code_to_word:
                print("No replacement mappings found in file.")
                return text
            
            # Restore each code to its original word
            deanonymized_text = text
            for code, word in code_to_word.items():
                # Use word boundary regex to avoid partial matches
                pattern = r'\b' + re.escape(code) + r'\b'
                deanonymized_text = re.sub(pattern, word, deanonymized_text)
            
            print(f"Deanonymization completed using {len(code_to_word)} mappings.")
            
            return deanonymized_text
            
        except Exception as e:
            print(f"Error reading replacement file: {e}")
            return text

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Text Pseudonimisatie Utility - Anonymize and deanonymize text by replacing identifiers with codes',
        epilog="""
Examples:
  %(prog)s document.txt                           # Anonymize document.txt
  %(prog)s document.txt output.txt                # Anonymize with specific output file
  %(prog)s                                        # Interactive mode - paste text to anonymize
  %(prog)s -r -f replacements/file.json input.txt # Deanonymize using replacement file
  %(prog)s -i custom_ids.txt -d my_replacements/  # Use custom identifiers and directory

The program replaces identifiers (names, places, etc.) with anonymous codes (X01, X02, ...)
while maintaining text structure. Replacement mappings are saved for later deanonymization.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input_file', nargs='?', 
                        help='Input text file to process (optional - will prompt for text input if not provided)')
    parser.add_argument('output_file', nargs='?', 
                        help='Output file for processed text (optional - will be auto-generated with timestamp if not provided)')
    
    # Short and long options
    parser.add_argument('-r', '--reverse', action='store_true', 
                        help='Reverse the anonymization process (deanonymize)')
    parser.add_argument('-f', '--replacement-file', 
                        help='Specific replacement file to use for deanonymization (required with --reverse)')
    parser.add_argument('-i', '--identifiers-file', default='identifiers.txt',
                        help='File containing identifiers to anonymize, one per line (default: identifiers.txt)')
    parser.add_argument('-d', '--replacements-dir', default='replacements',
                        help='Directory for storing replacement mapping files (default: replacements/)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle input - either from file or user input
    input_filename = "user_input"  # Default filename for user input
    
    if args.input_file:
        # Check if input file exists
        if not os.path.exists(args.input_file):
            print(f"Error: Input file '{args.input_file}' not found.")
            sys.exit(1)
        
        # Read input file
        try:
            with open(args.input_file, 'r', encoding='utf-8') as f:
                text = f.read()
            input_filename = args.input_file
        except Exception as e:
            print(f"Error reading input file: {e}")
            sys.exit(1)
    else:
        # Prompt for text input
        print("No input file specified. Please enter/paste your text below.")
        print("Press Ctrl+D (Unix/Mac) or Ctrl+Z+Enter (Windows) when finished:")
        print("-" * 50)
        
        try:
            # Read multiple lines until EOF
            lines = []
            while True:
                try:
                    line = input()
                    lines.append(line)
                except EOFError:
                    break
            text = '\n'.join(lines)
            
            if not text.strip():
                print("No text entered. Exiting.")
                sys.exit(1)
                
            print("-" * 50)
            print(f"Received {len(text)} characters of text.")
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(1)
    
    # Create anonymizer
    anonymizer = TextAnonymizer(args.identifiers_file, args.replacements_dir)
    
    # Generate output filename if not provided
    if not args.output_file:
        if args.reverse:
            args.output_file = anonymizer._generate_output_filename(input_filename, "deanonymized")
        else:
            args.output_file = anonymizer._generate_output_filename(input_filename, "anonymized")
        print(f"Auto-generated output filename: {args.output_file}")
    
    # Process text based on mode
    if args.reverse:
        # Deanonymize
        if not args.replacement_file:
            print("Error: --replacement-file (-f) is required for deanonymization.")
            sys.exit(1)
        
        processed_text = anonymizer.deanonymize(text, args.replacement_file)
        operation = "Deanonymized"
    else:
        # Anonymize
        processed_text, replacement_file = anonymizer.anonymize(text, input_filename)
        operation = "Anonymized"
    
    # Write output file
    try:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(processed_text)
        
        print(f"{operation} text saved to {args.output_file}")
        
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

