# Ramayana Shlokas Dataset

Elasticsearch integration for the Ramayana Sanskrit verses with translations and explanations.

**Content:** Ancient Hindu scripture with 23,402 shlokas (verses)

## Quick Stats

- **Total Shlokas:** 23,402
- **Index Size:** 20.1 MB
- **Books (Kandas):** 7
- **Key Fields:** Sanskrit text, Transliteration, Translation, Explanation
- **Document Count:** 23,402

## Table of Contents

- [Schema](#schema)
- [Conversion](#conversion)
- [Queries](#queries)
- [Kandas (Books)](#kandas-books)
- [Common Use Cases](#common-use-cases)

---

## Schema

```json
{
  "kanda": "keyword (book/section)",
  "sarga": "integer (chapter)",
  "shloka": "integer (verse number)",
  "shloka_text": "text (Sanskrit verse)",
  "transliteration": "text (Roman script)",
  "translation": "text (English/Hindi)",
  "explanation": "text (Detailed meaning)",
  "comments": "text (Scholarly notes)"
}
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `kanda` | keyword | Book name (7 kandas in Ramayana) |
| `sarga` | integer | Chapter number within a kanda |
| `shloka` | integer | Verse number |
| `shloka_text` | text | Original Sanskrit verse (Devanagari) |
| `transliteration` | text | Sanskrit in Roman/IAST script |
| `translation` | text | English or Hindi translation |
| `explanation` | text | Word-by-word meaning and explanation |
| `comments` | text | Scholarly commentary and notes |

---

## Conversion

### Convert CSV to JSON

```bash
python ramayana_converter.py ../ramayana.csv ramayana.json
```

### Convert to NDJSON (for bulk indexing)

```bash
python ramayana_converter.py ../ramayana.csv ramayana.ndjson --ndjson
```

### Script Features

- Handles UTF-8 BOM encoding
- Converts integers for sarga and shloka numbers
- Preserves Sanskrit (Devanagari) text properly
- Generates properly formatted NDJSON

---

## Queries

### 1. Search by Sanskrit Text

```bash
curl -s "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "match": {
        "shloka_text": "राम"
      }
    },
    "size": 10
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, shloka_text}'
```

**Use case:** Find verses mentioning specific concepts (e.g., "Rama", "Sita")

---

### 2. Filter by Kanda (Book)

Get all shlokas from Bala Kanda (Book of Childhood):

```bash
curl -s "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "term": {"kanda": "Bala Kanda"}
    },
    "size": 20,
    "sort": [{"shloka": {"order": "asc"}}]
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, explanation}'
```

**Use case:** Study specific book of the Ramayana

---

### 3. Full-Text Search in Translations

```bash
curl -s "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "multi_match": {
        "query": "Rama virtues righteousness",
        "fields": ["translation", "explanation", "shloka_text"],
        "type": "best_fields"
      }
    },
    "size": 10
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, translation}'
```

**Use case:** Find verses about specific themes (virtue, duty, love, etc.)

---

### 4. Specific Kanda and Sarga

```bash
curl -s "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "bool": {
        "must": [
          {"term": {"kanda": "Bala Kanda"}},
          {"term": {"sarga": 1}}
        ]
      }
    },
    "sort": [{"shloka": {"order": "asc"}}],
    "size": 50
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, explanation}'
```

**Use case:** Study a specific chapter

---

### 5. Kanda Distribution

```bash
curl -s "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "aggs": {
      "kandas": {
        "terms": {
          "field": "kanda",
          "size": 20
        }
      }
    }
  }' | jq '.aggregations.kandas.buckets[] | {kanda: .key, shloka_count: .doc_count}'
```

**Use case:** Understand structure of the Ramayana

---

### 6. Shlokas with Transliteration

Find verses with transliteration (Roman script) available:

```bash
curl -s "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "exists": {"field": "transliteration"}
    },
    "size": 20
  }' | jq '.hits.hits[] | {kanda, shloka, transliteration}'
```

**Use case:** Learn Sanskrit pronunciation

---

### 7. Shlokas with Commentary

Find verses with scholarly commentary:

```bash
curl -s "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "exists": {"field": "comments"}
    },
    "size": 20
  }' | jq '.hits.hits[] | {kanda, shloka, comments}'
