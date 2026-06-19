# CSV to Elasticsearch Converter

A comprehensive guide to converting CSV and JSON datasets to Elasticsearch-compatible formats and querying them efficiently.

**GitHub:** https://github.com/geddamsatish/restuarnts-es

## 📊 Datasets Included

This project includes two complete datasets with setup and query examples:

### 🍽️ [Bengaluru Restaurants](restaurants/README.md)
Kaggle dataset with 9,291 restaurants featuring location-based search, cuisine filtering, and geo-distance queries.

- **Documents:** 9,291 restaurants
- **Index Size:** 4 MB
- **Features:** Geo-location, ratings, reviews, cuisines, features
- **Source:** [Kaggle Restaurants Dataset](https://www.kaggle.com/datasets/mrmars1010/restaurants-dataset-bengaluru/data)
- **📘 [Full Documentation](restaurants/README.md)**

### 📖 [Ramayana Shlokas](ramayana/README.md)
Ancient Hindu scripture with 23,402 verses including Sanskrit text, transliteration, translations, and scholarly explanations.

- **Documents:** 23,402 shlokas (verses)
- **Index Size:** 20.1 MB
- **Features:** Full-text search, Kanda/Sarga navigation, Sanskrit/Roman script
- **📘 [Full Documentation](ramayana/README.md)**

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Dataset Documentation](#dataset-documentation)
- [Setup & Installation](#setup--installation)

## ✨ Features

- ✅ **CSV to JSON/NDJSON conversion** with UTF-8 BOM handling
- ✅ **Elasticsearch bulk format generation** ready for indexing
- ✅ **Proper data type mappings** (text, keyword, geo_point, integer, float)
- ✅ **Nested objects & array fields** support
- ✅ **Comprehensive sample queries** for both datasets
- ✅ **Geo-distance searching** for location-based queries
- ✅ **Full-text search** with fuzzy matching
- ✅ **Aggregations & analytics** for data insights
- ✅ **Two complete real-world datasets** included
- ✅ **Production-ready schema mappings**

## 📋 Prerequisites

- **Python** 3.7+
- **Elasticsearch** 7.0+ (or 8.0+)
- **curl** (for testing queries)
- **jq** (optional, for pretty-printing JSON)

### Quick Installation (macOS)

```bash
# Install Elasticsearch
brew install elasticsearch
brew services start elasticsearch

# Verify
curl http://localhost:9200
```

## 📁 Project Structure

```
restaurants-es/
├── README.md                      # This file (main overview)
├── SETUP.md                       # Detailed setup instructions
├── requirements.txt               # Python dependencies
├── .gitignore
│
├── restaurants/                   # 🍽️ Restaurants Dataset
│   ├── README.md                 # Restaurant docs & sample queries
│   ├── restaurants_converter.py  # CSV → JSON converter
│   ├── schema.json               # Elasticsearch mapping
│   ├── sample_queries.sh         # 10+ sample cURL queries
│   └── example_data.json        # Sample document
│
├── ramayana/                      # 📖 Ramayana Dataset
│   ├── README.md                 # Ramayana docs & sample queries
│   ├── ramayana_converter.py     # JSON → Bulk format converter
│   ├── schema.json               # Elasticsearch mapping
│   ├── sample_queries.sh         # 12+ sample cURL queries
│   └── example_data.json        # Sample document
│
└── data/                          # Data files (included)
    ├── Bengaluru_Restaurants.csv
    └── ramayana.json
```

---

## Restaurants Dataset

### Restaurants Schema

The Elasticsearch mapping for restaurants:

```json
{
  "name": "text (with keyword subfield)",
  "address": "text",
  "localAddress": "keyword",
  "addressObj": {
    "country": "keyword",
    "postalcode": "keyword",
    "state": "keyword"
  },
  "cuisine": ["keyword"],
  "description": "text",
  "dietaryRestrictions": ["keyword"],
  "dishes": ["keyword"],
  "features": ["keyword"],
  "location": "geo_point (lat/lon)",
  "mealType": ["keyword"],
  "numberOfReviews": "integer",
  "phone": "keyword",
  "rating": "float (0-5)",
  "rankingInfo": {
    "denominator": "integer",
    "position": "integer"
  },
  "rawRanking": "float"
}
```

**Index Statistics:**
- Total Documents: 9,291
- Index Size: 4 MB
- Total Restaurants: 9,291

### Restaurants Conversion

Convert CSV to JSON:

```bash
cd restaurants

# Convert to standard JSON (array format)
python restaurants_converter.py ../data/Bengaluru_Restaurants.csv restaurants.json

# Convert to NDJSON (newline-delimited JSON)
python restaurants_converter.py ../data/Bengaluru_Restaurants.csv restaurants.ndjson --ndjson
```

### Restaurants Sample Queries

Run the sample queries:

```bash
cd restaurants
bash sample_queries.sh
```

#### 1. **Search by Restaurant Name**

```bash
curl -s -X GET "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "match": {
        "name": {
          "query": "pizza",
          "fuzziness": "AUTO"
        }
      }
    }
  }' | jq '.hits.hits[] | {name, rating, cuisine}'
```

#### 2. **Filter by Cuisine with Rating**

```bash
curl -s -X GET "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 10,
    "query": {
      "bool": {
        "must": [{"term": {"cuisine": "Italian"}}],
        "filter": [{"range": {"rating": {"gte": 4.0}}}]
      }
    },
    "sort": [{"rating": {"order": "desc"}}]
  }' | jq '.hits.hits[] | {name, cuisine, rating}'
```

#### 3. **Geo-Distance Search (Nearby Restaurants)**

Find restaurants within 5km of coordinates (12.97°N, 77.59°E):

```bash
curl -s -X GET "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 10,
    "query": {
      "geo_distance": {
        "distance": "5km",
        "location": {"lat": 12.97, "lon": 77.59}
      }
    },
    "sort": [
      {
        "_geo_distance": {
          "location": {"lat": 12.97, "lon": 77.59},
          "order": "asc",
          "unit": "km"
        }
      }
    ]
  }' | jq '.hits.hits[] | {name, distance_km: .sort[0], rating}'
```

#### 4. **Filter by Features**

Find restaurants with Parking and WiFi:

```bash
curl -s -X GET "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 10,
    "query": {
      "bool": {
        "must": [
          {"terms": {"features": ["Parking"]}},
          {"terms": {"features": ["Wifi"]}}
        ]
      }
    }
  }' | jq '.hits.hits[] | {name, features}'
```

#### 5. **Top Rated Restaurants**

```bash
curl -s -X GET "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 10,
    "query": {
      "range": {"numberOfReviews": {"gte": 100}}
    },
    "sort": [
      {"rating": {"order": "desc"}},
      {"numberOfReviews": {"order": "desc"}}
    ]
  }' | jq '.hits.hits[] | {name, rating, numberOfReviews}'
```

#### 6. **Cuisine Distribution (Aggregation)**

```bash
curl -s -X GET "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "aggs": {
      "top_cuisines": {
        "terms": {"field": "cuisine", "size": 20}
      }
    }
  }' | jq '.aggregations.top_cuisines.buckets[] | {cuisine: .key, count: .doc_count}'
```

#### 7. **Average Rating by State**

```bash
curl -s -X GET "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "aggs": {
      "by_state": {
        "terms": {"field": "addressObj.state", "size": 10},
        "aggs": {
          "avg_rating": {"avg": {"field": "rating"}}
        }
      }
    }
  }' | jq '.aggregations.by_state.buckets[]'
```

#### 8. **Complex Query: Italian Restaurants Near Location with High Rating**

```bash
curl -s -X GET "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 10,
    "query": {
      "bool": {
        "must": [
          {"term": {"cuisine": "Italian"}},
          {"geo_distance": {
            "distance": "10km",
            "location": {"lat": 12.97, "lon": 77.59}
          }}
        ],
        "filter": [{"range": {"rating": {"gte": 4.0}}}]
      }
    },
    "sort": [
      {"rating": {"order": "desc"}},
      {"_geo_distance": {
        "location": {"lat": 12.97, "lon": 77.59},
        "order": "asc",
        "unit": "km"
      }}
    ]
  }' | jq '.hits.hits[] | {name, rating, distance_km: .sort[1]}'
```

---

## Ramayana Dataset

### Ramayana Schema

The Elasticsearch mapping for Ramayana shlokas:

```json
{
  "kanda": "keyword (book/section)",
  "sarga": "integer (chapter)",
  "shloka": "integer (verse number)",
  "shloka_text": "text (Sanskrit verse)",
  "transliteration": "text (Transliterated Sanskrit)",
  "translation": "text (English/Hindi translation)",
  "explanation": "text (Detailed explanation)",
  "comments": "text (Scholarly comments)"
}
```

**Index Statistics:**
- Total Documents: 23,402
- Index Size: 20.1 MB
- Total Shlokas: 23,402

### Ramayana Conversion

Convert CSV to JSON:

```bash
cd ramayana

# Convert to standard JSON
python ramayana_converter.py ../data/ramayana.csv ramayana.json

# Convert to NDJSON
python ramayana_converter.py ../data/ramayana.csv ramayana.ndjson --ndjson
```

### Ramayana Sample Queries

Run the sample queries:

```bash
cd ramayana
bash sample_queries.sh
```

#### 1. **Search Shlokas by Text**

Search for shlokas mentioning "राम" (Ram):

```bash
curl -s -X GET "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "match": {
        "shloka_text": "राम"
      }
    }
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, shloka_text}'
```

#### 2. **Filter by Kanda (Book)**

Get all shlokas from Bala Kanda (Book of Childhood):

```bash
curl -s -X GET "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 10,
    "query": {
      "term": {"kanda": "Bala Kanda"}
    }
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, explanation}'
```

#### 3. **Full-Text Search in Translations**

Search for "Rama" in translations and explanations:

```bash
curl -s -X GET "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "multi_match": {
        "query": "Rama",
        "fields": ["translation", "explanation", "shloka_text"],
        "type": "best_fields"
      }
    }
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, translation}'
```

#### 4. **Specific Kanda and Sarga**

Get shlokas from Bala Kanda, Sarga 1:

```bash
curl -s -X GET "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "bool": {
        "must": [
          {"term": {"kanda": "Bala Kanda"}},
          {"term": {"sarga": 1}}
        ]
      }
    },
    "sort": [{"shloka": {"order": "asc"}}]
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, explanation}'
```

#### 5. **Distribution by Kanda**

Count shlokas in each Kanda:

```bash
curl -s -X GET "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "aggs": {
      "kandas": {
        "terms": {"field": "kanda", "size": 20}
      }
    }
  }' | jq '.aggregations.kandas.buckets[] | {kanda: .key, count: .doc_count}'
```

#### 6. **Shlokas with Transliteration**

Find shlokas with transliteration available:

```bash
curl -s -X GET "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "exists": {"field": "transliteration"}
    }
  }' | jq '.hits.hits[] | {kanda, shloka, transliteration}'
```

#### 7. **Shlokas with Commentary**

Find annotated shlokas with comments:

```bash
curl -s -X GET "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "exists": {"field": "comments"}
    }
  }' | jq '.hits.hits[] | {kanda, shloka, comments}'
```

#### 8. **Shloka Range Search**

Get shlokas 100-110 from a specific Kanda:

```bash
curl -s -X GET "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 10,
    "query": {
      "bool": {
        "must": [
          {"term": {"kanda": "Ayodhya Kanda"}},
          {"range": {"shloka": {"gte": 100, "lte": 110}}}
        ]
      }
    },
    "sort": [{"shloka": {"order": "asc"}}]
  }' | jq '.hits.hits[] | {kanda, shloka, translation}'
```

#### 9. **Search for Virtues (Dharma)**

```bash
curl -s -X GET "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "match": {
        "translation": {
          "query": "dharma righteousness",
          "operator": "or"
        }
      }
    }
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, translation}'
```

#### 10. **Average Shlokas per Kanda**

```bash
curl -s -X GET "http://localhost:9200/ramayana/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "aggs": {
      "kandas": {
        "terms": {"field": "kanda", "size": 20},
        "aggs": {
          "avg_shloka": {"avg": {"field": "shloka"}}
        }
      }
    }
  }' | jq '.aggregations.kandas.buckets[]'
```

---

## Elasticsearch Bulk Indexing

### 1. Create Index with Schema

**For Restaurants:**
```bash
curl -X PUT "localhost:9200/restaurants" \
  -H "Content-Type: application/json" \
  -d @restaurants/schema.json
```

**For Ramayana:**
```bash
curl -X PUT "localhost:9200/ramayana" \
  -H "Content-Type: application/json" \
  -d @ramayana/schema.json
```

### 2. Generate NDJSON with Bulk Format

```bash
# For restaurants
cd restaurants
python restaurants_converter.py data.csv output.ndjson --ndjson

# For ramayana
cd ramayana
python ramayana_converter.py data.csv output.ndjson --ndjson
```

### 3. Add Bulk Metadata

Create a script to add Elasticsearch bulk API metadata:

```bash
#!/bin/bash
INPUT=$1
OUTPUT=$2
INDEX=${3:-"documents"}

while IFS= read -r line; do
  echo "{\"index\": {\"_index\": \"$INDEX\"}}"
  echo "$line"
done < "$INPUT" > "$OUTPUT"
```

### 4. Index to Elasticsearch

```bash
curl -X POST "localhost:9200/_bulk" \
  -H "Content-Type: application/json" \
  --data-binary @output_bulk.ndjson
```

### 5. Verify Indexing

```bash
# Count documents
curl -s "localhost:9200/restaurants/_count" | jq '.count'
curl -s "localhost:9200/ramayana/_count" | jq '.count'

# Get index stats
curl -s "localhost:9200/_stats" | jq '.indices'
```

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/geddamsatish/restuarnts-es.git
cd restuarnts-es
```

### 2. Prepare Data

Download CSV files from:
- **Restaurants**: [Kaggle Bengaluru Restaurants Dataset](https://www.kaggle.com/himanshuvaidya121/bengaluru-restaurants-more-on-theft)
- **Ramayana**: Add your ramayana CSV file to `data/` directory

### 3. Convert CSV to JSON

```bash
# Restaurants
python restaurants/restaurants_converter.py data/Bengaluru_Restaurants.csv restaurants.ndjson --ndjson

# Ramayana
python ramayana/ramayana_converter.py data/ramayana.csv ramayana.ndjson --ndjson
```

### 4. Create Indices in Elasticsearch

```bash
# Start Elasticsearch
brew services start elasticsearch

# Create indices with schema
curl -X PUT "localhost:9200/restaurants" -H "Content-Type: application/json" -d @restaurants/schema.json
curl -X PUT "localhost:9200/ramayana" -H "Content-Type: application/json" -d @ramayana/schema.json
```

### 5. Index Data

```bash
# Create bulk format files
for file in *.ndjson; do
  {
    while IFS= read -r line; do
      echo '{"index": {"_index": "'${file%.ndjson}'"}}'
      echo "$line"
    done < "$file"
  } > "${file%.ndjson}_bulk.ndjson"
done

# Index to Elasticsearch
curl -X POST "localhost:9200/_bulk" \
  -H "Content-Type: application/json" \
  --data-binary @restaurants_bulk.ndjson

curl -X POST "localhost:9200/_bulk" \
  -H "Content-Type: application/json" \
  --data-binary @ramayana_bulk.ndjson
```

### 6. Run Sample Queries

```bash
# Restaurants queries
bash restaurants/sample_queries.sh

# Ramayana queries
bash ramayana/sample_queries.sh
```

---

## Useful Resources

- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
- [Geo Queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-queries.html)
- [Aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html)
- [Kaggle - Bengaluru Restaurants](https://www.kaggle.com/himanshuvaidya121/bengaluru-restaurants-more-on-theft)

---

## License

MIT License

## Author

Satish Geddams
