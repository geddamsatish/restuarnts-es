#!/usr/bin/env python3
import json

# Read the regular NDJSON file
with open('Bengaluru_Restaurants_bulk.ndjson', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Create bulk format with index metadata
with open('Bengaluru_Restaurants_bulk_indexed.ndjson', 'w', encoding='utf-8') as f:
    for line in lines:
        # Write the action/metadata line
        f.write('{"index": {"_index": "restaurants"}}\n')
        # Write the document
        f.write(line)

print(f"✓ Created bulk-formatted NDJSON with {len(lines)} documents")
print("  File: Bengaluru_Restaurants_bulk_indexed.ndjson")
