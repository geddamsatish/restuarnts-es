#!/usr/bin/env python3
"""
CLI tool for converting CSV files to Elasticsearch JSON.

Usage:
    python cli.py --input data.csv --output data.json --index myindex
    python cli.py --input data.csv --output data.ndjson --index myindex --ndjson
"""

import argparse
import sys
from pathlib import Path
from .converter import CSVToElasticsearchConverter
from .restaurants_converter import RestaurantsConverter


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description='Convert CSV files to Elasticsearch-compatible JSON',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generic CSV to JSON
  python cli.py --input restaurants.csv --output restaurants.json

  # Create NDJSON for bulk indexing
  python cli.py --input restaurants.csv --output restaurants.ndjson --ndjson

  # Use specialized restaurants converter
  python cli.py --input restaurants.csv --output restaurants.json --dataset restaurants

  # Create bulk format and index to Elasticsearch
  python cli.py --input restaurants.csv --output restaurants.ndjson --ndjson --index bengaluru_restaurants --bulk
        '''
    )

    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input CSV file path'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output JSON file path'
    )
    parser.add_argument(
        '--index',
        default='documents',
        help='Elasticsearch index name (default: documents)'
    )
    parser.add_argument(
        '--ndjson',
        action='store_true',
        help='Output newline-delimited JSON instead of array'
    )
    parser.add_argument(
        '--bulk',
        action='store_true',
        help='Create Elasticsearch bulk format file (requires --ndjson)'
    )
    parser.add_argument(
        '--dataset',
        choices=['generic', 'restaurants'],
        default='generic',
        help='Dataset type for specialized handling (default: generic)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='Maximum number of documents to process'
    )
    parser.add_argument(
        '--encoding',
        default='utf-8-sig',
        help='File encoding (default: utf-8-sig)'
    )

    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Validate bulk format requirements
    if args.bulk and not args.ndjson:
        print("Error: --bulk requires --ndjson flag", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"Converting {args.input} to Elasticsearch format...")
        print(f"  Dataset type: {args.dataset}")
        print(f"  Output format: {'NDJSON' if args.ndjson else 'JSON'}")
        if args.limit:
            print(f"  Limit: {args.limit} documents")
        print()

        # Select converter
        if args.dataset == 'restaurants':
            converter = RestaurantsConverter()
        else:
            converter = CSVToElasticsearchConverter(encoding=args.encoding)

        # Convert to JSON/NDJSON
        count = converter.convert_csv_to_json(
            csv_file=args.input,
            json_file=args.output,
            ndjson=args.ndjson,
            limit=args.limit
        )

        print(f"✓ Converted {count} documents")
        print(f"  Output: {args.output}")

        # Create bulk format if requested
        if args.bulk:
            bulk_output = str(args.output).replace('.ndjson', '_bulk.ndjson')
            bulk_count = converter.create_bulk_format(
                ndjson_file=args.output,
                bulk_file=bulk_output,
                index=args.index
            )
            print()
            print(f"✓ Created bulk format file")
            print(f"  Output: {bulk_output}")
            print(f"  Ready for Elasticsearch _bulk API")
            print()
            print(f"To index to Elasticsearch:")
            print(f"  curl -X POST 'localhost:9200/_bulk' \\")
            print(f"    -H 'Content-Type: application/json' \\")
            print(f"    --data-binary @{bulk_output}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
