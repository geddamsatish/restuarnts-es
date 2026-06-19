# Ramayana Shlokas Dataset

This folder contains the raw dataset files for the Ramayana project.

## Files

- **ramayana.json** (24 MB)
  - Format: JSON array with 23,402 shloka (verse) records
  - Content: Ancient Hindu scripture with Sanskrit text, transliterations, translations, and explanations
  - Structure: Each record contains detailed verse information from all 7 Kandas (books)

## Usage

### Index Directly to Elasticsearch

Since ramayana.json is already in JSON format, you can use it directly:

```bash
# From ramayana directory
python ramayana_converter.py data/ramayana.json output.ndjson --ndjson
```

### Or Use the Converter

```bash
# If you have a CSV version
python ramayana_converter.py data/ramayana.csv output.ndjson --ndjson
```

## Data Structure

Each shloka record contains:
- **kanda** (string) - Book/section name (7 total)
- **sarga** (integer) - Chapter number within kanda
- **shloka** (integer) - Verse number
- **shloka_text** (string) - Original Sanskrit verse (Devanagari script)
- **transliteration** (string) - Roman/IAST transliteration
- **translation** (string) - English/Hindi translation
- **explanation** (string) - Word-by-word meaning
- **comments** (string) - Scholarly commentary

## The 7 Kandas

1. **Bala Kanda** - Book of Childhood
2. **Ayodhya Kanda** - Book of Ayodhya
3. **Aranya Kanda** - Book of the Forest
4. **Kishkindha Kanda** - Book of Kishkindha
5. **Sundar Kanda** - Book of Beauty
6. **Yuddha Kanda** - Book of War
7. **Uttara Kanda** - Book of Conclusion

## Character Encoding

- ✅ Full UTF-8 support for Devanagari script
- ✅ Supports diacritics in transliteration
- ✅ Proper Unicode handling for all ancient scripts

## Notes

- Total shlokas: 23,402
- Multiple translations available in dataset
- Scholarly comments add educational value
- Perfect for Sanskrit learning applications
- See parent README.md for sample queries

## References

- Ramayana - Ancient Hindu scripture
- Multiple translation sources compiled
- Traditional authoritative texts

## See Also

- [ramayana/README.md](../README.md) - Complete guide with queries
- [ramayana_converter.py](../ramayana_converter.py) - Conversion script
- [schema.json](../schema.json) - Elasticsearch mapping
