#!/usr/bin/env python3
import csv
import json
import re
import requests
import io
import sys
import os
from io import StringIO

# Set UTF-8 as default encoding for all I/O operations
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Hardcoded Google Sheets URL for Japanese conjugation data
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ2JYD9F35V9EfYtV7sqPx8DpCx-kDEQgSTbnKoQRCljpszh6cUNO3lGrx6tl52SwGrJLwlzBPtNt1M/pub?output=csv"
# Alternative format that might avoid encoding issues
GOOGLE_SHEETS_XLSX_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ2JYD9F35V9EfYtV7sqPx8DpCx-kDEQgSTbnKoQRCljpszh6cUNO3lGrx6tl52SwGrJLwlzBPtNt1M/pub?output=xlsx"

def clean_string(s):
    """Clean string values and handle NaN/empty values"""
    if not s or s.lower() == 'nan' or s == '':
        return None
    return s.strip()

def download_and_save_file(url, output_path):
    """Download file from URL and save to disk"""
    response = requests.get(url)
    response.raise_for_status()
    
    with open(output_path, 'wb') as f:
        f.write(response.content)
    
    return output_path

def csv_to_typescript(output_file_path, csv_file_path=None, use_manual_download=False):
    """Convert CSV from local file to TypeScript
    
    Args:
        output_file_path: Path where to save the TypeScript output
        csv_file_path: Path to a local CSV file (if provided)
        use_manual_download: If True, suggests manual download instead of auto-fetching
    """
    # Define the TypeScript template with types and structure
    typescript_header = """export interface ConjugationItem {
  Word: {
    // Dictionary form information
    dictionary: {
      kanji: string
      hiragana: string
    }
    // Word metadata
    definition: string
    type: WordType
  }
  // Conjugation forms
  "Present Affirmative": {
    kanji: string
    hiragana: string
  }
  "Present Negative": {
    kanji: string
    hiragana: string
  }
  "Past Affirmative": {
    kanji: string
    hiragana: string
  }
  "Past Negative": {
    kanji: string
    hiragana: string
  }
  "Te Form": {
    kanji: string
    hiragana: string
  } | null
}

export type WritingSystem = "kanji" | "hiragana"
export type VerbForm = "dictionary" | "masu"
export type WordType =
  | "verb-ru"
  | "verb-u"
  | "verb-irregular"
  | "noun"
  | "adjective-i"
  | "adjective-na"
  | "adverb"
  | "particle"
  | "expression"

// Restructured conjugation data with improved organization
export const conjugationData: ConjugationItem[] = [
"""

    typescript_footer = "]"

    conjugation_items = []
    
    if use_manual_download and not csv_file_path:
        print("Due to potential encoding issues with Japanese characters, please:")
        print(f"1. Open this URL in your browser: {GOOGLE_SHEETS_URL}")
        print("2. Download the CSV file manually")
        print("3. Run this script again with: python csv_to_typescript.py --local your_downloaded_file.csv")
        return

    # Handle CSV input from local file
    if not csv_file_path:
        # If no local file provided, instruct user to download manually
        print("Due to encoding issues with Japanese characters from direct URL access,")
        print("please download the CSV file manually and provide the local path.")
        print(f"\nDownload from: {GOOGLE_SHEETS_URL}")
        print("Then run: python csv_to_typescript.py --local your_downloaded_file.csv")
        return
        
    try:
        # Process CSV file with explicit UTF-8 encoding
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            process_csv_rows(reader, conjugation_items)
    except UnicodeDecodeError:
        # If UTF-8 fails, try with Shift-JIS (common for Japanese CSV files)
        print("UTF-8 encoding failed, trying with Shift-JIS encoding...")
        with open(csv_file_path, 'r', encoding='shift_jis') as csvfile:
            reader = csv.DictReader(csvfile)
            process_csv_rows(reader, conjugation_items)

    # Generate TypeScript code
    with open(output_file_path, 'w', encoding='utf-8') as ts_file:
        ts_file.write(typescript_header)
        
        for i, item in enumerate(conjugation_items):
            # Convert to formatted JSON string
            json_str = json.dumps(item, ensure_ascii=False, indent=2)
            
            # Add comma after every item except the last one
            if i < len(conjugation_items) - 1:
                json_str += ","
            
            # Write the item to the TypeScript file
            ts_file.write(f"  {json_str}")
        
        ts_file.write(typescript_footer)

