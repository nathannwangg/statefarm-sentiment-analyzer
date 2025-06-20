from llama_cpp import Llama

llm = Llama(
    model_path="models/mistral.gguf",
    n_ctx=1024,
    n_threads=6,
    n_batch=32,
    verbose=False
)

def summarize_post(text: str) -> str:
    prompt = f"""You are an assistant summarizing Reddit posts about insurance companies.
Summarize this post in 1–2 sentences:\n\n{text}\n\nSummary:"""
    
    response = llm(prompt, max_tokens=150, stop=["\n"])
    return response['choices'][0]['text'].strip()