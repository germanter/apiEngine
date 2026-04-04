import httpx as x
import asyncio
import json
import os

# This finds the file regardless of where the script is called from
base_path = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_path, "..", "saved2.json")
main_path = os.path.join(base_path, "..", "api.json") #to save at end

data = None
with open(json_path, "r") as file:
    data = json.load(file)

bigStein = asyncio.Semaphore(5) #bigStein stops the bad ones 

#this is a test version made by ai for base, we know everything about this codebase
async def check_url_liveness(client,url):
    async with bigStein:
        try:
            # 200 - 399 alive 
            # 403 - we say alive because dead site cannot block
            # 405 - we say unknown because it says head is not allowed
            # 404 - dead
            # exclude 403, 405, 404 and from 400<= all dead

            r = await client.head(url) #concurrent

            code = r.status_code
            #we have zero care for nerdy urls
            if (200<= code <= 399) or code == 403:
                return "ALIVE"
            elif code == 405:
                return "UNKNOWN"
            elif code >= 400:
                return "DEAD"
            return "UNKNOWN"
            

        except x.HTTPError:  #we dont fuckin care for the reason, if its error = dead, gone
            return "DEAD"
        except Exception:
            return "DEAD"
        
def analyzeResults(report):
    total = len(report)
    if total == 0:
        return "\n--- SCAN REPORT ---\nNo URLs found to check.\n-------------------\n"
    
    alive = sum(1 for i in report if i["status"] == "ALIVE")
    dead  = sum(1 for i in report if i["status"] == "DEAD")
    unknown = sum(1 for i in report if i["status"] == "UNKNOWN")

    # The formatted report string
    stats = (
        f"\n--- SCAN REPORT ---\n"
        f"Total Checked: {total}\n"
        f"✅ Alive: {alive} ({alive/total*100:.1f}%)\n"
        f"💀 Dead: {dead} ({dead/total*100:.1f}%)\n"
        f"❓ Unknown: {unknown} ({unknown/total*100:.1f}%)\n"
        f"-------------------\n"
    )
    return stats

async def main():

    promisedTasks = []
    reportList = [] 

    # headers = {  #prototype / failed for amazon final boss
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    # "Accept-Language": "en-US,en;q=0.5"
    # }

    async with x.AsyncClient(timeout=7.5, follow_redirects=True) as client:
        for i in data:
            promisedTasks.append(check_url_liveness(client, i["url"]))

        res = await asyncio.gather(*promisedTasks)

        for item, status in zip(data, res):
            print(f"{item['name']} - {item['url']} - {status}")
            reportList.append({"name": item["name"], "url": item["url"], "status": status}) 
            item["status"] = status #the legendary move, the proof of ai and human have to work together, this is a motto
        
        print(analyzeResults(reportList))
        with open(main_path, "w") as file:
            json.dump(data, file, indent=4)

asyncio.run(main())

# checker = check_url_liveness("https://www.amazon.com/")
# print(checker)





