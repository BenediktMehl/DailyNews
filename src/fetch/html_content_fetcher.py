from playwright.sync_api import sync_playwright


class HTMLContentFetcher:
    def get_html_content(self, url):
        raw_text = self._fetch_raw_text(url)
        return self._clean_text(raw_text)

    def _fetch_raw_text(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
            page.goto(url)
            content = page.inner_text('body')
            browser.close()

            return content

    def _clean_text(self, text):
        if text is None:
            return ""
        # Remove extra whitespace and newlines
        cleaned_text = ' '.join(text.split())
        return cleaned_text
