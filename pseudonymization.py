import sys
import argparse
import re
import json

class TextAnonymizer:
    def __init__(self, replacement_file='replacements.json'):
        """
        Initialize the anonymizer with optional replacement file.
        
        :param replacement_file: JSON file to store word-to-code mappings
        """
        self.replacement_file = replacement_file
        self.word_to_code = {}
        self.code_to_word = {}
        self.current_code_index = 1
        
        # Try to load existing replacements
        try:
            with open(replacement_file, 'r') as f:
                loaded_data = json.load(f)
                self.word_to_code = loaded_data['word_to_code']
                self.code_to_word = loaded_data['code_to_word']
                self.current_code_index = len(self.word_to_code) + 1
        except FileNotFoundError:
            pass
    
    def _generate_code(self):
        """
        Generate a unique code for anonymization.
        
        :return: Unique code (X01, X02, etc.)
        """
        code = f'X{self.current_code_index:02d}'
        self.current_code_index += 1
        return code
    
    def anonymize(self, text, words_to_anonymize=None):
        """
        Anonymize the given text by replacing specified words while preserving case.
        
        :param text: Input text to anonymize
        :param words_to_anonymize: List of specific words to anonymize (optional)
        :return: Anonymized text
        """
        # If no specific words provided, split the text into words
        if words_to_anonymize is None:
            words_to_anonymize = set(re.findall(r'\b\w+\b', text))
        
        # Convert to set to remove duplicates
        words_to_anonymize = set(words_to_anonymize)
        
        # Create a copy of the text to modify
        anonymized_text = text
        
        # Anonymize each word
        for word in words_to_anonymize:
            # Skip very short or common words
            if len(word) <= 2 or word.lower() in {'the', 'and', 'a', 'an', 'in', 'to'}:
                continue
            
            # Check if this exact word (with its case) is already known
            matching_code = next((code for code, existing_word in self.code_to_word.items() 
                                  if existing_word.lower() == word.lower()), None)
            
            if matching_code is None:
                # No existing code for this word, create a new one
                code = self._generate_code()
                self.word_to_code[word] = code
                self.code_to_word[code] = word
            else:
                # Use existing code for this word
                code = matching_code
                # Ensure the original case is preserved in our mapping
                self.word_to_code[word] = code
                self.code_to_word[code] = word
            
            # Create a pattern that matches the exact word with its original case
            pattern = r'\b' + re.escape(word) + r'\b'
            
            # Replace the word with its corresponding code
            anonymized_text = re.sub(pattern, code, anonymized_text)
        
        # Save replacements with a more comprehensive structure
        with open(self.replacement_file, 'w') as f:
            json.dump({
                'word_to_code': self.word_to_code,
                'code_to_word': self.code_to_word
            }, f, indent=2)
        
        return anonymized_text
    
    def deanonymize(self, text):
        """
        Restore the original words from anonymized text.
        
        :param text: Anonymized text
        :return: Original text
        """
        # Restore each code to its original word
        deanonymized_text = text
        for code, word in self.code_to_word.items():
            deanonymized_text = deanonymized_text.replace(code, word)
        
        return deanonymized_text

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Case-Preserving Text Anonymization Utility')
    parser.add_argument('input_file', help='Input text file to process')
    parser.add_argument('output_file', help='Output file for processed text')
    parser.add_argument('--reverse', action='store_true', 
                        help='Reverse the anonymization process')
    parser.add_argument('--words', nargs='*', 
                        help='Specific words to anonymize (optional)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create anonymizer
    anonymizer = TextAnonymizer()
    
    # Read input file
    with open(args.input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Process text based on mode
    if args.reverse:
        # Deanonymize
        processed_text = anonymizer.deanonymize(text)
    else:
        # Anonymize
        processed_text = anonymizer.anonymize(text, args.words)
    
    # Write output file
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(processed_text)
    
    print(f"{'Deanonymized' if args.reverse else 'Anonymized'} text saved to {args.output_file}")

if __name__ == '__main__':
    main()
