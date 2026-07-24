# Claims Evidence Audit Agent

An audit safe tool that checks if a car damage claim has enough photo evidence before it reaches a human adjuster.

Built to prevent false fraud flags and reduce painful call center calls.

How it works:
Upload 1 photo = Not Enough Information, routed to human QA for follow up.
Upload 2 angles = Evidence Met, ready for adjuster.

Never auto denies for fraud. Logic is deterministic and fully auditable with 14 column CSV output.

Live demo: https://jrblaise-claims-audit.netlify.app/

Tech: HTML JavaScript deterministic rules engine Netlify