def process_csv_rows(reader, conjugation_items):
    """Process CSV rows into conjugation item objects"""
    for row in reader:
        # Extract values from CSV, handling potential column name variations
        definition = clean_string(row.get('Definition'))
        word_type = clean_string(row.get('Type'))
        
        dict_hiragana = clean_string(row.get('Vocab Dictionary Hiragana'))
        dict_kanji = clean_string(row.get('Vocab dictionary Kanji'))
        
        present_aff_hiragana = clean_string(row.get('Present Postive Hiragana') or row.get('Vocab Masu Hiragana'))
        present_aff_kanji = clean_string(row.get('Present Postive Kanji') or row.get('Vocab Masu Kanji'))
        
        present_neg_hiragana = clean_string(row.get('Present Negative Hiragana'))
        present_neg_kanji = clean_string(row.get('Present Negative Kanji'))
        
        past_aff_hiragana = clean_string(row.get('Past Postive Hiragana'))
        past_aff_kanji = clean_string(row.get('Past Postive Kanji'))
        
        past_neg_hiragana = clean_string(row.get('Past Negatie Hiragana'))
        past_neg_kanji = clean_string(row.get('Past Negative Kanji'))
        
        te_form_kanji = clean_string(row.get('Te form Kanji'))
        te_form_hiragana = clean_string(row.get('Te form Hiragana'))
        
        # Print some debug information to help diagnose encoding issues
        if dict_kanji:
            print(f"Processing: {dict_kanji} ({dict_hiragana})")
        
        # Skip rows with missing essential data
        if not (dict_hiragana and dict_kanji and definition and word_type):
            print(f"Skipping row due to missing essential data: {dict_kanji if dict_kanji else 'Unknown'}")
            continue
            
        # Map the word type to the TypeScript enum format
        type_mapping = {
            "ru-verb": "verb-ru",
            "u-verb": "verb-u",
            "irregular": "verb-irregular",
            # Add other mappings as needed
        }
        
        # Use regex to determine if word type needs mapping
        mapped_type = word_type
        for pattern, type_value in type_mapping.items():
            if re.search(pattern, word_type, re.IGNORECASE):
                mapped_type = type_value
                break
        
        # Create a conjugation item object
        conjugation_item = {
            "Word": {
                "dictionary": {
                    "kanji": dict_kanji,
                    "hiragana": dict_hiragana
                },
                "definition": definition,
                "type": mapped_type
            },
            "Present Affirmative": {
                "kanji": present_aff_kanji,
                "hiragana": present_aff_hiragana
            },
            "Present Negative": {
                "kanji": present_neg_kanji,
                "hiragana": present_neg_hiragana
            },
            "Past Affirmative": {
                "kanji": past_aff_kanji,
                "hiragana": past_aff_hiragana
            },
            "Past Negative": {
                "kanji": past_neg_kanji,
                "hiragana": past_neg_hiragana
            }
        }
        
        # Handle Te form with dedicated columns for kanji and hiragana
        if te_form_kanji or te_form_hiragana:
            conjugation_item["Te Form"] = {
                "kanji": te_form_kanji or "",
                "hiragana": te_form_hiragana or ""
            }
        else:
            conjugation_item["Te Form"] = None
        
        conjugation_items.append(conjugation_item)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Convert Japanese conjugation CSV to TypeScript')
    parser.add_argument('--local', '-l', 
                        help='Path to a local CSV file (required due to encoding considerations)')
    parser.add_argument('--output', '-o', default='conjugation_data.ts', 
                        help='Path to the output TypeScript file (default: conjugation_data.ts)')
    
    args = parser.parse_args()
    
    csv_to_typescript(args.output, args.local, use_manual_download=True)
    
    if args.local:
        print(f"\nSuccessfully converted {args.local} to {args.output}")