# Damage Claim Verifier - Hackerrank

Multimodal insurance claim verification using Mistral Pixtral-12B-2409.

## Results on claims_1.csv
**44 claims processed**  
- Supported: 26 (59%)
- Contradicted: 14 (32%)
- Not enough information: 6 (14%)

Breakdown by object type:
- **Car**: 9 supported / 5 contradicted / 4 NEI
- **Laptop**: 5 supported / 6 contradicted / 2 NEI  
- **Package**: 10 supported / 3 contradicted / 0 NEI

## Approach
1. Multi-image reasoning - Parses semicolon separated paths, sends all images to Pixtral
2. Prompt injection defense - Ignores "approve this" instructions, flags potential_fraud
3. Evidence standards - Cars need wide+close shots, laptops need full device + screen
4. Edge case handling - Wrong object, blurry, missing angles = not_enough_information
5. Multilingual - Handles EN, ES, HI, ZH claims

## Usage
pip install mistralai pandas
export MISTRAL_API_KEY=your_key
python evaluate.py

Outputs results_claims_1.jsonl and submission.csv matching Hackerrank schema.
