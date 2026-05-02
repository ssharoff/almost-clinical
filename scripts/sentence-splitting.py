#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

"""Splitting texts into sentences
 Started from Colab suggestions
"""
import sys, re

def extract_and_clean_sentences(text_variable):
    """
    Takes a string variable with text, separates it into sentences,
    and cleans the text from formatting markups (e.g., asterisks).
    Newlines are treated as potential paragraph breaks, and sentences are
    then identified within these blocks, accounting for abbreviations like "Mr.".

    Args:
        text_variable (str): The input text string.

    Returns:
        list: A list of cleaned sentences.
    """
    all_sentences = []

    # Define common abbreviations that should not split a sentence if followed by a dot.
    abbreviations_to_replace = [
        "Mr.", "Dr.", "Mrs.", "Ms.", "Prof.", "Rev.", "Capt.", "Maj.",
        "Col.", "Gen.", "Lt.", "Sgt.", "Adm.", "Cpl.", "Pvt.", "Corp.",
        "Tel.", "etc.", "e.g.", "i.e.", "Fig.", "vs.", "approx.", "[A-Z]."
    ]

    # Process each line from the original text_variable separately
    for line in text_variable.split('\n'):
        # Remove markdown bold/italic asterisks
        cleaned_line = re.sub(r'\*\*|\*', '', line).strip()

        if not cleaned_line:
            continue

        processed_line = cleaned_line

        # Temporarily replace dots in common abbreviations with a placeholder
        for abbr in abbreviations_to_replace:
            processed_line = re.sub(r'\b' + re.escape(abbr), abbr.replace('.', '##TEMP_DOT##'), processed_line)

        # Split the line by sentence-ending punctuation (. ! ?)
        # This will split and *keep* the delimiters.
        # Example: "Hello. World!" -> ['Hello', '.', ' World', '!', '']
        parts = re.split(r'([.!?])', processed_line)

        current_sentence_builder = []
        for i, part in enumerate(parts):
            if not part.strip(): # Skip empty or whitespace-only parts
                continue

            current_sentence_builder.append(part)

            # If the current part is a sentence-ending punctuation or it's the very last part
            # This condition checks if a sentence has ended.
            if part in ['.', '!', '?']:
                final_sentence_candidate = "".join(current_sentence_builder).replace('##TEMP_DOT##', '.').strip()
                if final_sentence_candidate:
                    all_sentences.append(final_sentence_candidate)
                current_sentence_builder = []
            elif i == len(parts) - 1: # If it's the last part and it wasn't punctuation, append it as a sentence.
                final_sentence_candidate = "".join(current_sentence_builder).replace('##TEMP_DOT##', '.').strip()
                if final_sentence_candidate:
                    all_sentences.append(final_sentence_candidate)
                current_sentence_builder = []

    return all_sentences

# text="Please read the analysis. Mr. Smith, you'll be amazed. Tel. 2390-1243."
f=open(sys.argv[1]) if len(sys.argv)>1 else sys.stdin
text = f.read()
sentences = extract_and_clean_sentences(text)

print(f"{len(sentences)=}", file=sys.stderr)
for s in sentences:
    print(s)
