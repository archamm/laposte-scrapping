import json

def is_valid_json(file_name):
    try:
        with open(file_name, 'r') as f:
            json.load(f)
        print("File is valid JSON.")
        return True
    except ValueError as e:
        print("File is not valid JSON:", str(e))
        return False
    except FileNotFoundError:
        print("File not found.")
        return False

file_name = "TiersLieux/extracts/extract_raw_TiersLieux.json"  # replace with your file path
is_valid_json(file_name)
