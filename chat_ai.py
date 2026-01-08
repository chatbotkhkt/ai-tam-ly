from openai import OpenAI
from dotenv import load_dotenv
import os
from prompt import SYSTEM_PROMPT

# Load biến môi trường từ .env
load_dotenv()

# Tạo client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("🤖 AI TƯ VẤN TÂM LÝ (gõ 'exit' để thoát)")
print("-" * 40)

while True:
    user_input = input("👤 Bạn: ")

    if user_input.lower() == "exit":
        print("👋 Tạm biệt!")
        break

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )

    ai_reply = response.choices[0].message.content
    print("\n🤖 AI:", ai_reply)
    print("-" * 40)
