from playwright.sync_api import sync_playwright
import logging


def fetch_html_contents(news_items):
    contents = list()
    for url, _ in news_items:
        raw_text = _fetch_raw_text(url)
        logging.info(f"Fetch: Fetched raw text: {raw_text}")
        contents.append(_clean_text(raw_text))
    return contents


def _fetch_raw_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        page.goto(url)
        content = page.inner_text('body')
        browser.close()

        return content


def _clean_text(text):
    if text is None:
        return ""
    cleaned_text = ' '.join(text.split())
    return cleaned_text
