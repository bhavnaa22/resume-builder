#!/usr/bin/env python3
import os
import sys

print("Step 1: Checking environment...")
api_key = os.environ.get('GEMINI_API_KEY')
print(f"API Key from env: {api_key[:15] if api_key else 'NOT FOUND'}...")

print("\nStep 2: Loading dotenv...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    print(f"API Key after dotenv: {api_key[:15] if api_key else 'NOT FOUND'}...")
except Exception as e:
    print(f"dotenv error: {e}")

print("\nStep 3: Importing google.generativeai...")
try:
    import google.generativeai as genai
    print("✓ Import successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

print("\nStep 4: Configuring API...")
try:
    genai.configure(api_key=api_key)
    print("✓ Configuration successful")
except Exception as e:
    print(f"✗ Configuration failed: {e}")
    sys.exit(1)

print("\nStep 5: Listing models...")
try:
    models = list(genai.list_models())
    print(f"Found {len(models)} models")
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
except Exception as e:
    print(f"✗ List models failed: {e}")

print("\nStep 6: Testing generation...")
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Hello!")
    print(f"✓ Success: {response.text}")
except Exception as e:
    print(f"✗ Generation failed: {e}")

print("\nDone!")
