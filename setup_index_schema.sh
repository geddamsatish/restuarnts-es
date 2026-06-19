#!/bin/bash

# Create index with proper mapping for Bengaluru Restaurants

echo "Creating 'restaurants' index with schema..."

curl -X DELETE "localhost:9200/restaurants" 2>/dev/null

curl -X PUT "localhost:9200/restaurants" \
  -H "Content-Type: application/json" \
  -d '{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "analysis": {
      "analyzer": {
        "default": {
          "type": "standard"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword"
          }
        }
      },
      "address": {
        "type": "text"
      },
      "localAddress": {
        "type": "keyword"
      },
      "addressObj": {
        "type": "object",
        "properties": {
          "country": {
            "type": "keyword"
          },
          "postalcode": {
            "type": "keyword"
          },
          "state": {
            "type": "keyword"
          }
        }
      },
      "cuisine": {
        "type": "keyword"
      },
      "description": {
        "type": "text"
      },
      "dietaryRestrictions": {
        "type": "keyword"
      },
      "dishes": {
        "type": "keyword"
      },
      "features": {
        "type": "keyword"
      },
      "location": {
        "type": "geo_point"
      },
      "mealType": {
        "type": "keyword"
      },
      "numberOfReviews": {
        "type": "integer"
      },
      "phone": {
        "type": "keyword"
      },
      "rankingInfo": {
        "type": "object",
        "properties": {
          "denominator": {
            "type": "integer"
          },
          "position": {
            "type": "integer"
          }
        }
      },
      "rating": {
        "type": "float"
      },
      "rawRanking": {
        "type": "float"
      }
    }
  }
}'

echo ""
echo "Index schema created successfully!"
echo ""
echo "Now indexing documents..."

curl -X POST "localhost:9200/_bulk" \
  -H "Content-Type: application/json" \
  --data-binary @Bengaluru_Restaurants_bulk_indexed.ndjson 2>/dev/null > /tmp/bulk_result.json

# Parse results
TOOK=$(jq '.took' /tmp/bulk_result.json)
ERRORS=$(jq '.errors' /tmp/bulk_result.json)
TOTAL=$(jq '.items | length' /tmp/bulk_result.json)

echo "Indexing complete!"
echo "  Time taken: ${TOOK}ms"
echo "  Errors: ${ERRORS}"
echo "  Documents indexed: ${TOTAL}"

echo ""
echo "Verifying index..."
curl -s "localhost:9200/restaurants/_count" | jq '{index: "restaurants", doc_count: .count}'
