# HackerRank Orchestrate – Insurance Claim Assessment Agent

A deterministic rule-based claim verification system built for the HackerRank Orchestrate Hackathon.

The solution evaluates insurance claims and generates schema-compliant assessments using structured claim information and evidence requirements.

## Features

* Rule-based claim classification
* Deterministic output generation
* Handles missing image directories gracefully
* Maintains 1:1 mapping between input claims and output records
* Python 3.11 standard library only
* Produces HackerRank-compatible CSV output

## Approach

* Keyword-based classification for issue type, object part, and severity
* Validation of claim inputs and evidence structure
* Consistent output formatting for all records
* Fallback handling for incomplete or missing data

## Output

Generates a 14-column CSV matching the HackerRank evaluation schema.
