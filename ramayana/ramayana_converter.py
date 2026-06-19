#!/usr/bin/env python3
"""
Ramayana CSV to Elasticsearch Converter
Converts Ramayana shlokas data to Elasticsearch JSON
"""

import csv
import json
from pathlib import Path
from typing import Optional


def convert_ramayana_csv(csv_file: str, json_file: str, ndjson: bool = False, limit: Optional[int] = None) -> int:
    """
    Convert Ramayana CSV to Elasticsearch JSON.

    Args:
        csv_file: Input CSV file path
        json_file: Output JSON file path
        ndjson: If True, output newline-delimited JSON
        limit: Maximum number of documents to process

    Returns:
        Number of documents processed
    """
    shlokas = []
    count = 0

    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            if limit and count >= limit:
                break

            # Build document
            doc = {
                "kanda": row.get('kanda', '').strip(),
                "sarga": int(row.get('sarga', 0)) if row.get('sarga', '').strip() else None,
                "shloka": int(row.get('shloka', 0)) if row.get('shloka', '').strip() else None,
                "shloka_text": row.get('shloka_text', '').strip(),
                "transliteration": row.get('transliteration', '').strip() or None,
                "translation": row.get('translation', '').strip() or None,
                "explanation": row.get('explanation', '').strip() or None,
                "comments": row.get('comments', '').strip() or None,
            }

            shlokas.append(doc)
            count += 1

    # Write output
    Path(json_file).parent.mkdir(parents=True, exist_ok=True)

    if ndjson:
        with open(json_file, 'w', encoding='utf-8') as f:
            for doc in shlokas:
                f.write(json.dumps(doc, ensure_ascii=False) + '\n')
    else:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(shlokas, f, indent=2, ensure_ascii=False)

    return count


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ramayana_converter.py <input_csv> [output_json] [--ndjson]")
        sys.exit(1)

    csv_input = sys.argv[1]
    json_output = sys.argv[2] if len(sys.argv) > 2 else 'ramayana.json'
    is_ndjson = '--ndjson' in sys.argv

    count = convert_ramayana_csv(csv_input, json_output, ndjson=is_ndjson)
    print(f"✓ Converted {count} shlokas to {json_output}")
