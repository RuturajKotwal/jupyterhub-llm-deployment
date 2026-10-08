import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

token = os.getenv("JUPYTERHUB_API_TOKEN")
ollama_base_url = os.getenv("OLLAMA_BASE_URL")

client = OpenAI(
    base_url=ollama_base_url,
    api_key=token,
    default_headers={"Authorization": f"token {token}"},
    timeout=300,
)

stream = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[
        {
            "role": "user",
            "content": "Tell me capital of Germany.",
        }
    ],
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)

print()