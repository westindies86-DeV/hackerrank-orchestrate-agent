import os, csv, json, base64
from pathlib import Path
from mistralai.client import MistralClient

def main():
    client = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])

    test_dir = Path("dataset/images/test")
    case_folders = sorted([d for d in test_dir.iterdir() if d.is_dir() and d.name.startswith("case_")])
    print(f"Found {len(case_folders)} cases to process")

    all_results = []

    for idx, folder in enumerate(case_folders, 1):
        case_name = folder.name
        print(f"[{idx}/{len(case_folders)}] Processing {case_name}")

        img_files = list(folder.glob("*.jpg")) + list(folder.glob("*.png")) + list(folder.glob("*.jpeg"))

        if not img_files:
            result = {
                "evidence_standard_met": "False",
                "evidence_standard_met_reason": "No images provided",
                "risk_flags": "no_image",
                "issue_type": "unknown",
                "object_part": "unknown",
                "claim_status": "rejected",
                "claim_status_justification": "No evidence provided",
                "supporting_image_ids": "",
                "valid_image": "False",
                "severity": "unknown"
            }
            all_results.append(result)
            continue

        content = [{
            "type": "text",
            "text": "Analyze vehicle damage images. Return ONLY valid JSON with no other text. Required format: {\"evidence_standard_met\": \"True/False\", \"evidence_standard_met_reason\": \"reason\", \"risk_flags\": \"none/fraud_risk\", \"issue_type\": \"windshield_crack/dent/scratch/broken_lamp/other\", \"object_part\": \"front_windshield/rear_bumper/hood/door/other\", \"claim_status\": \"approved/rejected/needs_review\", \"claim_status_justification\": \"reason\", \"valid_image\": \"True/False\", \"severity\": \"low/medium/high\"}"
        }]

        for img_path in img_files[:3]:
            with open(img_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            content.append({
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{b64}"
            })

        try:
            response = client.chat(
                model="pixtral-12b-2409",
                messages=[{"role": "user", "content": content}]
            )

            result_text = response.choices[0].message.content.strip()

            brace_count = 0
            start_idx = -1
            for i, char in enumerate(result_text):
                if char == '{':
                    if start_idx == -1:
                        start_idx = i
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0 and start_idx!= -1:
                        json_str = result_text[start_idx:i+1]
                        result = json.loads(json_str)
                        break
            else:
                raise ValueError("No valid JSON block found")

            result["supporting_image_ids"] = ",".join([i.name for i in img_files])
            print(f" -> {result.get('claim_status','unknown')} | {result.get('issue_type','unknown')} | {result.get('severity','unknown')}")

        except Exception as e:
            print(f" -> ERROR: {type(e).__name__}: {str(e)[:100]}")
            result = {
                "evidence_standard_met": "False",
                "evidence_standard_met_reason": "Parsing failed",
                "risk_flags": "processing_error",
                "issue_type": "unknown",
                "object_part": "unknown",
                "claim_status": "needs_review",
                "claim_status_justification": "Could not parse model output",
                "supporting_image_ids": ",".join([i.name for i in img_files]),
                "valid_image": "False",
                "severity": "unknown"
            }

        all_results.append(result)

    columns = ["evidence_standard_met","evidence_standard_met_reason","risk_flags",
               "issue_type","object_part","claim_status","claim_status_justification",
               "supporting_image_ids","valid_image","severity"]

    with open("output.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"\nDone. Wrote {len(all_results)} results to output.csv")

if __name__ == "__main__":
    main()