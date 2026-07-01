## Why #1,678 Matters

Most AI demos fail when images are blurry, evidence conflicts, or users lie.

This system ranked #1,678/1,773 in the Orchestrate Agent Hackathon because it processed REAL damage claims: stock photos passed off as incident photos, user history that contradicted claims, and "lacks enough information" edge cases that kill CSAT and trigger audits.

Top 50 submissions used clean tutorial data. This used messy customer data.

**Result:** Rebuilt as a multi-modal evidence review system with human QA gates. Zero findings > leaderboard scores.

**If you hire for Kaggle scores, skip this repo.**  
**If you hire for production reality + audit compliance, clone it.**

---

# HackerRank Orchestrate – Insurance Claim Assessment Agent

A deterministic claim verification system built for regulated industries.

Evaluates insurance claims using structured data + image evidence, routing "insufficient evidence" cases to human QA with severity scores and justifications. Designed for BtoC scale.

## Problem This Solves

Real claims fail when:
* Photos are blurry, dark, or stock images
* User claim text conflicts with visual evidence  
* Evidence is missing → AI can't auto-deny without audit risk
* CS teams need justifications for every decision

## Approach

* **Multi-Modal Evidence Review**: Extract claim → Inspect images → Flag quality/authenticity risks
* **Human QA Routing**: "Lacks enough information" cases output severity + justification for manual review
* **Audit-Ready CSV**: 14-column schema matching compliance requirements. Every decision has a receipt.
* **Deterministic Pipeline**: Python 3.11 stdlib only. No LLM hallucinations in final assessment.

## Tech Stack

* **Core**: Python 3.11 standard library
* **AI Components Used**: Mistral + Meta for evidence extraction, not final decisions
* **Output**: HackerRank-compatible CSV with severity, justification, and QA flags

## Why Rule-Based?

When a denied claim goes to legal, "the LLM felt uncertain" doesn't hold up.  
"Flagged for human review: blurry_image + severity_3 + prior_claim_conflict" does.

This is built for compliance, not demos.

## Output Schema

Generates 14-column CSV matching HackerRank evaluation + adds internal QA fields for severity and justification.

---

**Defended this system to an AI Judge for 30min on camera.**  
**Ask me about failure modes, evaluation workflows, or building for audit risk.**
