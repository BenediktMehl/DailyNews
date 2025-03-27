from company_llm_summarizer import summarize_content_with_company_llm

def test_summarize_content():
    with open('src/build/example_html_content.txt', 'r') as file:
        text = file.read()
    
    summary = summarize_content_with_company_llm(text)
    print("Original Text Length:", len(text))
    print("Summary Length:", len(summary))
    print("Summary:", summary)

if __name__ == "__main__":
    test_summarize_content()
