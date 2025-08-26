# Text Pseudonymization Tool

A Python-based command-line utility for anonymizing and deanonymizing text by replacing identifiers with codes. Ideal for protecting sensitive information in documents while maintaining text structure.

## Features

- 🔐 **Secure pseudonymization**: Replaces identifiers with anonymous codes (X01, X02, etc.)
- 🔄 **Reversible anonymization**: Restore original text using replacement files
- 📝 **Flexible input**: Support for both file input and interactive text input
- 🎯 **Multi-word support**: Detects and replaces multi-word identifiers
- ⚡ **Automatic naming**: Generates output files with timestamps
- 📁 **Organized storage**: Replacement mappings are neatly stored
- 🛡️ **Case-preserving**: Maintains original capitalization structure

## Installation

```bash
git clone https://github.com/your-username/text-pseudonymization
cd text-pseudonymization
```

The script only requires standard Python 3.x libraries, no additional installations needed.

## Quick Start

### 1. Create an identifiers file

Create a file `identifiers.txt` with the words you want to anonymize (one per line):

```
John Doe
Jane Smith
Amsterdam
Confidential Project Alpha
secret
```

### 2. Anonymize text

```bash
# From file
python pseudonymization.py document.txt

# Interactive mode
python pseudonymization.py

# With custom options
python pseudonymization.py -i my_identifiers.txt -d my_replacements/ document.txt
```

### 3. Deanonymize text

```bash
python pseudonymization.py -r -f replacements/replacements_document_20241226_143022.json document_anonymized.txt
```

## Usage

### Command-line Options

```
usage: pseudonymization.py [-h] [-r] [-f REPLACEMENT_FILE] [-i IDENTIFIERS_FILE] 
                           [-d REPLACEMENTS_DIR] [input_file] [output_file]

Options:
  input_file            Input text file (optional - prompts for text if not provided)
  output_file           Output file (optional - auto-generated with timestamp)
  
  -h, --help           Show help message
  -r, --reverse        Reverse the anonymization process (deanonymize)
  -f, --replacement-file  Replacement file for deanonymization (required with -r)
  -i, --identifiers-file  File containing identifiers (default: identifiers.txt)
  -d, --replacements-dir  Directory for replacement files (default: replacements/)
```

### Examples

#### Basic anonymization
```bash
python pseudonymization.py document.txt
# Output: document_anonymized_20241226_143022.txt
# Replacement: replacements/replacements_document_20241226_143022.json
```

#### Interactive mode
```bash
python pseudonymization.py
# Paste your text and press Ctrl+D (Unix/Mac) or Ctrl+Z+Enter (Windows)
```

#### Custom configuration
```bash
python pseudonymization.py -i custom_identifiers.txt -d my_replacements/ sensitive_data.txt output.txt
```

#### Deanonymization
```bash
python pseudonymization.py -r -f replacements/replacements_document_20241226_143022.json document_anonymized.txt
```

## File Structure

```
project/
├── pseudonymization.py          # Main script
├── identifiers.txt              # List of words to anonymize
├── replacements/                # Directory for replacement files
│   ├── replacements_document_20241226_143022.json
│   └── replacements_report_20241226_144500.json
├── document.txt                 # Original document
├── document_anonymized_20241226_143022.txt
└── document_deanonymized_20241226_145000.txt
```

## How It Works

### Anonymization Process

1. **Identifier Detection**: The script searches for words and phrases from the identifiers list
2. **Prioritization**: Longer phrases take precedence over shorter words
3. **Code Generation**: Each unique identifier gets a code (X01, X02, etc.)
4. **Replacement**: All occurrences are replaced with codes
5. **Mapping Storage**: Relationships are stored in JSON file

### Example Transformation

**Before anonymization:**
```
John Doe worked on Confidential Project Alpha in Amsterdam.
Jane Smith coordinated the project from headquarters.
```

**After anonymization:**
```
X01 worked on X02 in X03.
X04 coordinated the project from headquarters.
```

**Replacement mapping:**
```json
{
  "word_to_code": {
    "John Doe": "X01",
    "Confidential Project Alpha": "X02",
    "Amsterdam": "X03",
    "Jane Smith": "X04"
  }
}
```

## Advanced Features

### Multi-word Identifiers
The script automatically detects multi-word identifiers and prioritizes them:
```
identifiers.txt:
New York
York

Text: "I visited New York last year"
Result: "I visited X01 last year" (not "I visited New X02 last year")
```

### Case Preservation
Original capitalization is maintained:
```
"JOHN DOE and john doe" → "X01 and X01"
```

### Timestamp Matching
Output files and replacement files use the same timestamp for easy pairing:
```
document_anonymized_20241226_143022.txt
replacements_document_20241226_143022.json
```

## Best Practices

### Identifiers File
- Place most specific/longest identifiers first
- Use # for comment lines
- Test with sample text before processing large files

```
# Names
John Doe
Jane Smith

# Places  
New York City
Amsterdam

# Projects
Confidential Project Alpha
Project Beta
```

### Security
- Store replacement files securely - they contain the original identifiers
- Use different replacement directories for different projects
- Backup replacement files before sharing or moving them

### Workflow
1. Test first with small text samples
2. Check the anonymized output for completeness
3. Store replacement files in a secure location
4. Document which replacement belongs to which output

## Troubleshooting

### Common Issues

**"No identifiers found"**
- Check if `identifiers.txt` exists and contains identifiers
- Ensure identifiers match exactly with text in document

**"Replacement file not found"**
- Check path to replacement file
- Make sure you're using the correct replacement file for the text

**Incomplete anonymization**
- Check if all variants of names are in identifiers
- Pay attention to capitalization and spelling variations

### Debug Tips
```bash
# Test with verbose output
python pseudonymization.py -i identifiers.txt test_small.txt

# Check what's found in the output
# Script always shows which identifiers it finds
```

## Contributing

Contributions are welcome! Open an issue or submit a pull request.

### Development Setup
```bash
git clone https://github.com/your-username/text-pseudonymization
cd text-pseudonymization
# No extra dependencies needed
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0
- Basic pseudonymization functionality
- Multi-word identifier support
- Interactive text input
- Automatic filename generation
- Short command-line options

---

**⚠️ Important**: 

This tool is designed for basic text pseudonymization. For medical, legal, or other sensitive data, always verify the output and follow relevant privacy regulations.
