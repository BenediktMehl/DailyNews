from src.fetchContent.ai_generate_topics import create_news_topic
import unittest


class TestCreateNewsSummary(unittest.TestCase):
    def test_summarize_content(self):
        with open('src/buildPost/example_html_content.txt', 'r') as file:
            text = file.read()

        summary = create_news_topic(text)
        print("Original Text Length:", len(text))
        print("Summary:", summary)

        # Assertions
        self.assertIsNotNone(summary, "Summary should not be None for valid input")
        self.assertIsInstance(summary, dict, "Summary should be a dictionary")
        self.assertIn("headline", summary, "Summary should contain a 'headline'")
        self.assertIn("entry_sentence", summary, "Summary should contain an 'entry_sentence'")
        self.assertIn("detail", summary, "Summary should contain a 'detail'")
        self.assertGreater(len(summary["headline"]), 0, "Headline should not be empty")
        self.assertGreater(len(summary["entry_sentence"]), 0, "Entry sentence should not be empty")
        self.assertGreater(len(summary["detail"]), 0, "Detail should not be empty")

    def test_null_summary(self):
        nonsensical_text = "asdf qwer zxcv"
        summary = create_news_topic(nonsensical_text)
        print("Summary for nonsensical text:", summary)

        # Assertions
        self.assertIsNone(summary, "Summary should be None for nonsensical input")

    def test_empty_input(self):
        empty_text = ""
        summary = create_news_topic(empty_text)
        print("Summary for empty text:", summary)

        # Assertions
        self.assertIsNone(summary, "Summary should be None for empty input")

    def test_partial_fields(self):
        partial_text = "This is a partial text that might not generate all fields."
        summary = create_news_topic(partial_text)
        print("Summary for partial text:", summary)

        # Assertions
        if summary is not None:
            self.assertIn("headline", summary, "Summary should contain a 'headline' if valid")
            self.assertIn("entry_sentence", summary, "Summary should contain an 'entry_sentence' if valid")
            self.assertIn("detail", summary, "Summary should contain a 'detail' if valid")


if __name__ == "__main__":
    unittest.main()
