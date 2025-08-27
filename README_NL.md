# Text Pseudonimisatie Tool

Een Python-gebaseerde command-line utility voor het anonimiseren en de-anonimiseren van tekst door identifiers te vervangen met codes. Ideaal voor het beschermen van gevoelige informatie in documenten terwijl de tekststructuur behouden blijft.

## Features

- 🔐 **Veilige pseudonimisatie**: Vervangt identifiers met anonieme codes (X01, X02, etc.)
- 🔄 **Reversibele anonimisatie**: Herstel oorspronkelijke tekst met replacement files
- 📝 **Flexibele invoer**: Ondersteuning voor zowel bestanden als interactieve tekst input
- 🎯 **Automatische detectie e-mail adressen**: Herkent e-mail adressen zonder dat ze opgevoerd hoeven te worden in de lijst
- 🎯 **Multi-word ondersteuning**: Detecteert en vervangt ook meerwoord-identifiers
- ⚡ **Automatische naamgeving**: Genereert output bestanden met timestamps
- 📁 **Georganiseerde opslag**: Replacement mappings worden netjes opgeslagen
- 🛡️ **Case-preserving**: Behoudt originele hoofdletter/kleine letter structuur

## Installatie

```bash
git clone https://github.com/jouw-username/text-pseudonymization
cd text-pseudonymization
```

Het script vereist alleen standaard Python 3.x libraries, geen extra installaties nodig.

## Quick Start

### 1. Maak een identifiers bestand

Maak een bestand `identifiers.txt` met de woorden die je wilt anonimiseren (één per regel):

```
John Doe
Jane Smith
Amsterdam
Confidential Project Alpha
geheim
```

### 2. Anonimiseer tekst

```bash
# Van bestand
python pseudonymization.py document.txt

# Interactieve modus
python pseudonymization.py

# Met custom opties
python pseudonymization.py -i my_identifiers.txt -d my_replacements/ document.txt
```

### 3. De-anonimiseer tekst

```bash
python pseudonymization.py -r -f replacements/replacements_document_20241226_143022.json document_anonymized.txt
```

## Gebruik

### Command-line Opties

```
usage: pseudonymization.py [-h] [-r] [-f REPLACEMENT_FILE] [-i IDENTIFIERS_FILE] [-d REPLACEMENTS_DIR] [--no-email] [input_file] [output_file]

Text Pseudonymization Utility - Anonymize and deanonymize text by replacing identifiers with codes

positional arguments:
  input_file            Input text file to process (optional - will prompt for text input if not provided)
  output_file           Output file for processed text (optional - will be auto-generated with timestamp if not provided)

options:
  -h, --help            show this help message and exit
  -r, --reverse         Reverse the anonymization process (deanonymize)
  -f REPLACEMENT_FILE, --replacement-file REPLACEMENT_FILE
                        Specific replacement file to use for deanonymization (required with --reverse)
  -i IDENTIFIERS_FILE, --identifiers-file IDENTIFIERS_FILE
                        File containing identifiers to anonymize, one per line (default: identifiers.txt)
  -d REPLACEMENTS_DIR, --replacements-dir REPLACEMENTS_DIR
                        Directory for storing replacement mapping files (default: replacements/)
  --no-email            Disable automatic email detection and anonymization
```

### Voorbeelden

#### Basis anonimisatie
```bash
python pseudonymization.py document.txt
# Output: document_anonymized_20241226_143022.txt
# Replacement: replacements/replacements_document_20241226_143022.json
```

#### Interactieve modus
```bash
python pseudonymization.py
# Plak je tekst en druk Ctrl+D (Unix/Mac) of Ctrl+Z+Enter (Windows)
```

#### Custom configuratie
```bash
python pseudonymization.py -i custom_identifiers.txt -d my_replacements/ sensitive_data.txt output.txt
```

#### De-anonimisatie
```bash
python pseudonymization.py -r -f replacements/replacements_document_20241226_143022.json document_anonymized.txt
```

## Bestandsstructuur

```
project/
├── pseudonymization.py          # Hoofd script
├── identifiers.txt              # Lijst van te anonimiseren woorden
├── replacements/                # Directory voor replacement bestanden
│   ├── replacements_document_20241226_143022.json
│   └── replacements_report_20241226_144500.json
├── document.txt                 # Origineel document
├── document_anonymized_20241226_143022.txt
└── document_deanonymized_20241226_145000.txt
```

