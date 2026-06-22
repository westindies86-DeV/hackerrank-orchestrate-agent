import os, json, base64
from pathlib import Path
from mistralai.client import MistralClient

client = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])

folder = Path("dataset/images/test/case_001")
img_files = list(folder.glob("*.jpg")) + list(folder.glob("*.png"))
print(f"Found {len(img_files)} images in case_001")

content = [{"type": "text", "text": "Analyze vehicle damage. Return ONLY JSON: {\"issue_type\": \"windshield_crack\", \"severity\": \"high\"}"}]

for img_path in img_files[:2]: # first 2 images only for speed
    print(f"Loading {img_path.name}")
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    content.append({"type": "image_url", "image_url": f"data:image/jpeg;base64,{b64}"})

print("Calling Pixtral...")
response = client.chat(model="pixtral-12b-2409", messages=[{"role": "user", "content": content}])
print("API Response:")
print(response.choices[0].message.content)