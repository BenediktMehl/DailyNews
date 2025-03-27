from company_llm_summarizer import summarize_content_with_company_llm

def test_summarize_content():
    with open('src/buildPost/example_html_content.txt', 'r') as file:
        text = file.read()
    
    summary = summarize_content_with_company_llm(text)
    print("Original Text Length:", len(text))
    print("Summary Length:", len(summary))
    print("Summary:", summary)
    assert len(summary) < len(text)
    assert len(summary) > 100

def test_null_summary():
    nonsensical_text = "asdf qwer zxcv"
    summary = summarize_content_with_company_llm(nonsensical_text)
    print("Summary for nonsensical text:", summary)
    assert summary.lower() == "null"

if __name__ == "__main__":
    test_summarize_content()
    test_null_summary()
