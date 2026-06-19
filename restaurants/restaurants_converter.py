#!/usr/bin/env python3
"""
Bengaluru Restaurants CSV to Elasticsearch Converter
Kaggle dataset: https://www.kaggle.com/himanshuvaidya121/bengaluru-restaurants-more-on-theft
"""

import csv
import json
from pathlib import Path
from typing import Optional


def split_list_field(value: str) -> list:
    """Convert space-separated values to a list."""
    if not value or not value.strip():
        return []
    return [item.strip() for item in value.split() if item.strip()]


def convert_restaurants_csv(csv_file: str, json_file: str, ndjson: bool = False, limit: Optional[int] = None) -> int:
    """
    Convert Bengaluru Restaurants CSV to Elasticsearch JSON.

    Args:
        csv_file: Input CSV file path
        json_file: Output JSON file path
        ndjson: If True, output newline-delimited JSON
        limit: Maximum number of documents to process

    Returns:
        Number of documents processed
    """
    restaurants = []
    count = 0

    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            if limit and count >= limit:
                break

            # Parse location coordinates
            lat = float(row.get('latitude', 0)) if row.get('latitude', '').strip() else None
            lon = float(row.get('longitude', 0)) if row.get('longitude', '').strip() else None

            # Build document
            doc = {
                "name": row.get('name', '').strip() or None,
                "address": row.get('address', '').strip(),
                "localAddress": row.get('localAddress', '').strip(),
                "addressObj": {
                    "country": row.get('addressObj/country', '').strip(),
                    "postalcode": row.get('addressObj/postalcode', '').strip(),
                    "state": row.get('addressObj/state', '').strip(),
                },
                "cuisine": split_list_field(row.get('cuisine', '')),
                "description": row.get('description', '').strip() or None,
                "dietaryRestrictions": split_list_field(row.get('DietaryRestrictions', '')),
                "dishes": split_list_field(row.get('Dishes', '')),
                "features": split_list_field(row.get('Features', '')),
                "mealType": split_list_field(row.get('Meal Type', '')),
                "numberOfReviews": int(row.get('numberOfReviews', 0)) if row.get('numberOfReviews', '').strip() else 0,
                "phone": row.get('phone', '').strip(),
                "rankingInfo": {
                    "denominator": int(row.get('rankingDenominator', 0)) if row.get('rankingDenominator', '').strip() else 0,
                    "position": int(row.get('rankingPosition', 0)) if row.get('rankingPosition', '').strip() else 0,
                },
                "rating": float(row.get('rating', 0)) if row.get('rating', '').strip() else 0,
                "rawRanking": float(row.get('rawRanking', 0)) if row.get('rawRanking', '').strip() else 0,
            }

            # Only add location if both coordinates exist
            if lat is not None and lon is not None:
                doc["location"] = {"lat": lat, "lon": lon}

            restaurants.append(doc)
            count += 1

    # Write output
    Path(json_file).parent.mkdir(parents=True, exist_ok=True)

    if ndjson:
        with open(json_file, 'w', encoding='utf-8') as f:
            for doc in restaurants:
                f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    else:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(restaurants, f, indent=2, ensure_ascii=False)

    return count


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python restaurants_converter.py <input_csv> [output_json] [--ndjson]")
        sys.exit(1)

    csv_input = sys.argv[1]
    json_output = sys.argv[2] if len(sys.argv) > 2 else 'restaurants.json'
    is_ndjson = '--ndjson' in sys.argv

    count = convert_restaurants_csv(csv_input, json_output, ndjson=is_ndjson)
    print(f"✓ Converted {count} restaurants to {json_output}")
