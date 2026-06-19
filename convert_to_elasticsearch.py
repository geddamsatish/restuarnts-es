#!/usr/bin/env python3
import csv
import json
import sys

def clean_list_field(value):
    """Convert space-separated values to a list, handling empty values"""
    if not value or not value.strip():
        return []
    # Split by multiple spaces and filter empty strings
    items = [item.strip() for item in value.split() if item.strip()]
    return items if items else []

def convert_csv_to_elasticsearch_json(csv_file, json_file, ndjson=False):
    """
    Convert Bengaluru Restaurants CSV to Elasticsearch JSON format.

    Args:
        csv_file: Input CSV file path
        json_file: Output JSON file path
        ndjson: If True, output newline-delimited JSON (better for bulk indexing)
    """
    restaurants = []

    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader):
            # Parse location coordinates
            lat = float(row.get('latitude', 0)) if row.get('latitude', '').strip() else None
            lon = float(row.get('longitude', 0)) if row.get('longitude', '').strip() else None

            # Build restaurant document
            doc = {
                "name": row.get('name', '').strip() or None,
                "address": row.get('address', '').strip(),
                "localAddress": row.get('localAddress', '').strip(),
                "addressObj": {
                    "country": row.get('addressObj/country', '').strip(),
                    "postalcode": row.get('addressObj/postalcode', '').strip(),
                    "state": row.get('addressObj/state', '').strip(),
                },
                "cuisine": clean_list_field(row.get('cuisine', '')),
                "description": row.get('description', '').strip() or None,
                "dietaryRestrictions": clean_list_field(row.get('DietaryRestrictions', '')),
                "dishes": clean_list_field(row.get('Dishes', '')),
                "features": clean_list_field(row.get('Features', '')),
                "mealType": clean_list_field(row.get('Meal Type', '')),
                "numberOfReviews": int(row.get('numberOfReviews', 0)) if row.get('numberOfReviews', '').strip() else 0,
                "phone": row.get('phone', '').strip(),
                "rankingInfo": {
                    "denominator": int(row.get('rankingDenominator', 0)) if row.get('rankingDenominator', '').strip() else 0,
                    "position": int(row.get('rankingPosition', 0)) if row.get('rankingPosition', '').strip() else 0,
                },
                "rating": float(row.get('rating', 0)) if row.get('rating', '').strip() else 0,
                "rawRanking": float(row.get('rawRanking', 0)) if row.get('rawRanking', '').strip() else 0,
            }

            # Only add location if both lat and lon are present
            if lat is not None and lon is not None:
                doc["location"] = {
                    "lat": lat,
                    "lon": lon,
                }

            restaurants.append(doc)

    # Write output
    if ndjson:
        # Newline-delimited JSON (better for Elasticsearch bulk indexing)
        with open(json_file, 'w', encoding='utf-8') as f:
            for doc in restaurants:
                f.write(json.dumps(doc) + '\n')
        print(f"✓ Created NDJSON file: {json_file}")
        print(f"  Total restaurants: {len(restaurants)}")
        print(f"  Format: Newline-delimited JSON (use with _bulk API)")
    else:
        # Standard JSON array
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(restaurants, f, indent=2, ensure_ascii=False)
        print(f"✓ Created JSON file: {json_file}")
        print(f"  Total restaurants: {len(restaurants)}")

if __name__ == '__main__':
    csv_input = '/Users/sgeddam/dev/satish-works/elastic-search/Bengaluru_Restaurants.csv'
    json_output = '/Users/sgeddam/dev/satish-works/elastic-search/Bengaluru_Restaurants_ES.json'
    ndjson_output = '/Users/sgeddam/dev/satish-works/elastic-search/Bengaluru_Restaurants_bulk.ndjson'

    print("Converting Bengaluru Restaurants CSV to Elasticsearch JSON...")
    print()

    # Create standard JSON
    convert_csv_to_elasticsearch_json(csv_input, json_output, ndjson=False)
    print()

    # Create NDJSON (better for bulk indexing)
    convert_csv_to_elasticsearch_json(csv_input, ndjson_output, ndjson=True)
    print()
    print("Sample document structure:")
    print("- name: Restaurant name")
    print("- address: Full address")
    print("- location: GeoJSON point (for geo queries)")
    print("- cuisine, dishes, features, mealType: Array fields")
    print("- rating: Float (0-5)")
    print("- numberOfReviews: Integer")
