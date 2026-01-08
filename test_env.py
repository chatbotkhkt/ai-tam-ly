from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

if key:
    print("✅ ĐÃ ĐỌC ĐƯỢC API KEY")
    print("Key bắt đầu bằng:", key[:5], "*****")
else:
    print("❌ KHÔNG ĐỌC ĐƯỢC API KEY")
