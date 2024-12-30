from playwright.sync_api import sync_playwright
import time
import json

def execute_steps(steps):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        actions = {
            "goto": lambda url: page.goto(url),
            "click": lambda selector: page.click(selector),
            "type": lambda selector, text: page.fill(selector, text),
            "wait": lambda seconds: time.sleep(seconds),
            "title": lambda: print(page.title()),
            "source": lambda: print(page.content())
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

steps = json.loads(job_spec)
execute_steps(steps)