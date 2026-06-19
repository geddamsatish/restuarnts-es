#!/usr/bin/env python3
"""
CSV to Elasticsearch JSON Converter

Converts CSV files to Elasticsearch-compatible JSON formats (standard JSON and NDJSON).
Supports custom field mappings, type conversions, and data transformations.
"""

import csv
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable


class CSVToElasticsearchConverter:
    """Convert CSV files to Elasticsearch-compatible JSON formats."""

    def __init__(self, encoding: str = 'utf-8-sig'):
        """
        Initialize the converter.

        Args:
            encoding: File encoding (default: 'utf-8-sig' for handling BOM)
        """
        self.encoding = encoding
        self.field_mappings = {}
        self.type_conversions = {}
        self.transformers = {}

    def add_field_mapping(self, csv_field: str, json_field: str) -> None:
        """Map CSV column name to JSON field name."""
        self.field_mappings[csv_field] = json_field

    def add_type_conversion(self, field: str, conversion_fn: Callable) -> None:
        """Add a type conversion function for a field."""
        self.type_conversions[field] = conversion_fn

    def add_transformer(self, field: str, transform_fn: Callable) -> None:
        """Add a transformation function for a field."""
        self.transformers[field] = transform_fn

    def _split_list_field(self, value: str, separator: str = ' ') -> List[str]:
        """
        Convert space or custom-separated values to a list.

        Args:
            value: String value to split
            separator: Delimiter to use (default: space)

        Returns:
            List of non-empty strings
        """
        if not value or not value.strip():
            return []
        items = [item.strip() for item in value.split(separator) if item.strip()]
        return items

    def _convert_value(self, field: str, value: str) -> Any:
        """
        Convert field value to appropriate type.

        Args:
            field: Field name
            value: String value to convert

        Returns:
            Converted value or None if empty
        """
        if not value or not str(value).strip():
            return None

        # Use custom conversion if available
        if field in self.type_conversions:
            return self.type_conversions[field](value)

        # Try to infer type from field name
        if any(x in field.lower() for x in ['rating', 'score', 'price']):
            try:
                return float(value)
            except (ValueError, TypeError):
                return value.strip()
        elif any(x in field.lower() for x in ['count', 'number', 'id']):
            try:
                return int(value)
            except (ValueError, TypeError):
                return value.strip()
        else:
            return value.strip()

    def _get_output_field_name(self, csv_field: str) -> str:
        """Get the output field name (mapped or original)."""
        return self.field_mappings.get(csv_field, csv_field)

    def process_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """
        Process a single CSV row into a document.

        Args:
            row: Dictionary representing a CSV row

        Returns:
            Processed document dictionary
        """
        doc = {}

        for csv_field, value in row.items():
            if csv_field is None:
                continue

            output_field = self._get_output_field_name(csv_field)
            converted_value = self._convert_value(output_field, value)

            # Apply custom transformer if available
            if output_field in self.transformers:
                converted_value = self.transformers[output_field](converted_value)

            doc[output_field] = converted_value

        return doc

    def convert_csv_to_json(
        self,
        csv_file: str,
        json_file: str,
        ndjson: bool = False,
        limit: Optional[int] = None,
    ) -> int:
        """
        Convert CSV file to JSON format.

        Args:
            csv_file: Input CSV file path
            json_file: Output JSON file path
            ndjson: If True, output newline-delimited JSON
            limit: Maximum number of documents to process

        Returns:
            Number of documents processed
        """
        documents = []
        count = 0

        with open(csv_file, 'r', encoding=self.encoding) as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError(f"No headers found in {csv_file}")

            for row in reader:
                if limit and count >= limit:
                    break

                doc = self.process_row(row)
                documents.append(doc)
                count += 1

        # Write output
        output_path = Path(json_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if ndjson:
            with open(json_file, 'w', encoding='utf-8') as f:
                for doc in documents:
                    f.write(json.dumps(doc, ensure_ascii=False) + '\n')
        else:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(documents, f, indent=2, ensure_ascii=False)

        return count

    def create_bulk_format(self, ndjson_file: str, bulk_file: str, index: str = 'documents') -> int:
        """
        Convert NDJSON to Elasticsearch bulk format.

        Args:
            ndjson_file: Input NDJSON file path
            bulk_file: Output bulk format file path
            index: Elasticsearch index name

        Returns:
            Number of documents processed
        """
        count = 0
        output_path = Path(bulk_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(ndjson_file, 'r', encoding='utf-8') as infile, \
             open(bulk_file, 'w', encoding='utf-8') as outfile:
            for line in infile:
                if line.strip():
                    outfile.write(json.dumps({'index': {'_index': index}}) + '\n')
                    outfile.write(line)
                    count += 1

        return count
