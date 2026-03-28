---
description: "Query Zscaler best practices from a curated knowledge base backed by ChromaDB vector embeddings. Use this skill whenever the user asks about Zscaler best practices, recommended configurations, deployment guidance, troubleshooting patterns, or 'what does Zscaler recommend for X'. Also trigger when the user says 'check best practices', 'look up the KB', 'search the knowledge base', or references the HuggingFace QA app."
---

**Zscaler Best Practices Advisor** | Vector Knowledge Base | ChromaDB RAG

Answer Zscaler best-practice questions by querying a curated knowledge base hosted on HuggingFace Spaces. The knowledge base contains vectorized Zscaler documentation, deployment guides, and field-proven configurations indexed in ChromaDB. Always query the KB first, then layer your own expertise on top of the retrieved context.

## When to use

- User asks "what is the best practice for ..." anything Zscaler-related
- Deployment guidance questions (ZIA, ZPA, ZDX, ZCC, ZTB, DLP, CASB, etc.)
- Troubleshooting patterns and recommended diagnostic steps
- Configuration validation ("is this the right way to set up ...")
- Pre-engagement research to ground recommendations in official guidance
- Cross-referencing your own skill output against the knowledge base
- Any time you want to augment a ZStack skill's output with authoritative references

## How it works

The knowledge base is a Gradio app at `https://pganti-zscaler-best-practices-qa.hf.space`. It accepts a natural language question, searches ChromaDB vector embeddings of Zscaler best-practice documents, and returns relevant passages with source attribution.

## Querying the Knowledge Base

Use the bundled script to query:

```bash
python3 <skill-dir>/scripts/query_kb.py "your question here"
```

Or call the API directly with curl:

```bash
curl -s -X POST \
  https://pganti-zscaler-best-practices-qa.hf.space/run/predict \
  -H "Content-Type: application/json" \
  -d '{"data": ["What is the best practice for ZPA connector placement?"]}' \
  | python3 -c "import sys,json; r=json.load(sys.stdin); print(r.get('data',['No response'])[0])"
```

If `/run/predict` returns an error, try the streaming endpoint:

```bash
# Step 1: Initiate the call
EVENT_ID=$(curl -s -X POST \
  https://pganti-zscaler-best-practices-qa.hf.space/call/predict \
  -H "Content-Type: application/json" \
  -d '{"data": ["your question"]}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['event_id'])")

# Step 2: Fetch the result
curl -s "https://pganti-zscaler-best-practices-qa.hf.space/call/predict/$EVENT_ID"
```

## Response Handling

The KB returns text that typically includes:
- **Retrieved passages** from Zscaler documentation
- **Source references** indicating which documents were matched
- **Confidence context** based on vector similarity

When presenting results to the user:

1. **Lead with the KB answer** - Show what the knowledge base returned as the authoritative source
2. **Augment with expertise** - Add practical context, gotchas, and field experience from your ZStack skills
3. **Flag gaps** - If the KB doesn't have a strong answer, say so and provide your best guidance with a note that it's not from the curated KB
4. **Cite sources** - When the KB response includes document references, pass them through

## Integration with Other Skills

This skill pairs well with every other ZStack skill. Use it to:

- **Validate designs**: After running `zia-policy` or `zpa-connectors`, query the KB to confirm alignment with official best practices
- **Enrich proposals**: Before generating a `ps-proposal` or `ps-sow`, pull relevant best practices to include as references
- **Support migrations**: Query migration-specific best practices when running `migrate-palo-alto`, `migrate-checkpoint`, etc.
- **Troubleshoot**: When a deployment hits issues, query the KB before diving into manual diagnosis

Example chaining:
```
User: "Design ZPA for our AWS environment"
1. Query KB: "ZPA best practices for AWS connector deployment"
2. Run zpa-connectors skill with KB context
3. Validate output against KB recommendations
```

## Gotchas

- The HuggingFace Space may cold-start after inactivity (30-60s delay on first query) - if the first call times out, retry once
- The KB is curated from official Zscaler documentation and field guides - it may not cover bleeding-edge features released in the last few weeks
- Vector search returns the closest semantic matches, not exact keyword matches - phrase questions naturally rather than using keyword queries
- If the space is down or unreachable, fall back to your built-in ZStack expertise and note that KB validation was unavailable
- Rate limit: be reasonable with queries (no more than 5-10 per engagement session)
