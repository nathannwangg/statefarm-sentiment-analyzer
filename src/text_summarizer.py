import google.generativeai as genai
import random
from dotenv import load_dotenv
import os

# Set up Gemini API key and load model
load_dotenv()
# API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel("gemini-2.0-flash")


def summarize_post(title, body):
    prompt = f"""You are a social media manager for a large enterprise. Summarize the following Reddit post in 3 sentences.
    
    Title: {title}
    
    Body: {body}
    """
    response = model.generate_content(prompt)
    return response.text.strip()


def summarize_comments(comments: list[str]) -> str:
    # If more than 50 comments, randomly sample 50
    if len(comments) > 50:
        sampled_comments = random.sample(comments, 50)
    else:
        sampled_comments = comments

    comments_text = "\n".join(sampled_comments)

    prompt = f"""
    You are a social media manager for State Farm. Summarize the following comments to a Reddit post in 3 sentences, focusing specifically on sentiment towards State Farm.
    Comments: {comments_text}
    """
    response = model.generate_content(prompt)
    return response.text.strip()


