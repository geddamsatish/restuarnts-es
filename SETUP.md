# Setup Guide

Complete setup instructions for the Restaurants & Ramayana Elasticsearch Project.

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/geddamsatish/restuarnts-es.git
cd restuarnts-es
```

### 2. Install Elasticsearch

We provide detailed guides for different installation methods:

#### 🍺 Using Homebrew (Recommended for Beginners)
```bash
brew tap elastic/tap
brew install elastic/tap/elasticsearch-full
brew services start elastic/tap/elasticsearch-full
curl http://localhost:9200
```
👉 **[Complete Homebrew Guide](INSTALL_ELASTICSEARCH_BREW.md)**

#### 📥 Direct Installation (Recommended for Control)
```bash
mkdir -p ~/elasticsearch && cd ~/elasticsearch
curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.0-darwin-aarch64.tar.gz
tar -xzf elasticsearch-8.10.0-darwin-aarch64.tar.gz
cd elasticsearch-8.10.0
./bin/elasticsearch
```
👉 **[Complete Direct Installation Guide](INSTALL_ELASTICSEARCH_DIRECT.md)**

#### 📋 Choose Your Method
👉 **[Installation Method Comparison & Decision Guide](INSTALL_ELASTICSEARCH.md)**

#### Docker (Alternative)
```bash
docker run -d --name elasticsearch \
  -e discovery.type=single-node \
  -p 9200:9200 \
  -p 9300:9300 \
  docker.elastic.co/elasticsearch/elasticsearch:8.10.0
```

#### Linux (Ubuntu/Debian)
```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
sudo apt-get install -y elasticsearch
sudo systemctl start elasticsearch
```

### 3. Install Python Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 4. Verify Elasticsearch Connection

```bash
# Test Elasticsearch connection
curl -X GET http://localhost:9200

# Should return something like:
# {
#   "name" : "your-machine",
#   "cluster_name" : "elasticsearch",
#   "version" : { "number" : "8.0.0", ... },
#   ...
# }
```

---

## Data Setup

### Dataset Files

The repository includes two datasets:

1. **Bengaluru_Restaurants.csv** (3.2 MB)
   - 9,291 restaurants
   - Location, cuisine, ratings, reviews

2. **ramayana.json** (24 MB)
   - 23,402 shlokas (verses)
   - Sanskrit text, translations, explanations

---

## Create Indices

### Option 1: Create with Schema Mapping

```bash
# Create Restaurants index
curl -X PUT "localhost:9200/restaurants" \
  -H "Content-Type: application/json" \
  -d @restaurants/schema.json

# Create Ramayana index
curl -X PUT "localhost:9200/ramayana" \
  -H "Content-Type: application/json" \
  -d @ramayana/schema.json
```

### Option 2: Auto-create on First Index

Elasticsearch can auto-create indices, but using explicit schemas is recommended for:
- Proper type mappings
- Geo-point field configuration
- Optimized analyzer settings
- Better search performance

---

## Convert and Index Data

### Step 1: Generate NDJSON Files

```bash
# Convert Restaurants CSV to NDJSON
cd restaurants
python restaurants_converter.py ../Bengaluru_Restaurants.csv restaurants.ndjson --ndjson
cd ..

# Convert Ramayana JSON (if CSV available)
cd ramayana
python ramayana_converter.py ../ramayana_data.csv ramayana.ndjson --ndjson
cd ..
```

### Step 2: Create Bulk Format

```bash
# Create a helper script
cat > create_bulk.sh << 'EOF'
#!/bin/bash
INPUT=$1
OUTPUT=$2
INDEX=${3:-"documents"}

while IFS= read -r line; do
  echo "{\"index\": {\"_index\": \"$INDEX\"}}"
  echo "$line"
done < "$INPUT" > "$OUTPUT"
EOF

chmod +x create_bulk.sh

# Generate bulk format files
./create_bulk.sh restaurants.ndjson restaurants_bulk.ndjson restaurants
./create_bulk.sh ramayana.ndjson ramayana_bulk.ndjson ramayana
```

### Step 3: Index to Elasticsearch

```bash
# Index Restaurants
curl -X POST "localhost:9200/_bulk" \
  -H "Content-Type: application/json" \
  --data-binary @restaurants_bulk.ndjson

# Index Ramayana
curl -X POST "localhost:9200/_bulk" \
  -H "Content-Type: application/json" \
  --data-binary @ramayana_bulk.ndjson
```

### Step 4: Verify Indexing

```bash
# Check document counts
curl -s http://localhost:9200/restaurants/_count | jq '.count'
curl -s http://localhost:9200/ramayana/_count | jq '.count'

# Should show: 9291 and 23402 respectively
```

---

## Quick Test

Run sample queries to verify everything works:

```bash
# Test Restaurants queries
bash restaurants/sample_queries.sh

# Test Ramayana queries
bash ramayana/sample_queries.sh
```

---

## Troubleshooting

### Elasticsearch Connection Issues

```bash
# Check if Elasticsearch is running
curl http://localhost:9200

# If port 9200 is not responding, start Elasticsearch
brew services start elasticsearch
# or
systemctl start elasticsearch
```

### CSV Parsing Errors

```bash
# Check CSV file format
file Bengaluru_Restaurants.csv

# Try different encoding
python restaurants/restaurants_converter.py Bengaluru_Restaurants.csv output.json
```

### Large File Issues

If encountering memory issues with large NDJSON files:

```bash
# Process in chunks
python -c "
import csv
import json

batch_size = 1000
batch = []

with open('Bengaluru_Restaurants.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        # Convert and add to batch
        batch.append(json.dumps(row))

        if (i + 1) % batch_size == 0:
            with open(f'batch_{i//batch_size}.ndjson', 'w') as out:
                out.write('\n'.join(batch) + '\n')
            batch = []
"
```

---

## IDE Setup

### VS Code

1. Install extensions:
   - REST Client (for testing queries)
   - Python
   - Elasticsearch for VS Code (optional)

2. Create `.vscode/settings.json`:
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "[python]": {
    "editor.formatOnSave": true
  }
}
```

### PyCharm

1. Configure Python interpreter:
   - Settings → Project → Python Interpreter
   - Select `./venv` directory

2. Set up run configurations for scripts

---

## Environment Variables (Optional)

Create `.env` file for custom settings:

```bash
# Elasticsearch settings
ES_HOST=localhost
ES_PORT=9200
ES_INDEX_RESTAURANTS=restaurants
ES_INDEX_RAMAYANA=ramayana

# Python settings
PYTHONUNBUFFERED=1
```

---

## Next Steps

1. ✅ Elasticsearch installed and running
2. ✅ Python dependencies installed
3. ✅ Data files available
4. ✅ Indices created
5. ✅ Data indexed
6. → Run sample queries from README.md
7. → Explore advanced queries
8. → Build your own applications

See [README.md](README.md) for comprehensive query examples.
