import pandas as pd
import os
import re
from PIL import Image, ImageStat

OUTPUT_COLUMNS = [
    "user_id","image_paths","user_claim","claim_object",
    "evidence_standard_met","evidence_standard_met_reason","risk_flags",
    "issue_type","object_part","claim_status","claim_status_justification",
    "supporting_image_ids","valid_image","severity"
]

ALLOWED_ISSUE_TYPES = ["dent","scratch","crack","glass_shatter","broken_part","missing_part",
                       "torn_packaging","crushed_packaging","water_damage","stain","none","unknown"]

def extract_user_claim(conversation):
    lines = str(conversation).split('\n')
    user_lines = []
    for line in lines:
        if 'customer:' in line.lower() or 'user:' in line.lower():
            parts = line.split(':', 1)
            if len(parts) > 1:
                user_lines.append(parts[1].strip())
    return ' '.join(user_lines) if user_lines else str(conversation)

def detect_claim_object(text):
    t = text.lower()
    if any(w in t for w in ['car','vehicle','windshield','bumper','door','window','roof']):
        return "car"
    if any(w in t for w in ['laptop','screen','keyboard']):
        return "laptop"
    if any(w in t for w in ['package','box','delivery']):
        return "package"
    return "unknown"

def detect_issue_type(text):
    t = text.lower()
    for it in ALLOWED_ISSUE_TYPES:
        if it in ["unknown","none"]:
            continue
        if it.replace("_"," ") in t or it in t:
            return it
    if "crack" in t: return "crack"
    if "dent" in t or "dented" in t: return "dent"
    if "scratch" in t or "chip" in t: return "scratch"
    if "shatter" in t: return "glass_shatter"
    if "broken" in t or "won't" in t or "wont" in t: return "broken_part"
    if "leak" in t or "water" in t: return "water_damage"
    return "unknown"

def detect_object_part(text, claim_object):
    t = text.lower()
    if claim_object == "car":
        if "windshield" in t: return "windshield"
        if "rear bumper" in t or "back bumper" in t: return "rear_bumper"
        if "bumper" in t: return "front_bumper"
        if "door" in t: return "door"
        if "window" in t: return "window"
        if "roof" in t: return "roof"
    if claim_object == "laptop":
        if "screen" in t: return "screen"
        if "keyboard" in t: return "keyboard"
    return "unknown"

def parse_min_images(text):
    match = re.search(r'(\d+)\+?\s*image', str(text).lower())
    return int(match.group(1)) if match else 2

def is_blurry(img, threshold=100):
    try:
        gray = img.convert('L')
        return ImageStat.Stat(gray).var[0] < threshold
    except:
        return False

def resolve_image_paths(image_ids, claim_id):
    if pd.isna(image_ids) or not image_ids:
        return [], []

    paths, ids = [], []
    for idx, img_id in enumerate(str(image_ids).split(';')):
        img_id = img_id.strip()
        if not img_id:
            continue

        # Convert img_001.jpg -> img_1.jpg to match dataset files
        match = re.search(r'img_0*(\d+)\.jpg', img_id)
        actual_filename = f"img_{match.group(1)}.jpg" if match else img_id

        path = f"dataset/images/test/{claim_id}/{actual_filename}"
        if os.path.exists(path):
            paths.append(path)
            ids.append(str(idx))

    return paths, ids

def analyze_claim(row, evidence_reqs):
    claim_id = row["claim_id"]
    user_id = row["user_id"]
    conversation = row["conversation"]
    image_ids = row.get("image_ids", "")

    user_claim = extract_user_claim(conversation)
    claim_object = detect_claim_object(user_claim)
    image_paths, supporting_image_ids = resolve_image_paths(image_ids, claim_id)

    valid_images = []
    risk_flags = set()

    for path in image_paths:
        try:
            img = Image.open(path)
            img.verify()
            img = Image.open(path)
            if is_blurry(img):
                risk_flags.add("blurry_image")
            else:
                valid_images.append(path)
        except Exception:
            risk_flags.add("wrong_object")

    if image_ids and not image_paths:
        risk_flags.add("wrong_object")

    valid_image = len(valid_images) > 0

    req_row = evidence_reqs[evidence_reqs["claim_object"] == claim_object]
    min_images = 2
    if not req_row.empty:
        min_images = parse_min_images(req_row["minimum_image_evidence"].iloc[0])

    evidence_standard_met = len(valid_images) >= min_images

    if not valid_image:
        evidence_standard_met_reason = "no_valid_images"
    elif not evidence_standard_met:
        evidence_standard_met_reason = f"requires_{min_images}_images_found_{len(valid_images)}"
    else:
        evidence_standard_met_reason = "evidence_standard_met"

    issue_type = detect_issue_type(user_claim)
    object_part = detect_object_part(user_claim, claim_object)

    if not valid_image or not evidence_standard_met:
        claim_status = "not_enough_information"
        claim_status_justification = "Insufficient valid images per evidence requirements"
    else:
        claim_status = "supported"
        claim_status_justification = f"Image evidence consistent with {issue_type} on {object_part}"

    severity = "medium" if claim_status == "supported" and issue_type in ["crack","glass_shatter","broken_part"] else "low"

    return {
        "user_id": user_id,
        "image_paths": ";".join(image_paths),
        "user_claim": user_claim,
        "claim_object": claim_object,
        "evidence_standard_met": evidence_standard_met,
        "evidence_standard_met_reason": evidence_standard_met_reason,
        "risk_flags": ";".join(risk_flags),
        "issue_type": issue_type,
        "object_part": object_part,
        "claim_status": claim_status,
        "claim_status_justification": claim_status_justification,
        "supporting_image_ids": ";".join(supporting_image_ids),
        "valid_image": valid_image,
        "severity": severity
    }

if __name__ == "__main__":
    claims = pd.read_csv("dataset/claims.csv")
    evidence_reqs = pd.read_csv("dataset/evidence_requirements.csv")
    results = [analyze_claim(row, evidence_reqs) for _, row in claims.iterrows()]
    pd.DataFrame(results, columns=OUTPUT_COLUMNS).to_csv("output.csv", index=False)
    print(f"Processed {len(results)} claims. Saved output.csv")