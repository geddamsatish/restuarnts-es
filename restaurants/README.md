# Bengaluru Restaurants Dataset

Elasticsearch integration for Kaggle's Bengaluru Restaurants dataset.

**Dataset Source:** [Kaggle - Bengaluru Restaurants](https://www.kaggle.com/datasets/mrmars1010/restaurants-dataset-bengaluru/data)

## Quick Stats

- **Total Restaurants:** 9,291
- **Index Size:** 4 MB
- **Key Fields:** Name, Location (Geo), Cuisine, Rating, Reviews
- **Document Count:** 9,291

## Table of Contents

- [Schema](#schema)
- [Conversion](#conversion)
- [Queries](#queries)
- [Common Use Cases](#common-use-cases)

---

## Schema

```json
{
  "name": "text (searchable)",
  "address": "text",
  "location": "geo_point (lat/lon)",
  "cuisine": ["keyword"],
  "rating": "float (0-5)",
  "numberOfReviews": "integer",
  "features": ["keyword"],
  "mealType": ["keyword"],
  "phone": "keyword"
}
```

**Field Descriptions:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | text | Restaurant name (searchable with fuzzy matching) |
| `address` | text | Full address |
| `location` | geo_point | Geographic coordinates for distance queries |
| `cuisine` | keyword[] | Types of cuisine (Italian, Chinese, etc.) |
| `rating` | float | Rating from 0 to 5 |
| `numberOfReviews` | integer | Total number of reviews |
| `features` | keyword[] | Features (Parking, WiFi, Reservations, etc.) |
| `mealType` | keyword[] | Available meal types (Lunch, Dinner, etc.) |
| `phone` | keyword | Contact number |
| `dietaryRestrictions` | keyword[] | Dietary options (Vegan, Vegetarian, etc.) |
| `dishes` | keyword[] | Popular dishes served |

---

## Conversion

### Convert CSV to JSON

```bash
python restaurants_converter.py ../Bengaluru_Restaurants.csv restaurants.json
```

### Convert to NDJSON (for bulk indexing)

```bash
python restaurants_converter.py ../Bengaluru_Restaurants.csv restaurants.ndjson --ndjson
```

### Script Features

- Handles UTF-8 BOM encoding
- Converts data types (latitude/longitude to float)
- Splits list fields properly
- Only includes location if both coordinates exist
- Generates properly formatted NDJSON

---

## Queries

### 1. Search by Name

```bash
curl -s "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "match": {
        "name": {
          "query": "pizza",
          "fuzziness": "AUTO"
        }
      }
    },
    "size": 10
  }' | jq '.hits.hits[] | {name, rating, cuisine}'
```

**Use case:** Find restaurants by partial name match

---

### 2. Filter by Cuisine

```bash
curl -s "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "bool": {
        "must": [
          {"term": {"cuisine": "Italian"}},
          {"range": {"rating": {"gte": 4.0}}}
        ]
      }
    },
    "sort": [{"rating": {"order": "desc"}}],
    "size": 10
  }' | jq '.hits.hits[] | {name, cuisine, rating}'
```

**Use case:** Find highly-rated restaurants of a specific cuisine

---

### 3. Nearby Restaurants (Geo Search)

Find restaurants within 5km of location (12.97°N, 77.59°E):

```bash
curl -s "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "geo_distance": {
        "distance": "5km",
        "location": {
          "lat": 12.97,
          "lon": 77.59
        }
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
    ],
    "size": 20
  }' | jq '.hits.hits[] | {name, distance_km: .sort[0], rating}'
```

**Use case:** "Find restaurants near me" functionality

---

### 4. Filter by Features

```bash
curl -s "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "bool": {
        "must": [
          {"terms": {"features": ["Parking"]}},
          {"terms": {"features": ["WiFi"]}}
        ]
      }
    },
    "size": 10
  }' | jq '.hits.hits[] | {name, features, rating}'
```

**Use case:** Find restaurants with specific amenities

---

### 5. Top Rated Restaurants

```bash
curl -s "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": {
      "range": {
        "numberOfReviews": {"gte": 100}
      }
    },
    "sort": [
      {"rating": {"order": "desc"}},
      {"numberOfReviews": {"order": "desc"}}
    ],
    "size": 20
  }' | jq '.hits.hits[] | {name, rating, numberOfReviews}'
```

**Use case:** Find highly-rated, well-reviewed restaurants

---

### 6. Cuisine Distribution

```bash
curl -s "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
    "size": 0,
    "aggs": {
      "cuisine_distribution": {
        "terms": {
          "field": "cuisine",
          "size": 30
        }
      }
    }
  }' | jq '.aggregations.cuisine_distribution.buckets[] | {cuisine: .key, count: .doc_count}'
```

**Use case:** See what cuisines are popular

---

### 7. Average Rating by State

```bash
curl -s "http://localhost:9200/restaurants/_search" \
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
```

**Use case:** Compare restaurant quality across regions

---

### 8. Complex Query: Italian Near Location with High Rating

```bash
curl -s "http://localhost:9200/restaurants/_search" \
  -H 'Content-Type: application/json' \
  -d '{
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
        "filter": [
          {"range": {"rating": {"gte": 4.0}}}
        ]
      }
    },
    "sort": [
      {"rating": {"order": "desc"}},
      {
        "_geo_distance": {
          "location": {"lat": 12.97, "lon": 77.59},
          "order": "asc",
          "unit": "km"
        }
      }
    ],
    "size": 10
  }' | jq '.hits.hits[] | {name, rating, distance_km: .sort[1]}'
```

**Use case:** Find the best Italian restaurants nearby

---

## Common Use Cases

### 1. Restaurant Discovery App

Combine:
- Name search
- Cuisine filter
- Location (geo)
- Rating filter

### 2. Recommendation System

Use aggregations to:
- Find trending cuisines
- Identify popular features
- Analyze rating distribution

### 3. Location-Based Services

Leverage `geo_point`:
- Find nearby restaurants
- Search by distance
- Implement "places nearby" features

### 4. Business Analytics

Use aggregations for:
- Cuisine popularity
- Feature availability
- Rating trends by location
- Review count analysis

---

## Setup

### Create Index

```bash
curl -X PUT "localhost:9200/restaurants" \
  -H "Content-Type: application/json" \
  -d @schema.json
```

### Index Data

```bash
# Create bulk format
python restaurants_converter.py ../Bengaluru_Restaurants.csv output.ndjson --ndjson

# Add metadata
while IFS= read -r line; do
  echo '{"index": {"_index": "restaurants"}}'
  echo "$line"
done < output.ndjson > output_bulk.ndjson

# Index to Elasticsearch
curl -X POST "localhost:9200/_bulk" \
  -H "Content-Type: application/json" \
  --data-binary @output_bulk.ndjson
```

### Verify

```bash
curl -s http://localhost:9200/restaurants/_count | jq '.count'
# Should return: 9291
```

---

## Data Format Example

```json
{
  "name": "Absolute Barbecues",
  "address": "3rd Floor, 90/4, Marathahalli Outer Ring Road...",
  "location": {
    "lat": 12.949864,
    "lon": 77.69931
  },
  "cuisine": ["Indian", "Barbecue", "Asian"],
  "rating": 4.5,
  "numberOfReviews": 816,
  "features": ["Parking", "Reservations", "WiFi"],
  "mealType": ["Lunch", "Dinner"],
  "phone": "+91 73373 36712",
  "addressObj": {
    "country": "India",
    "state": "Karnataka",
    "postalcode": "560037"
  }
}
```

---

## Performance Tips

1. **Use `keyword` for exact matches** instead of `text`
2. **Add `gte` filters** before expensive geo-distance queries
3. **Limit aggregation results** with `size` parameter
4. **Use `_source: false`** if you only need scores/IDs
5. **Implement pagination** with `from` and `size`

---

## Troubleshooting

### No results for cuisine search

Ensure field exists and uses exact term:
```bash
# Check available cuisines
curl -s "http://localhost:9200/restaurants/_search?size=0" \
  -d '{"aggs": {"cuisines": {"terms": {"field": "cuisine"}}}}' | \
  jq '.aggregations.cuisines.buckets[].key'
```

### Geo search returns no results

Verify location field is populated:
```bash
curl -s "http://localhost:9200/restaurants/_search" \
  -d '{"query": {"exists": {"field": "location"}}}' | \
  jq '.hits.total.value'
```

---

## See Also

- [Main README](../README.md) - Project overview
- [Ramayana Dataset](../ramayana/README.md) - Complementary dataset
- [Setup Guide](../SETUP.md) - Installation instructions
