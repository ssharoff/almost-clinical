#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

#!/usr/bin/env python3
"""
Generate text files by filling a template with all combinations of variable values.

Usage:
    python generate_texts.py --template template.txt --json data.json --output_dir output_texts
"""

import argparse
import json
import os, re
import itertools

def sanitize_for_filename(value):
    """
    If the value contains any non-alphanumeric character, return the concatenation
    of the first alphanumeric character of each word; otherwise return the value itself.
    """
    # Detect if value contains any non-alphanumeric characters
    if not value.isalnum():
        # Extract first character of each alphanumeric word
        words = re.findall(r"[A-Za-z0-9]+", value)
        initials = "".join(word[0] for word in words if word)
        return initials.lower()
    return value


def main():
    parser = argparse.ArgumentParser(description="Generate text files from a template and JSON variable lists.")
    parser.add_argument("-t", "--template", required=True, help="Path to the template text file (with {variables}).")
    parser.add_argument("-j", "--json", required=True, help="Path to the JSON file with variable lists.")
    parser.add_argument("-o", "--output_dir", default="outputs", help="Directory to save generated text files.")
    args = parser.parse_args()

    # --- Read template ---
    with open(args.template, "r") as f:
        template_text = f.read()

    # --- Load variable data ---
    with open(args.json, "r") as f:
        data = json.load(f)

    # --- Ensure output directory exists ---
    try:
        os.makedirs(args.output_dir)
    except:
        print(args.output_dir)

    # --- Generate combinations ---
    variable_names = list(data.keys())
    value_lists = [data[var] for var in variable_names]

    for combination in itertools.product(*value_lists):
        # Build substitution dict
        values_dict = dict(zip(variable_names, combination))

        # Fill template
        filled_text = template_text.format(**values_dict)

        # Build filename
        filename_parts = [sanitize_for_filename(str(v)) for v in combination]
        filename = "-".join(filename_parts) + ".txt"
        filepath = os.path.join(args.output_dir, filename)

        # Save file
        with open(filepath, "w") as out:
            out.write(filled_text)

        # print(f"Generated: {filepath}")
        print(filepath)
    print("All combinations generated successfully.")


if __name__ == "__main__":
    main()