## Hoe het werkt

### Anonimisatie Proces

1. **Identifier Detectie**: Het script zoekt naar woorden en zinnen uit de identifiers lijst
2. **Prioritering**: Langere zinnen hebben voorrang over kortere woorden
3. **Code Generatie**: Elke unieke identifier krijgt een code (X01, X02, etc.)
4. **Replacement**: Alle voorkomens worden vervangen met codes
5. **Mapping Opslag**: Relatie wordt opgeslagen in JSON bestand

### Voorbeeld Transformatie

**Voor anonimisatie:**
```
John Doe werkte aan Confidential Project Alpha in Amsterdam.
Jane Smith coordineerde het project vanuit het hoofdkantoor.
```

**Na anonimisatie:**
```
X01 werkte aan X02 in X03.
X04 coordineerde het project vanuit het hoofdkantoor.
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

And the `replacements.json` would look like:
```json
{
  "word_to_code": {
    "John": "X01",
    "JOHN": "X03",
    "john": "X04",
    "Tech": "X02"
  },
  "code_to_word": {
    "X01": "John",
    "X03": "JOHN", 
    "X04": "john",
    "X02": "Tech"
  }
}
```

## Geavanceerde Features

### Multi-word Identifiers
Het script detecteert automatisch meerwoord-identifiers en geeft deze voorrang:
```
identifiers.txt:
New York
York

Tekst: "I visited New York last year"
Result: "I visited X01 last year" (niet "I visited New X02 last year")
```

### Case Preservation
Originele hoofdlettergebruik wordt behouden:
```
"JOHN DOE and john doe" → "X01 and X01"
```

### Timestamp Matching
Output bestanden en replacement bestanden gebruiken dezelfde timestamp voor eenvoudige koppeling:
```
document_anonymized_20241226_143022.txt
replacements_document_20241226_143022.json
```

## Best Practices

### Identifiers Bestand
- Plaats meest specifieke/langste identifiers eerst
- Gebruik # voor commentaar regels
- Test met voorbeeldtekst voordat je grote bestanden verwerkt

```
# Namen
John Doe
Jane Smith

# Plaatsen  
New York City
Amsterdam

# Projecten
Confidential Project Alpha
Project Beta
```

### Beveiliging
- Bewaar replacement bestanden veilig - deze bevatten de originele identifiers
- Gebruik verschillende replacement directories voor verschillende projecten
- Backup replacement bestanden voordat je ze deelt of verplaatst

### Workflow
1. Test eerst met kleine tekstvoorbeelden
2. Controleer de anonieme output op completheid
3. Bewaar replacement bestanden op veilige locatie
4. Documenteer welke replacement bij welke output hoort

## Troubleshooting

### Veelvoorkomende Problemen

**"No identifiers found"**
- Controleer of `identifiers.txt` bestaat en identifiers bevat
- Zorg dat identifiers exact overeenkomen met tekst in document

**"Replacement file not found"**
- Controleer pad naar replacement bestand
- Zorg dat je het juiste replacement bestand gebruikt voor de tekst

**Onvolledig geanonimiseerd**
- Controleer of alle varianten van namen in identifiers staan
- Let op hoofdlettergebruik en spelling variaties

### Debug Tips
```bash
# Test met verbose output
python pseudonymization.py -i identifiers.txt test_small.txt

# Controleer wat er gevonden wordt in de output
# Script toont altijd welke identifiers het vindt
```

## Contributing

Bijdragen zijn welkom! Open een issue of submit een pull request.

### Development Setup
```bash
git clone https://github.com/jouw-username/text-pseudonymization
cd text-pseudonymization
# Geen extra dependencies nodig
```

## License

Dit project is gelicenseerd onder de MIT License - zie het [LICENSE](LICENSE) bestand voor details.

## Changelog

### v1.0.0
- Basis pseudonimisatie functionaliteit
- Multi-word identifier ondersteuning
- Interactieve tekst input
- Automatische bestandsnaam generatie
- Korte command-line opties

---

**⚠️ Belangrijk**: 
Dit tool is bedoeld voor basis tekstpseudonymisatie. Voor medische, juridische of andere gevoelige data, controleer altijd de output en volg relevante privacy regelgeving.
