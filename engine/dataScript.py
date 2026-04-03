import json 
data = None
with open("engine\\data\\jsonDataset.json", "r") as file:
    data = json.load(file)

# print(json.dumps(data, indent=4))

def categoryOverride(data):
    for key in data.keys():
        for val in data[key]:
            val["category"] = key.strip()
    return data
            
def datasetNormalizer(data):
    #just done enter fucked up dict into this, i have no time to check this shit
    normalized = [d for lst in data.values() for d in lst]
    return normalized

def normalizedSaver(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def urlResolver(url):
    url = url.split("://")[1]
    url = url.rstrip("/")
    return url

def duplicateChecker(dataset): #this is for checking within data itself not new vs existing
    seen = {}
    duplicates = []
    
    for item in dataset:
        url = urlResolver(item["url"])
        if url in seen:
            duplicates.append({
                "url":url,
                "first_seen": seen[url],
                "duplicate": item["name"]
            })
            item["dup"] = True
        else:
            seen[url] = item["name"]
    
    if duplicates:
        dataset = [item for item in dataset if "dup" not in item]
        print(f"Duplicates found len({len(duplicates)}):")
        for dup in duplicates:
            print(f"URL: {dup['url']}, First Seen: {dup['first_seen']}, Duplicate: {dup['duplicate']}")
            print("-" * 40)
    else:
        print("No duplicates found.")
    return dataset

data = categoryOverride(data)
data = datasetNormalizer(data)
data = duplicateChecker(data)
normalizedSaver(data, "saved2.json")

