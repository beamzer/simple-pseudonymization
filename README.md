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
  }
}
```

The script ensures that:
- Each unique case of a word gets its own code
- The original case is perfectly preserved during de-pseudonimization
- Multiple variations of the same word (with different cases) are treated distinctly
- Basically the file replacements.json is de pseudonimization key
