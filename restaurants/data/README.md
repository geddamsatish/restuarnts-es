# Bengaluru Restaurants Dataset

This folder contains the raw dataset files for the Bengaluru Restaurants project.

## Files

- **Bengaluru_Restaurants.csv** (3.2 MB)
  - Source: [Kaggle - Bengaluru Restaurants Dataset](https://www.kaggle.com/datasets/mrmars1010/restaurants-dataset-bengaluru/data)
  - Format: CSV with 9,291 restaurant records
  - Includes: Restaurant names, locations, cuisines, ratings, reviews, etc.

## Usage

### Convert to JSON for Elasticsearch

```bash
# From restaurants directory
python restaurants_converter.py data/Bengaluru_Restaurants.csv output.json

# Convert to NDJSON (for bulk indexing)
python restaurants_converter.py data/Bengaluru_Restaurants.csv output.ndjson --ndjson
```

## Data Structure

The CSV contains the following columns:
- name
- address
- localAddress
- addressObj/country, addressObj/postalcode, addressObj/state
- cuisine
- description
- DietaryRestrictions
- Dishes
- Features
- latitude, longitude
- Meal Type
- numberOfReviews
- phone
- rankingDenominator, rankingPosition
- rating
- rawRanking

## Notes

- UTF-8 encoding with BOM marker
- Some restaurants may have missing location data
- Ratings are on a 0-5 scale
- See parent README.md for sample queries

## License

Dataset source: Kaggle (refer to Kaggle's terms for usage)
