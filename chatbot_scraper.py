import requests
from bs4 import BeautifulSoup

# Replace with your Hugging Face API token
HF_API_TOKEN = "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"

# Step 1: Scrape website content
def fetch_website_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove scripts and styles
    for script in soup(["script", "style", "noscript"]):
        script.decompose()

    text = soup.get_text(separator=" ")
    return " ".join(text.split())

# Step 2: Load website content
website_url = "https://www.flipkart.com/"
website_content = fetch_website_text(website_url)

# Step 3: Chat with Hugging Face model
def chat_with_huggingface(user_input, context):
    prompt = f"""
You are a helpful chatbot trained using the following website information:

{context}

Now answer this user question:
User: {user_input}
Chatbot:"""

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7
        }
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json()[0]["generated_text"].split("Chatbot:")[-1].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Step 4: Run console chatbot
def run_chatbot():
    print("🤖 BotPenguin Chatbot (via Hugging Face)")
    print("Ask anything about BotPenguin. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        reply = chat_with_huggingface(user_input, website_content[:3000])  # Truncate to avoid token limit
        print(f"Chatbot: {reply}\n")

if __name__ == "__main__":
    run_chatbot()
