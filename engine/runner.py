from scrape import callScrape
from incScript import callInc
from urlScript import callUrlScript
from cmpScript import callCmp

if __name__ == "__main__":
    print("Starting the data pipeline...")
    callScrape()  # Step 0: Scrape new data and save to inc.json
    print("Starting data processing...")
    callInc()  # Step 1: Process incoming data and merge with main dataset
    print("Data processing complete. Starting URL checks...")
    callUrlScript()  # Step 2: Check URL liveness and update statuses
    print("URL checks complete. Starting data compression...")
    callCmp()  # Step 3: Compress the dataset for storage/transmission
    print("Data compression complete. All tasks finished.")