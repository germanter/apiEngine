import random

cats = [
    "AI", 
    "Data & Information", 
    "Developer Utilities", 
    "Location & Maps", 
    "Security & Safety", 
    "Scraping", 
    ]

def get_prompt():
    category = random.choice(cats)
    prompt = f"""
Task:
Search from internet, List real, currently available {category} APIs (as of latest knowledge). Do not include deprecated, unofficial, invite-only, or unclear APIs.

Strict rules:
- Output MUST be valid JSON (parsable).
- No trailing commas.
- No comments.
- No duplicate entries.
- Prefer official API providers (not SDKs, not apps, not wrappers unless widely used).
- Try to add as much as APIs to the list 10 is a good number
-categoryName = {category}

Each object must follow EXACT schema:

{{
"name": "string",
"desc": "string (max 12 words, factual, no marketing language)",
"url": "string (direct docs or API console URL)",
"cost": "free | freemium | premium",
"auth": true,
"category": "string"
}}

Field constraints:
- "desc": short, concrete, what it actually does.
- "url": prefer docs or API console (not homepage unless necessary).
- "cost":
- free = usable without payment
- freemium = free tier or credits exist
- premium = paid only
- "auth":
- true = requires API key / OAuth
- false = fully open without auth (rare; only include if certain)
- "category": "category name"


Quality filter:
- Exclude:
- vague “platform” listings without clear API endpoints

IMPORTANT= Please Do Not Ignore free open source APIs when you are searching, please add open source apis to the list if theres one, we do not have a limit that says you cant add anymore to the list and you have to ignore open source one, no , you can absolutely add open source apis if theres one.

Return the main result to me as proper json in json mode
"""
    return prompt

