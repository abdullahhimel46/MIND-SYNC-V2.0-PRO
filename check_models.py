import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
url = "https://openrouter.ai/api/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}",
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        models = data.get("data", [])
        free_models = [m["id"] for m in models if ":free" in m["id"]]
        print("Available Free Models:")
        for m in free_models:
            print(m)
except Exception as e:
    print(f"Error: {e}")
