#!/bin/bash
# Sample Elasticsearch queries for Ramayana dataset

ES_URL="http://localhost:9200"
INDEX="ramayana"

echo "=== RAMAYANA ELASTICSEARCH SAMPLE QUERIES ==="
echo ""

# 1. Count total shlokas
echo "1. Total number of shlokas:"
curl -s "$ES_URL/$INDEX/_count" | jq '.count'
echo ""

# 2. Search by shloka text
echo "2. Search for shlokas mentioning 'Ram' in text:"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 3,
    "query": {
      "match": {
        "shloka_text": {
          "query": "राम",
          "operator": "or"
        }
      }
    }
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, shloka_text}'
echo ""

# 3. Filter by Kanda
echo "3. All shlokas from 'Bala Kanda' (first 5):"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "term": {"kanda": "Bala Kanda"}
    }
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, explanation}'
echo ""

# 4. Full-text search in translation
echo "4. Search for 'Rama' in translation:"
curl -s -X GET "$ES_URL/$INDEX/_search" \
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
echo ""

# 5. Get specific sarga from a Kanda
echo "5. Shlokas from Bala Kanda, Sarga 1 (first 3):"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 3,
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
echo ""

# 6. Distribution of shlokas by Kanda
echo "6. Number of shlokas in each Kanda:"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "aggs": {
      "kandas": {
        "terms": {"field": "kanda", "size": 20}
      }
    }
  }' | jq '.aggregations.kandas.buckets[] | {kanda: .key, shloka_count: .doc_count}'
echo ""

# 7. Shlokas with transliteration
echo "7. Shlokas with transliteration available (first 3):"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 3,
    "query": {
      "exists": {"field": "transliteration"}
    }
  }' | jq '.hits.hits[] | {kanda, shloka, transliteration}'
echo ""

# 8. Shlokas with comments (first 3)
echo "8. Shlokas with commentary (first 3):"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 3,
    "query": {
      "exists": {"field": "comments"}
    }
  }' | jq '.hits.hits[] | {kanda, shloka, comments}'
echo ""

# 9. Average shloka number by Kanda
echo "9. Average shloka number per Kanda:"
curl -s -X GET "$ES_URL/$INDEX/_search" \
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
  }' | jq '.aggregations.kandas.buckets[] | {kanda: .key, avg_shloka_count: .avg_shloka.value | round}'
echo ""

# 10. Search shlokas mentioning virtues
echo "10. Search for 'dharma' (righteousness):"
curl -s -X GET "$ES_URL/$INDEX/_search" \
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
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, translation: .translation[:100]}'
echo ""

# 11. Complex query - specific Kanda and Sarga with text search
echo "11. Shlokas from Ayodhya Kanda, any sarga, mentioning 'Dasaratha':"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "bool": {
        "must": [
          {"term": {"kanda": "Ayodhya Kanda"}},
          {
            "multi_match": {
              "query": "Dasaratha",
              "fields": ["shloka_text", "translation", "explanation"]
            }
          }
        ]
      }
    }
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, explanation: .explanation[:100]}'
echo ""

# 12. Get shlokas by shloka number range
echo "12. Shlokas 100-110 from Ayodhya Kanda:"
curl -s -X GET "$ES_URL/$INDEX/_search" \
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
  }' | jq '.hits.hits[] | {kanda, sarga, shloka, translation: .translation[:80]}'
