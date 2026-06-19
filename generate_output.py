import pandas as pd

claims = pd.read_csv('dataset/claims.csv')
user_history = pd.read_csv('dataset/user_history.csv')

results = []

for idx, row in claims.iterrows():
    user_id = row['user_id']
    user_claim = str(row['user_claim']).lower()
    claim_object = row['claim_object']
    image_paths = str(row['image_paths'])

    supporting_images = []
    if pd.notna(image_paths) and image_paths!= 'nan':
        supporting_images = [p.strip() for p in image_paths.split(';') if p.strip()]

    if any(word in user_claim for word in ['not working', 'broken', 'failed', 'defect', 'malfunction']):
        status = 'approved'
        issue = 'functional_defect'
    elif any(word in user_claim for word in ['scratch', 'dent', 'crack', 'damage']):
        status = 'approved'
        issue = 'cosmetic_damage'
    elif any(word in user_claim for word in ['missing', 'lost', 'stolen']):
        status = 'rejected'
        issue = 'not_covered'
    else:
        status = 'pending'
        issue = 'unknown'

    user_rows = user_history[user_history['user_id'] == user_id]
    risk_flags = []
    if len(user_rows) > 0:
        if user_rows['past_claim_count'].iloc[0] > 2:
            risk_flags.append('repeat_claimer')
        if user_rows['rejected_claim'].iloc[0] > 0:
            risk_flags.append('prior_reject')
        if user_rows['manual_review_claim'].iloc[0] > 0:
            risk_flags.append('prior_manual_review')

    results.append({
        'claim_id': user_id,
        'claim_status': status,
        'issue_type': issue,
        'object_part': claim_object,
        'supporting_image_ids': ';'.join(supporting_images),
        'claim_status_justification': f'Object: {claim_object}, Claim: {user_claim[:100]}',
        'risk_flags': ';'.join(risk_flags) if risk_flags else 'none',
        'severity': 'medium'
    })

output_df = pd.DataFrame(results)
output_df.to_csv('output.csv', index=False)
print(f"Generated output.csv: {len(output_df)} rows")
print(f"First 3 claim_ids: {output_df['claim_id'].head(3).tolist()}")