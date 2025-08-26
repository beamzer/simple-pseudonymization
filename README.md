<<<<<<< HEAD
# Text Pseudonimisatie Tool

Een Python-gebaseerde command-line utility voor het anonimiseren en de-anonimiseren van tekst door identifiers te vervangen met codes. Ideaal voor het beschermen van gevoelige informatie in documenten terwijl de tekststructuur behouden blijft.

## Features

- 🔐 **Veilige pseudonimisatie**: Vervangt identifiers met anonieme codes (X01, X02, etc.)
- 🔄 **Reversibele anonimisatie**: Herstel oorspronkelijke tekst met replacement files
- 📝 **Flexibele invoer**: Ondersteuning voor zowel bestanden als interactieve tekst input
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
usage: pseudonymization.py [-h] [-r] [-f REPLACEMENT_FILE] [-i IDENTIFIERS_FILE] 
                           [-d REPLACEMENTS_DIR] [input_file] [output_file]

Opties:
  input_file            Input tekstbestand (optioneel - vraagt om tekst als niet opgegeven)
  output_file           Output bestand (optioneel - wordt auto-gegenereerd met timestamp)
  
  -h, --help           Toon help bericht
  -r, --reverse        Keer anonimisatie proces om (de-anonimiseren)
  -f, --replacement-file  Replacement bestand voor de-anonimisatie (vereist met -r)
  -i, --identifiers-file  Bestand met identifiers (default: identifiers.txt)
  -d, --replacements-dir  Directory voor replacement bestanden (default: replacements/)
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
=======
Simple python script to remove identifiable information from a text file and afterwards reverse the proces.
I wrote this to be used with AI / LLM, so it doesn't store information i don't want it to store.

For example:

```bash
# Let's work with a sample text:
echo "John works at Tech. JOHN is a manager. john is awesome." > sample.txt

# Anonymize
python pseudonymization.py sample.txt anonymized.txt --words "John" "Tech"

# Show anonymized content
cat anonymized.txt
# This will output: "X01 works at X02. X03 is a manager. X04 is awesome."

# Reverse anonymization
python pseudonymization.py anonymized.txt restored.txt --reverse

# Show restored content
cat restored.txt
# "John works at Tech. JOHN is a manager. john is awesome."
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
>>>>>>> 8592fab285bbc5b9241d7b7dcfe9926604811ef8
  }
}
```

<<<<<<< HEAD
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

**⚠️ Belangrijk**: Dit tool is bedoeld voor basis tekstpseudonymisatie. Voor medische, juridische of andere gevoelige data, controleer altijd de output en volg relevante privacy regelgeving.
=======
The script ensures that:
- Each unique case of a word gets its own code
- The original case is perfectly preserved during de-pseudonimization
- Multiple variations of the same word (with different cases) are treated distinctly
- Basically the file replacements.json is de pseudonimization key
>>>>>>> 8592fab285bbc5b9241d7b7dcfe9926604811ef8
