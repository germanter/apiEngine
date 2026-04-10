import json
import sys
import os

def validate_and_load(): #ai write this for me, looks fine for now
    # 1. Pathing inside the function
    # If this stays global, it runs on import. Keep it here.
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_path, "..", "incoming.json")

    # 2. Check if file even exists before trying to open
    if not os.path.exists(json_path):
        print(f"CRITICAL: {json_path} not found. Mission aborted.")
        sys.exit(1)

    # 1. Is it actual JSON?
    try:
        with open(json_path, "r") as file:
            data = json.load(file)
    except Exception:
        print("CRITICAL: Not a valid JSON string. Mission aborted.")
        sys.exit(1)

    # 2. Is it a list of objects [{}, {}]?
    if not isinstance(data, list):
        print("CRITICAL: Root structure is not a list. Mission aborted.")
        sys.exit(1)

    # 3. Strict Key Validation
    # We define exactly what we allow. No more, no less.

    allowed_keys = {"name", "desc", "url", "cost", "auth", "category"}

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            print(f"CRITICAL: Item at index {index} is not an object. Mission aborted.")
            sys.exit(1)

        current_keys = set(item.keys())

        # If keys don't match exactly (missing or extra), kill it.
        if current_keys != allowed_keys:
            missing = allowed_keys - current_keys
            extra = current_keys - allowed_keys
            print(f"CRITICAL: Schema mismatch at index {index}.")
            if missing: print(f"Missing: {missing}")
            if extra: print(f"Unauthorized extra keys: {extra}")
            sys.exit(1)

    # If we got here, it's 100% clean
    return data

def getMainData():
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_path, "..", "api.json")

    with open(json_path, "r") as file:
        data = json.load(file)
    return data


def dupCheck(dataset): 
    seen = {} # We will store {name: url}
    duplicates = []
    
    for item in dataset:
        name = item["name"]
        url = item["url"]

        if name in seen:
            # If the NAME was seen before, this is a dup
            duplicates.append({
                "url": url,
                "first_seen_url": seen[name], # Get the URL of the original
                "duplicate_name": name
            })
            item["dup"] = True
        else:
            # First time seeing this name, map it to its URL
            seen[name] = url

    if duplicates:
        # Filter the list to remove anything we tagged as "dup"
        dataset = [item for item in dataset if "dup" not in item]
        
        print(f"Duplicates found len({len(duplicates)}):")
        for dup in duplicates:
            print(f"Name: {dup['duplicate_name']}")
            print(f"Current URL: {dup['url']}")
            print(f"Original URL: {dup['first_seen_url']}")
            print("-" * 40)
    else:
        print("No duplicates found.")
        
    return dataset

def callInc():
    incData = validate_and_load()
    for i in incData:
        i["status"] = "UNKNOWN" 
        i["category"] = i["category"].strip()
    
    data = getMainData()
    data.extend(incData)
    data = dupCheck(data)

    #write to main

    base_path = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(base_path, "..", "api.json")

    with open(main_path, "w") as file:
        json.dump(data, file, indent=4)