```

**Use case:** Deep scholarly study

---

### 8. Shloka Range Search

Get verses 100-110 from a specific kanda:

```bash
curl -s "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "bool": {
        "must": [
          {"term": {"kanda": "Ayodhya Kanda"}},
          {"range": {"shloka": {"gte": 100, "lte": 110}}}
        ]
      }
    },
    "sort": [{"shloka": {"order": "asc"}}],
    "size": 20
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, translation}'
```

**Use case:** Study specific verse sequences

---

### 9. Search for Virtues (Dharma)

```bash
curl -s "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "bool": {
        "should": [
          {"match": {"translation": "dharma"}},
          {"match": {"translation": "righteousness"}},
          {"match": {"explanation": "duty"}}
        ]
      }
    },
    "size": 20
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, translation}'
```

**Use case:** Explore philosophical themes

---

### 10. Average Shlokas per Kanda

```bash
curl -s "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "aggs": {
      "kandas": {
        "terms": {"field": "kanda", "size": 20},
        "aggs": {
          "avg_shloka_num": {"avg": {"field": "shloka"}}
        }
      }
    }
  }' | jq '.aggregations.kandas.buckets[] | {kanda: .key, avg_shloka: (.avg_shloka_num.value | floor)}'
```

**Use case:** Understand verse numbering structure

---

## Kandas (Books)

The Ramayana is divided into 7 main books:

1. **Bala Kanda** - Book of Childhood
2. **Ayodhya Kanda** - Book of Ayodhya
3. **Aranya Kanda** - Book of the Forest
4. **Kishkindha Kanda** - Book of Kishkindha
5. **Sundar Kanda** - Book of Beauty
6. **Yuddha Kanda** - Book of War
7. **Uttara Kanda** - Book of Conclusion

### Example: Study Sundar Kanda

```bash
curl -s "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {"term": {"kanda": "Sundar Kanda"}},
    "size": 50
  }' | jq '.hits.hits[] | {sarga, shloka, translation}' | head -20
```

---

## Common Use Cases

### 1. Sanskrit Learning App

- Search Sanskrit text
- Show transliteration (pronunciation)
- Provide translation
- Display explanation

### 2. Spiritual Study Platform

- Browse by Kanda/Sarga
- Full-text search for themes
- Compare translations
- Show scholarly commentary

### 3. Research Tool

- Find verses about specific topics
- Analyze verse frequency
- Study narrative progression
- Compare multiple translations

### 4. Educational Content

- Create study guides per Kanda
- Generate vocab lists
- Highlight important verses
- Provide cultural context

---

## Setup

### Create Index

```bash
curl -X PUT "localhost:9200/ramayana" \
  -H "Content-Type: application/json" \
  -d @schema.json
```

### Index Data

```bash
# Create bulk format
python ramayana_converter.py ../ramayana.json output.ndjson --ndjson

# Add metadata
while IFS= read -r line; do
  echo '{"index": {"_index": "ramayana"}}'
  echo "$line"
done < output.ndjson > output_bulk.ndjson

# Index to Elasticsearch
curl -X POST "localhost:9200/_bulk" \
  -H "Content-Type: application/json" \
  --data-binary @output_bulk.ndjson
```

### Verify

```bash
curl -s http://localhost:9200/ramayana/_count | jq '.count'
# Should return: 23402
```

---

## Data Format Example

```json
{
  "kanda": "Bala Kanda",
  "sarga": 1,
  "shloka": 1,
  "shloka_text": "तपस्स्वाध्यायनिरतं तपस्वी वाग्विदां वरम् ।",
  "transliteration": "tapassvādhyāyanirataṁ tapasvī vāgvidāṁ varam।",
  "translation": "Ascetic Valmiki enquired of Narada...",
  "explanation": "Valmiki was deeply engaged in...",
  "comments": "Saint Narada visits hermitage of Valmiki..."
}
```

---

## Performance Tips

1. **Use `keyword` for exact kanda matches**
2. **Sort by `shloka` for sequential reading**
3. **Use range queries for verse numbers**
4. **Full-text search for theme exploration**
5. **Implement pagination for large result sets**

---

## Encoding Notes

- ✅ Supports Devanagari (Sanskrit script)
- ✅ Preserves diacritics in transliteration
- ✅ Maintains Unicode characters
- ✅ Use `utf-8` encoding when processing

### Example: Search with Devanagari

```bash
# Search for "dharma" in Sanskrit
curl -s "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "match": {
        "shloka_text": "धर्म"
      }
    }
  }'
```

---

## Troubleshooting

### Devanagari Text Not Displaying

Ensure your terminal/browser supports UTF-8:
```bash
# Verify UTF-8 support
locale
# Should show UTF-8
```

### No Results for Transliteration

Check if transliteration field is populated:
```bash
curl -s "http://localhost:9200/ramayana/_search" \
  -d '{"query": {"exists": {"field": "transliteration"}}}' | \
  jq '.hits.total.value'
```

---

## References

- Ramayana - Ancient Sanskrit Epic
- Traditional Hindu Scripture
- Multiple English translations available

---

## See Also

- [Main README](../README.md) - Project overview
- [Restaurants Dataset](../restaurants/README.md) - Complementary dataset
- [Setup Guide](../SETUP.md) - Installation instructions
