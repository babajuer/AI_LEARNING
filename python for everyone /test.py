from openai import OpenAI
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


from ollama import chat
response = chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": "为什么天空是蓝色的？"}
    ]
)
print(response.message.content)