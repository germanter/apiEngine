import httpx as x
import asyncio
import json
import os

# This finds the file regardless of where the script is called from
base_path = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_path, "..", "saved2.json")
data = None
with open(json_path, "r") as file:
    data = json.load(file)

bigStein = asyncio.Semaphore(5) #bigStein stops the bad ones 

#this is a test version made by ai for base, we know everything about this codebase
async def check_url_liveness(client,url):
    async with bigStein:
        try:
            r = await client.head(url) #concurrent

            code = r.status_code

            if code < 300:
                return f"✅ ALIVE ({code})" # alive
            
            elif code == 405:
                return f"HEAD is not allowed (UNKNOWN) ({code})" #  - do not switch to get, respect the url

            elif code == 403:
                return "🛡️ ALIVE (Blocked / Protected)" # alive

            elif code == 404:
                return "💀 DEAD (404)" # dead

            elif code >= 500:
                return f"🤒 ALIVE (Server Error {code})" # alive

            else:
                return f"❓ UNKNOWN ({code})" # dead
            

        except x.TooManyRedirects:
            return url, "🔄 ALIVE (Redirect Loop)"
        
        except x.ReadTimeout:
            return url, "🕒 ALIVE (Read Timeout - Server connected but slow)"
        
        except x.ConnectError:
            return "❌ DEAD (No connection)" # dead  //serveraaaa

        except x.TimeoutException:
            return "🕒 TIMEOUT (Slow / Possibly alive)" # dead //user or server

        except x.RequestError as e:
            return f"⚠️ ERROR ({type(e).__name__})" # dead //user side

async def main():

    logs = []

    # headers = {  #prototype / failed for amazon final boss
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    # "Accept-Language": "en-US,en;q=0.5"
    # }

    async with x.AsyncClient(timeout=7.5, follow_redirects=True) as client:
        for i in data:
            logs.append({"name":i["name"],"status":check_url_liveness(client, i["url"])})

        res = await asyncio.gather(*logs)

        for i in res:
            print(i)

asyncio.run(main())

# checker = check_url_liveness("https://www.amazon.com/")
# print(checker)





