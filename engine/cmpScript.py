import json
import os


    # {
    #     "n": "OpenAI API",
    #     "d": "Text, image, speech, embeddings models via REST API",
    #     "u": "https://platform.openai.com/docs/api-reference",
    #     "m": "freemium",  //m = money = cost
    #     "a": true,
    #     "c": "AI",
    #     "s": 1 / 0 / -1  -- 1 alive 0 dead -1 unknown
    # },
# This finds the file regardless of where the script is called from
base_path = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_path, "..", "api.json")
save_path = os.path.join(base_path, "..", "apiCmp.json") #to save at end

data = None
with open(json_path, "r") as file:
    data = json.load(file)

keyMAP = {
    "name": "n",
    "description": "d",
    "url": "u",
    "cost": "m",
    "active": "a",
    "category": "c",
    "status": "s"
}

statusMAP = {
    "ALIVE": 1,
    "DEAD": 0,
    "UNKNOWN": -1
}

def compressor(data):
    compressed = []
    for item in data:
        cmp = {}

        if item["status"] in statusMAP:
            item["status"] = statusMAP[item["status"]]

        for key,val in item.items():
            if key in keyMAP:
                cmp[keyMAP[key]] = val
        compressed.append(cmp)

    return compressed

data = compressor(data)  #60% reduced size tier 1
with open(save_path, "w") as file:    
    json.dump(data, file, separators=(',', ':'))