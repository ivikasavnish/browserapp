from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import random
import time

def clean_html(html_content: str) -> str:
    """Clean HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup(['script', 'style', 'meta', 'link', 'noscript']):
        element.decompose()
    return soup.get_text(separator=' ', strip=True)

def wait_for_selector_with_retry(page, selector, retries=3, timeout=10000):
    """Wait for a selector with retries."""
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}: Waiting for {selector}")
            return page.wait_for_selector(selector, timeout=timeout)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                raise

def search_google_and_extract(keyword, headless=False):
    """Search Google and extract cleaned results."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        try:
            # Navigate to Google and perform search
            search_url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}"
            print("Navigating to Google...")
            page.goto(search_url, wait_until="networkidle")

            # Wait for search results
            print("Waiting for search results...")
            wait_for_selector_with_retry(page, 'div.g')

            # Extract first result
            results = page.query_selector_all('div.g a')
            if not results:
                raise Exception("No results found.")
            
            first_result_url = results[0].get_attribute('href')
            print(f"First result URL: {first_result_url}")

            # Visit the first result
            # page.goto(first_result_url, wait_until="networkidle")
            time.sleep(random.uniform(2, 5))
            cleaned_content = clean_html(page.content())
            return cleaned_content

        finally:
            browser.close()

# Example usage
if __name__ == "__main__":
    try:
        keyword = "latest python developer"
        content = search_google_and_extract(keyword, headless=False)
        print("\nCleaned Content:\n", content)
    except Exception as e:
        print(f"Error: {e}")
