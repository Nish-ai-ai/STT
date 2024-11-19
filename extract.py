import spacy
import re
import json
import os

# Load spaCy language model
nlp = spacy.load("en_core_web_sm")

# Function to extract name, phone, and address from text
def extract_entities(text):
    details = {"name": None, "phone": None, "address": None}
    doc = nlp(text)

    # Extract name based on PERSON entity
    for ent in doc.ents:
        if ent.label_ == "PERSON" and details["name"] is None:
            details["name"] = ent.text

    # Extract address using GPE/LOC entities or keywords
    for ent in doc.ents:
        if ent.label_ in {"GPE", "LOC"} and details["address"] is None:
            details["address"] = ent.text

    address_keywords = ["address is", "located at", "live at", "reside at", "stay at"]
    for keyword in address_keywords:
        if keyword in text.lower():
            address_match = re.search(f'{keyword} (.+)', text, re.IGNORECASE)
            if address_match:
                details["address"] = address_match.group(1)
                break

    # Extract phone numbers with regex
    phone_match = re.search(r'\b(?:\d{3}[-.\s]??\d{3}[-.\s]??\d{4})\b', text)
    if phone_match:
        details["phone"] = phone_match.group()

    return details

# Main function to process input and save output
def main():
    # Ensure input file exists
    input_file = "output.txt"
    output_file = "extracted.json"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    # Read input text
    with open(input_file, "r") as f:
        text = f.read()

    if not text.strip():
        print("Error: Input file is empty.")
        return

    # Extract entities
    extracted_data = extract_entities(text)

    # Save extracted data to JSON file
    with open(output_file, "w") as f:
        json.dump(extracted_data, f, indent=4)

    print(f"Extracted data saved to {output_file}")

# Execute the script
if __name__ == "__main__":
    main()
