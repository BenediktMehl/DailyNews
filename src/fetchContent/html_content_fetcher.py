from playwright.sync_api import sync_playwright
import logging
from time import sleep


def fetch_html_contents(topics, max_number_of_contents=3):
    contents = list()
    for item in topics:
        if len(contents) >= max_number_of_contents:
            break
        url = item['url']
        raw_text = _fetch_raw_text(url)
        logging.info(f"Fetch: Fetched raw text with {len(raw_text)} characters")
        if( len(raw_text) < 1000):
            logging.warning(f"Fetch: Raw text: {raw_text} is too short, skipping URL: {url}")
            continue
        cleaned_text = _clean_text(raw_text)
        content_item = {
            'title': item['title'],
            'url': url,
            'content': cleaned_text
        }
        contents.append(content_item)
    return contents


def _fetch_raw_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")
        page.goto(url)
        sleep(1)
        content = page.inner_text('body')
        browser.close()

        return content


def _clean_text(text):
    if text is None:
        return ""
    cleaned_text = ' '.join(text.split())
    return cleaned_text
