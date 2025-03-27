from transformers import pipeline

def summarize_content(text: str) -> str:
    if not text.strip():
        return text
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']
