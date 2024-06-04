#!/bin/bash 

echo "Cleaning the data"
python3 clean_and_anonymize_data.py

echo "Generating derived features"
python3 generate_derived_features.py

echo "Generating docs"
python3 generate_docstring.py