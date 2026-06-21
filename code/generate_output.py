import pandas as pd

claims = pd.read_csv('dataset/claims.csv')
history = pd.read_csv('dataset/user_history.csv')

def extract_issue_type(conversation):
    conv = str(conversation).lower()
    if 'stone' in conv or 'windshield' in conv or 'glass' in conv or 'crack' in conv:
        return 'cosmetic_damage'
    if 'leak' in conv or 'water' in conv or 'flood' in conv:
        return 'water_damage'
    if 'dent' in conv or 'dented' in conv or 'bumper' in conv or 'collision' in conv:
        return 'collision_damage'
    return 'unknown'

def extract_object_part(conversation):
    conv = str(conversation).lower()
    if 'windshield' in conv or 'glass' in conv:
        return 'windshield'
    if 'bumper' in conv:
        return 'bumper'
    if 'roof' in conv:
        return 'roof'
    if 'window' in conv:
        return 'window'
    return 'unknown'

def get_risk_flags(user_id):
    user_rows = history[history['user_id'] == user_id]
    flags = []
    if (user_rows['previous_claims_count'] > 1).any():
        flags.append('repeat_claimer')
    if (user_rows['previous_claim_status'] == 'rejected').any():
        flags.append('prior_reject')
    return ';'.join(flags)

output_rows = []
for idx, row in claims.iterrows():
    conversation = row['conversation']
    user_id = row['user_id']
    issue_type = extract_issue_type(conversation)
    object_part = extract_object_part(conversation)
    risk_flags = get_risk_flags(user_id)
    
    if issue_type == 'unknown':
        status = 'rejected'
        justification = 'Insufficient evidence'
        severity = 'low'
    else:
        status = 'approved'
        justification = f'Validated {issue_type} on {object_part}'
        severity = 'medium' if risk_flags else 'low'

    output_rows.append({
        'claim_id': row['claim_id'],
        'status': status,
        'issue_type': issue_type,
        'object_part': object_part,
        'risk_flags': risk_flags,
        'severity': severity,
        'claim_status_justification': justification,
        'supporting_image_ids': row.get('image_ids', '')
    })

pd.DataFrame(output_rows).to_csv('output.csv', index=False)
print(f"Generated output.csv: {len(output_rows)} rows")
