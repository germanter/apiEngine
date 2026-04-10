
import os
import json
import time
import re
from playwright.sync_api import sync_playwright, TimeoutError

def ask_perplexity(url: str, prompt: str):
    with sync_playwright() as p:
        # 1. POWERFUL CI/CD BROWSER LAUNCH
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage", # CRITICAL for GitHub Actions (prevents memory crashes)
                "--disable-blink-features=AutomationControlled", # Evasion tactic
                "--window-size=1920,1080"
            ]
        )
        
        # 2. ANTI-BOT CONTEXT SETUP
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1,
            has_touch=False,
            is_mobile=False
        )
        
        # Mask the WebDriver property to bypass basic bot protection
        context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        page = context.new_page()
        page.set_default_timeout(60000) # 60s timeout accommodates slower CI runners

        print("🌐 Navigating to Perplexity...")
        page.goto(url, wait_until="domcontentloaded")

        # 3. LOCATE INPUT (With Fallbacks & Debugging)
        print("🔍 Locating search input...")
        # Target the textarea dynamically in case they change IDs
        input_locator = page.locator('textarea[placeholder*="Ask"], #ask-input').first
        
        try:
            input_locator.wait_for(state="visible", timeout=15000)
        except TimeoutError:
            print("❌ ERROR: Could not find input box. Possible Cloudflare block or UI update.")
            page.screenshot(path="github_actions_error.png")
            print("📸 Saved error screenshot to github_actions_error.png (Upload this as a GHA Artifact to debug)")
            browser.close()
            return None

        # 4. ENTER PROMPT & SUBMIT
        print("✍️ Entering prompt...")
        input_locator.fill(prompt) # 'fill' is much faster and more reliable in CI than 'insert_text'
        page.wait_for_timeout(500) 
        
        print("🚀 Submitting...")
        input_locator.press("Enter")

        # 5. WAIT FOR RESPONSE WITH SMART POLLING
        answer_selector = ".prose, [data-testid='answer-text']"
        print("⏳ Waiting for AI to start generating...")
        
        try:
            page.wait_for_selector(answer_selector, state="visible", timeout=60000)
        except TimeoutError:
            print("❌ ERROR: AI never started generating.")
            page.screenshot(path="timeout_error.png")
            browser.close()
            return None

        print("🤖 AI is typing... Waiting for stabilization...")
        previous_text = ""
        stable_count = 0
        
        # Poll up to ~120 seconds to allow long responses
        for _ in range(120):
            page.wait_for_timeout(1000)
            current_text = page.locator(answer_selector).last.inner_text()
            
            if current_text and current_text == previous_text:
                stable_count += 1
            else:
                stable_count = 0
                previous_text = current_text
            
            # If text hasn't changed for 3 seconds, generation is done
            if stable_count >= 3:
                break

        print("✅ Generation complete.")
        page.wait_for_timeout(1000) # Let the UI finish any final DOM renders

        # 6. BULLETPROOF EXTRACTION (Bypassing the Clipboard entirely)
        # Why? Because headless Linux (GitHub Actions) often lacks a clipboard.
        print("📦 Extracting JSON payload from DOM...")
        extracted_json_text = None
        
        # Method A: Direct extraction from the code block (100x safer than clicking 'copy')
        code_blocks = page.locator("pre code")
        if code_blocks.count() > 0:
            print("✅ Found code block! Extracting text directly...")
            extracted_json_text = code_blocks.last.inner_text()
        else:
            print("⚠️ No UI code block found. AI might have messed up formatting. Attempting Regex Rescue...")
            # Method B: Regex extraction from raw text as a safety net
            full_text = page.locator(answer_selector).last.inner_text()
            
            # Look for standard markdown codeblocks
            match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', full_text, re.IGNORECASE)
            if match:
                extracted_json_text = match.group(1)
            else:
                # Look for raw JSON arrays or objects lying around
                match = re.search(r'(\[\s*\{[\s\S]*\}\s*\]|\{\s*"[\s\S]*\}\s*)', full_text)
                if match:
                    extracted_json_text = match.group(1)

        if not extracted_json_text:
            print("❌ ERROR: Could not extract JSON from the AI response.")
            page.screenshot(path="extraction_failed.png")
            browser.close()
            return None

        print("\n=== EXTRACTED JSON ===")
        print(extracted_json_text[:200] + "... [truncated for preview]")
        print("===================\n")
        
        browser.close()
        return extracted_json_text

# --- Execution logic remains exactly as you had it ---



def callScrape():
    url = "https://www.perplexity.ai/"
    from tools import get_prompt
    prompt = get_prompt()
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_path, "..", "incoming.json")

    extracted_text = ask_perplexity(url, prompt)

    if extracted_text:
        try:
            # Validate it's actual JSON
            parsed_json = json.loads(extracted_text)

            keys = [i.lower() for j in parsed_json for i in j.keys()]

            if "error" in keys or "invalid" in keys:
                raise ValueError("JSON data contains prohibited error/invalid keys.")
                
            
            # 'w' mode overwrites the file entirely
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(parsed_json, f, indent=4, ensure_ascii=False)
                
            print(f"✅ Successfully overwrote and saved JSON to: {os.path.abspath(json_path)}")
            
        except json.JSONDecodeError as e:
            print(f"⚠️ Warning: The extracted text is not perfectly valid JSON. Saving raw output for review. Error: {e}")
            with open(json_path + ".raw.txt", 'w', encoding='utf-8') as f:
                f.write(extracted_text)
    else:
        print("❌ Script aborted. See console for errors.")
