#!/usr/bin/env python3
"""
Bengaluru Restaurants CSV to Elasticsearch Converter

Specialized converter for Kaggle Bengaluru Restaurants dataset.
Handles nested address objects, location coordinates, and list fields.
"""

from typing import Dict, Any, List, Optional
from .converter import CSVToElasticsearchConverter


class RestaurantsConverter(CSVToElasticsearchConverter):
    """Convert Bengaluru Restaurants CSV to Elasticsearch format."""

    def __init__(self):
        super().__init__(encoding='utf-8-sig')
        self._setup_field_mappings()
        self._setup_type_conversions()
        self._setup_transformers()

    def _setup_field_mappings(self):
        """Configure field name mappings."""
        mappings = {
            'Meal Type': 'mealType',
            'DietaryRestrictions': 'dietaryRestrictions',
            'Features': 'features',
            'Dishes': 'dishes',
        }
        for csv_field, json_field in mappings.items():
            self.add_field_mapping(csv_field, json_field)

    def _setup_type_conversions(self):
        """Configure type conversions."""
        def to_float(val):
            if isinstance(val, str):
                val = val.strip()
            return float(val) if val else None

        def to_int(val):
            if isinstance(val, str):
                val = val.strip()
            return int(val) if val else 0

        self.add_type_conversion('latitude', to_float)
        self.add_type_conversion('longitude', to_float)
        self.add_type_conversion('rating', to_float)
        self.add_type_conversion('rawRanking', to_float)
        self.add_type_conversion('numberOfReviews', to_int)
        self.add_type_conversion('rankingDenominator', to_int)
        self.add_type_conversion('rankingPosition', to_int)

    def _setup_transformers(self):
        """Configure field transformers."""
        # Convert list fields
        for field in ['cuisine', 'mealType', 'dietaryRestrictions', 'dishes', 'features']:
            self.add_transformer(field, lambda val: self._split_list_field(val) if val else [])

    def process_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """
        Process restaurant row with special handling for nested fields and locations.

        Args:
            row: Dictionary representing a CSV row

        Returns:
            Processed restaurant document
        """
        doc = {}

        # Standard fields
        standard_fields = {
            'name': 'name',
            'address': 'address',
            'localAddress': 'localAddress',
            'phone': 'phone',
            'description': 'description',
        }

        for csv_field, json_field in standard_fields.items():
            if csv_field in row:
                doc[json_field] = self._convert_value(json_field, row.get(csv_field, ''))

        # List fields
        list_fields = ['cuisine', 'mealType', 'dietaryRestrictions', 'dishes', 'features']
        for field in list_fields:
            if field in row:
                doc[field] = self._split_list_field(row.get(field, ''))

        # Nested address object
        doc['addressObj'] = {
            'country': row.get('addressObj/country', '').strip(),
            'postalcode': row.get('addressObj/postalcode', '').strip(),
            'state': row.get('addressObj/state', '').strip(),
        }

        # Location (geo_point) - only add if both coordinates exist
        lat = self._convert_value('latitude', row.get('latitude', ''))
        lon = self._convert_value('longitude', row.get('longitude', ''))
        if lat is not None and lon is not None:
            doc['location'] = {
                'lat': lat,
                'lon': lon,
            }

        # Numeric fields
        doc['numberOfReviews'] = self._convert_value('numberOfReviews', row.get('numberOfReviews', ''))
        doc['rating'] = self._convert_value('rating', row.get('rating', ''))
        doc['rawRanking'] = self._convert_value('rawRanking', row.get('rawRanking', ''))

        # Ranking info
        doc['rankingInfo'] = {
            'denominator': self._convert_value('rankingDenominator', row.get('rankingDenominator', '')),
            'position': self._convert_value('rankingPosition', row.get('rankingPosition', '')),
        }

        return doc
