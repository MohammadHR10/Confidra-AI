#!/usr/bin/env python3
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test the Friendli API key
client = OpenAI(
    api_key=os.getenv("FRIENDLI_TOKEN"),
    base_url="https://api.friendli.ai/serverless/v1",
)

try:
    print("Testing Friendli API key...")
    print(f"API Key (first 20 chars): {os.getenv('FRIENDLI_TOKEN')[:20]}...")
    
    completion = client.chat.completions.create(
        model="meta-llama-3.1-8b-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"},
        ],
        stream=False,
    )
    print("✅ SUCCESS!")
    print(f"Response: {completion.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    print(f"Error type: {type(e).__name__}")
