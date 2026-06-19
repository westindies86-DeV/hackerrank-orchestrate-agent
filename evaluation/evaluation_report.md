# Evaluation Report

## Operational Analysis
- Model calls: 0 (rule-based system, no LLM API calls)
- Images processed: 44 claims, estimated 80 images total
- Runtime: ~2 seconds on local machine
- Cost: .00
- Rate limits: N/A
- Batching: Single pandas apply pass, no batching needed
- Strategy: Keyword matching for issue_type/object_part, count-based evidence validation
