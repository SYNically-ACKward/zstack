---
description: "Implement AI/ML security controls for prompt inspection, shadow AI discovery, and LLM data leakage prevention"
---

**AI Security Officer** | Zscaler Zero Trust Exchange | GenAI Risk Lead

Control employee use of Large Language Models (ChatGPT, Claude, Copilot, LLaMA) to prevent credential leakage, intellectual property theft, and unauthorized SaaS adoption.

## When to use

- Preventing employees from pasting confidential documents into ChatGPT and other public LLMs
- Discovering shadow AI tool usage (unauthorized ChatGPT accounts, side-loaded models, ollama deployments)
- Blocking prompt injections and jailbreak attempts in enterprise GenAI deployments
- Monitoring approved GenAI tools (GitHub Copilot, Microsoft Copilot Pro, Claude Enterprise) for misuse
- Enforcing data classification in LLM interactions (no confidential data to public models)
- Detecting policy violations (PII sent to unauthorized LLM, source code uploaded to public AI)
- Meeting regulatory requirements (GDPR prohibits training LLMs on customer data, HIPAA requires data residency)

## 5-Gate Artifacts

1. **AI Tool Inventory & Approval Matrix** - Public LLMs (ChatGPT, Claude, Gemini—blocked by default), enterprise-safe tools (Copilot Enterprise, internal fine-tuned models—approved), evaluation tier (allowed for specific teams with logging and data segregation), data residency requirements per tool

2. **Prompt Inspection Rules** - Detect credential patterns (API keys, passwords in prompts), confidential markers (marked as "Confidential", "Internal Only"), customer data (PII, financial records, medical records), source code snippets (full files, repos), regulatory data (HIPAA, PCI, credit card numbers)

3. **Shadow AI Detection Heuristics** - Identify proxy services (OpenAI API via third-party wrappers, tunneling), browser-based model inference (Ollama, LLaMA local, ComfyUI), plugin-based LLMs, unusual API patterns to model endpoints, DNS exfiltration attempts

4. **LLM Response Monitoring** - Detect if model response contains suspicious content (injected credentials from training data, copyrighted text, memorized training data), model behavior changes (response quality degradation, refusal to comply with policy)

5. **Approved LLM Policy Framework** - Enterprise Copilot configuration (tenant lock to specific org, data residency in US only, retention 30 days), GitHub Copilot usage (enterprise account required, no public code snippets, internal repos only), auditing + logging per HIPAA/SOC2

## Key Configuration

- **Prompt Sanitization**: Strip credentials, PII, and confidential markers before LLM request; log original prompt for audit; implement redaction masks for sensitive field types

- **Response Inspection**: Check LLM responses for trained data leakage (verbatim training data output), copyrighted content (book excerpts, song lyrics), injected malicious code, model jailbreak attempt indicators

- **Model Endpoint Whitelisting**: Allow only approved LLM APIs (OpenAI official endpoint, Azure OpenAI, internal Hugging Face); block proxy services and side-loaded models; enforce mTLS for enterprise LLMs

- **Session-Level Controls**: Limit per-user daily token usage to <100K tokens; flag high-volume users (potential data ingestion attack); implement rate limiting by department to prevent resource exhaustion

- **Integration with DLP**: Trigger DLP block if prompt contains sensitive data before reaching LLM; log incident for audit trail; correlate with other data exfiltration indicators

- **User Feedback Loop**: Track user appeals of AI Guard blocks; measure false positive rate and fine-tune rules quarterly; implement appeal process with manager approval for edge cases

## Gotchas

- Prompt inspection with regex/ML model classifiers creates performance overhead (100-500ms per prompt); use sampling (1-in-10 prompts) initially; monitor latency impact on user experience

- LLM jailbreak techniques bypass keyword filters (homoglyphs, encoding, indirect references like "write SSN as N: 123-45-6789"); combine pattern matching with semantic inspection; update rules monthly based on new attacks

- Blocking all public LLMs creates user frustration and shadow AI workarounds (personal accounts, home VPN); establish approved tier with clear policies and business case; measure shadow AI usage quarterly

- Fine-tuned internal LLMs on proprietary data create new attack surface (model inversion attacks can recover training data); don't train on unencrypted sensitive data; implement data governance for training datasets

- LLM responses may contain copyrighted material (book excerpts, song lyrics, code from training data); need legal review before compliance claims; implement response-level content filtering

- Session termination for policy violations unclear—do you block current session, revoke API token, or alert user? Define escalation path per violation severity; blocking too aggressive destroys productivity

- Approved LLM endpoint can be compromised (Azure OpenAI access key leaked); rotate credentials quarterly and monitor for unusual usage patterns; implement IP whitelisting for data-sensitive operations
