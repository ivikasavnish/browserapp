from playwright.sync_api import sync_playwright
import time
import json
import os 
from dotenv import load_dotenv
import random
load_dotenv()
def execute_steps(steps):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        actions = {
            "goto": lambda url: page.goto(url),
            "click": lambda selector: page.click(selector),
            "type": lambda selector, text: page.fill(selector, text),
            "wait": lambda seconds: time.sleep(seconds),
            "title": lambda:  (page.title()),
            "source": lambda:  page.content(),
        }
        
        for step in steps:
            action = step.get("action")
            args = step.get("args", [])
            if action in actions:
                actions[action](*args)
        
        browser.close()

# Example JSON job specification
job_spec = '''
[
    {"action": "goto", "args": ["http://playwright.dev"]},
    {"action": "wait", "args": [5]},
    {"action": "title"},
    {"action": "source"}
]
'''

# steps = json.loads(job_spec)
# execute_steps(steps)
config = {
    "api_key": "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",
    "model": "gpt-3.5-turbo"
}
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
config = {
    "api_key": "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",
    "model": "gpt-3.5-turbo"
}
client = OpenAI(
    api_key=config["api_key"]
)

# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {
#             "role": "user",
#             "content": "Write a haiku about recursion in programming."
#         }
#     ]
# )
from lmapi import LLMFactory
class AiScraper():
    def __init__(self,domain:str,plan_file:str):
        self.steps = []
        self.domain = domain
        self.ai_helper =   LLMFactory.create_provider("openai",config)
        self.driver = sync_playwright().start()
    def find_menu(self):
        pass

    def find_links(self):
        pass

    def find_entities(self):
        pass

    def find_home(self):

        pass

    def search(self, domain: str):
        
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                
            )
            context = browser.new_context(
             
                java_script_enabled=False  # Disable JavaScript
            )
            page = context.new_page()

            # Block unnecessary resources
            page.route("**/*.{png,jpg,jpeg,gif,svg,css,woff,woff2}", lambda route: route.abort())
            page.route("**/{analytics,gtm,adsense,doubleclick}**", lambda route: route.abort())
            
            search_params = {
                "q": f"{domain} {random.choice(['official', 'website', 'homepage'])}",
                "hl": "en",
                "strip": "1",  # Request basic version
                "nfpr": "1"    # No search corrections
            }

            try:
                time.sleep(random.uniform(2, 5))
                context.clear_cookies()
                
                search_url = "https://www.google.com/search?" + "&".join([f"{k}={v}" for k,v in search_params.items()])
                response = page.goto(search_url, wait_until='domcontentloaded')
                
                # Get clean HTML
                html_content = response.text()
                
                # Basic HTML cleaning (optional)
                html_content = (html_content
                    .replace('javascript:', '')
                    .replace('onclick=', '')
                    .replace('onload=', '')
                )
                
                return html_content
                
            except Exception as e:
                print(f"Search error: {e}")
            finally:
                context.close()
                browser.close()


class AiTester():
    def __init__(self,plan_file:str):
        self.scraper = AiScraper()
        self.plan_file = plan_file
    def test(self):
        self.scraper.add_step("goto", "http://playwright.dev")
        self.scraper.add_step("wait", 5)
        self.scraper.add_step("title")
        self.scraper.add_step("source")
        self.scraper.execute()
from scrapper import search_google_and_extract 
from lmapi import OpenAIProvider
llmprovider = OpenAIProvider("openai",config)
import logging
import logging.handlers
from datetime import datetime
import os

class CustomLogger:
    def __init__(self, name='browser_automation'):
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)
        
        # Setup logger
        self.logger = logging.getLogger(name)
logger = CustomLogger().logger
import sys
from openapisvc import find_best_match
if __name__ == "__main__":
    keyword = sys.argv[1]
    print(llmprovider.__dict__)
    urls  = search_google_and_extract(keyword)
    result = find_best_match(urls,keyword)
    print(result)

