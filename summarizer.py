from transformers import pipeline, BartTokenizer


class TextSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.summarizer = pipeline("summarization", model=model_name)
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.max_length = 1024
        self.chunk_overlap = 50

    def chunk_text(self, text, max_tokens=800):
        tokens = self.tokenizer.encode(text)
        chunks = []
        for i in range(0, len(tokens), max_tokens - self.chunk_overlap):
            chunk_tokens = tokens[i:i + max_tokens]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append(chunk_text)
        return chunks

    def summarize(self, text, min_length=30, max_length=130):
        chunks = self.chunk_text(text)
        summaries = []
        for chunk in chunks:
            summary = self.summarizer(chunk, min_length=min_length, max_length=max_length, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        combined_summary = " ".join(summaries)
        return combined_summary
