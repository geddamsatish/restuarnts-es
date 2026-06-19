import csv
import json
import re

def clean_multi_space_array(text):
    """Splits strings separated by two or more spaces into clean arrays."""
    if not text:
        return []
    # Tokenizes strings while preserving multi-word phrases like 'Vegetarian Friendly'
    items = re.split(r'\s{2,}', text.strip())
    return [i.strip() for i in items if i.strip()]

def clean_single_space_array(text):
    """Splits simple single-space words into arrays."""
    if not text:
        return []
    return [i.strip() for i in text.strip().split(' ') if i.strip()]

def convert_csv_to_json(csv_filepath, json_filepath):
    all_restaurants = []
    
    with open(csv_filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            structured_doc = {
                "name": row.get("name"),
                "address": row.get("address"),
                "localAddress": row.get("localAddress"),
                "addressObj": {
                    "country": row.get("addressObj/country"),
                    "postalcode": row.get("addressObj/postalcode"),
                    "state": row.get("addressObj/state")
                },
                "cuisine": clean_single_space_array(row.get("cuisine")),
                "description": row.get("description"),
                "dietary_restrictions": clean_multi_space_array(row.get("DietaryRestrictions")),
                "dishes": clean_single_space_array(row.get("Dishes")),
                "features": clean_multi_space_array(row.get("Features")),
                "meal_type": clean_multi_space_array(row.get("Meal Type")),
                "metrics": {
                    "numberOfReviews": int(row["numberOfReviews"]) if row.get("numberOfReviews") else 0,
                    "rankingDenominator": int(row["rankingDenominator"]) if row.get("rankingDenominator") else 0,
                    "rankingPosition": int(row["rankingPosition"]) if row.get("rankingPosition") else 0,
                    "rating": float(row["rating"]) if row.get("rating") else 0.0,
                    "rawRanking": float(row["rawRanking"]) if row.get("rawRanking") else 0.0
                },
                "phone": row.get("phone"),
                "location": {
                    "lat": float(row["latitude"]) if row.get("latitude") else 0.0,
                    "lon": float(row["longitude"]) if row.get("longitude") else 0.0
                }
            }
            all_restaurants.append(structured_doc)
            
    # Write output to an aligned JSON file
    with open(json_filepath, mode='w', encoding='utf-8') as out_f:
        json.dump(all_restaurants, out_f, indent=2)
    print(f"Successfully converted CSV to {json_filepath}")

# Execute conversion:
convert_csv_to_json("Bengaluru_Restaurants.csv", "Bengaluru_Restaurants.json")
