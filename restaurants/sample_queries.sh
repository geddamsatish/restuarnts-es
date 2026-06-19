#!/bin/bash
# Sample Elasticsearch queries for Restaurants dataset

ES_URL="http://localhost:9200"
INDEX="restaurants"

echo "=== RESTAURANTS ELASTICSEARCH SAMPLE QUERIES ==="
echo ""

# 1. Count total restaurants
echo "1. Total number of restaurants:"
curl -s "$ES_URL/$INDEX/_count" | jq '.count'
echo ""

# 2. Search by restaurant name
echo "2. Search restaurants by name (pizza):"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 3,
    "query": {
      "match": {
        "name": {
          "query": "pizza",
          "fuzziness": "AUTO"
        }
      }
    }
  }' | jq '.hits.hits[] | {name, rating, cuisine}'
echo ""

# 3. Filter by cuisine
echo "3. Italian restaurants with rating >= 4.0:"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "bool": {
        "must": [{"term": {"cuisine": "Italian"}}],
        "filter": [{"range": {"rating": {"gte": 4.0}}}]
      }
    },
    "sort": [{"rating": {"order": "desc"}}]
  }' | jq '.hits.hits[] | {name, cuisine, rating, address}'
echo ""

# 4. Geo search - restaurants near coordinates
echo "4. Restaurants within 5km of (12.97, 77.59):"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
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
  }' | jq '.hits.hits[] | {name, distance: .sort[0], rating}'
echo ""

# 5. Filter by features
echo "5. Restaurants with Parking and Wifi:"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "bool": {
        "must": [
          {"terms": {"features": ["Parking"]}},
          {"terms": {"features": ["Wifi"]}}
        ]
      }
    }
  }' | jq '.hits.hits[] | {name, features, rating}'
echo ""

# 6. Top rated restaurants
echo "6. Top 10 rated restaurants (min 100 reviews):"
curl -s -X GET "$ES_URL/$INDEX/_search" \
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
echo ""

# 7. Cuisine distribution
echo "7. Top 10 cuisines by count:"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "aggs": {
      "cuisines": {
        "terms": {"field": "cuisine", "size": 10}
      }
    }
  }' | jq '.aggregations.cuisines.buckets[] | {cuisine: .key, count: .doc_count}'
echo ""

# 8. Average rating by state
echo "8. Average rating by state:"
curl -s -X GET "$ES_URL/$INDEX/_search" \
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
  }' | jq '.aggregations.by_state.buckets[] | {state: .key, avg_rating: .avg_rating.value, count: .doc_count}'
echo ""

# 9. Complex query - Italian near location with rating filter
echo "9. Italian restaurants within 10km of (12.97, 77.59) with rating >= 4.0:"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "bool": {
        "must": [
          {"term": {"cuisine": "Italian"}},
          {
            "geo_distance": {
              "distance": "10km",
              "location": {"lat": 12.97, "lon": 77.59}
            }
          }
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
  }' | jq '.hits.hits[] | {name, cuisine, rating, distance_km: .sort[1]}'
echo ""

# 10. Full-text search
echo "10. Full-text search for 'biryani':"
curl -s -X GET "$ES_URL/$INDEX/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 5,
    "query": {
      "multi_match": {
        "query": "biryani",
        "fields": ["name^2", "description", "dishes"],
        "type": "best_fields"
      }
    }
  }' | jq '.hits.hits[] | {name, rating, _score}'
