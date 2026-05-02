#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

# Copyright (C) 2019  Serge Sharoff
# This program is free software under GPL 3, see http://www.gnu.org/licenses/
# The tool converts a json file with generated text to a word document while removing sentences with boilerplate, such as
patterns=[
    r"I can provide [^.]*\.",
    r"I can't provide a response [^.]*\.",
    r"Please note that [^.]*\.",
    r"If you're looking for [^.]*\.",
    ]

import sys, json, re

compiled_patterns = [re.compile(p) for p in patterns]

o = sys.argv[1]

f = open(sys.argv[2]) if len(sys.argv)>2 else sys.stdin

import tempfile
import subprocess
from pathlib import Path

def extract_assistant_text(generated_text):
    """
    Extract the text for `"role": "assistant"` from the generated_text.
    Works for either structured JSON-like text or plain text outputs.
    """
    # Try to parse as JSON (if the model returned structured content)
    try:
        # data = json.loads(generated_text)
        data = generated_text
        if isinstance(data, list):
            for record in data:
                if isinstance(record, dict) and record.get("role") == "assistant":
                    return record.get("content", "").strip()
        elif isinstance(data, dict) and data.get("role") == "assistant":
            return data.get("content", "").strip()
    except json.JSONDecodeError:
        # Not JSON — try simple text extraction
        pass

    # Fallback: heuristic extraction (if text contains role indicators)
    if '"role": "assistant"' in generated_text:
        start = generated_text.find('"role": "assistant"')
        snippet = generated_text[start:]
        end = snippet.find('"role": "user"')
        text_block = snippet[:end] if end != -1 else snippet
        return text_block.strip()
    
    # Fallback: assume the entire generated_text is from the assistant
    return generated_text.strip()

def clean_assistant_text(text):
    for pat in compiled_patterns:
        text = re.sub(pat, "", text)
    return re.sub(r'\s{2,}', ' ', text).strip()
    
collected_texts = []
for i,l in enumerate(f):
    try:
        rec = json.loads(l)
    except json.JSONDecodeError:
        print(f"Failed in line: {i}, file: {f}")
        break
                
    filename = rec.get("filename", "unknown")
    generated_text = rec.get("generated_text", "")
    assistant_text = extract_assistant_text(generated_text)
    cleaned_text = clean_assistant_text(assistant_text)
    collected_texts.append(f"# {filename}\n\n{assistant_text}\n")

# Write to temporary markdown file
# with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as tmp_md:
with open(o+'.md', mode="w") as outf:
    # tmp_md_path = tmp_md.name
    outf.write("\n\n".join(collected_texts))
# print(f"✅ Temporary Markdown file created: {tmp_md_path}")

# Run Pandoc to convert to DOCX
# cmd = ["pandoc", tmp_md_path, "-f", "gfm", "-o", o + ".docx"]
# try:
#     subprocess.run(cmd, check=True)
#     print(f"✅ Word document created: {o}")
# except subprocess.CalledProcessError as e:
#     print(f"❌ Pandoc failed: {e}")
# finally:
#     Path(tmp_md_path).unlink(missing_ok=True)  # Clean up



