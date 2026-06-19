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

## 🚀 Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/geddamsatish/restuarnts-es.git
cd restuarnts-es

# Install dependencies
pip install -r requirements.txt

# Start Elasticsearch
brew services start elasticsearch
```

### 2. Create Indices

```bash
# Create indices with schema mappings
curl -X PUT "localhost:9200/restaurants" \
  -H "Content-Type: application/json" \
  -d @restaurants/schema.json

curl -X PUT "localhost:9200/ramayana" \
  -H "Content-Type: application/json" \
  -d @ramayana/schema.json
```

### 3. Convert & Index Data

```bash
# Convert data to bulk format
python restaurants/restaurants_converter.py Bengaluru_Restaurants.csv restaurants.ndjson --ndjson
python ramayana/ramayana_converter.py ramayana.json ramayana.ndjson --ndjson

# Add Elasticsearch bulk metadata
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

### 4. Verify & Query

```bash
# Verify indexing
curl -s "localhost:9200/restaurants/_count" | jq '.count'
curl -s "localhost:9200/ramayana/_count" | jq '.count'

# Run sample queries
bash restaurants/sample_queries.sh
bash ramayana/sample_queries.sh
```

---

## 📚 Dataset Documentation

### [🍽️ Restaurants Dataset](restaurants/README.md)

Complete guide for the Bengaluru Restaurants dataset:
- **10+ sample queries** (search, geo, filters, aggregations)
- **Data schema** with field descriptions
- **Common use cases** (discovery, recommendations, location services)
- **Setup instructions** specific to restaurants

**Quick Links:**
- [Schema](restaurants/schema.json)
- [Converter Script](restaurants/restaurants_converter.py)
- [Sample Queries](restaurants/sample_queries.sh)

### [📖 Ramayana Dataset](ramayana/README.md)

Complete guide for the Ramayana Shlokas dataset:
- **12+ sample queries** (text search, filtering, aggregations)
- **Data schema** with Sanskrit field support
- **Common use cases** (learning, research, spiritual study)
- **Kanda (book) navigation** examples

**Quick Links:**
- [Schema](ramayana/schema.json)
- [Converter Script](ramayana/ramayana_converter.py)
- [Sample Queries](ramayana/sample_queries.sh)

---

## 📖 Additional Resources

- **[SETUP.md](SETUP.md)** - Detailed setup for all operating systems
- **[Elasticsearch Docs](https://www.elastic.co/guide/index.html)** - Official documentation
- **[Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)** - Query language guide
- **[Geo Queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-queries.html)** - Location-based queries
- **[Aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html)** - Data analytics

## 🔗 Data Sources

- **Restaurants:** [Kaggle Bengaluru Restaurants Dataset](https://www.kaggle.com/datasets/mrmars1010/restaurants-dataset-bengaluru/data)
- **Ramayana:** Ancient Hindu scripture

---

## 📝 License

MIT License

## 👤 Author

Satish Geddams

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
