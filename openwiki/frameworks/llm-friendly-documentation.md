---
type: methodology
title: LLM-Friendly Documentation Framework
description: A 12-principle framework for writing documentation that an LLM can consume without inference gaps — covering explicitness, state separation, glossaries, constraints, ADRs, document layering, and a verification loop — proposed as the starting methodology for this research session.
tags: [methodology, documentation, hallucination, llm, framework]
verified:
  - by: openwiki/0.4.3
    at: 2026-09-05T20:17:03.290Z
sources:
  - id: openwiki-source-6a8850bd107a3ccc222eec42
    resource: repo://agent-expertise-framework/00-data-lake/00-llm-friendly-docs-framework.md
generated: { by: "claude-code", at: "2026-08-30T15:41:00.038Z" }
---

## Starting point

This is the original methodology that opens this session's line of inquiry: a set of principles for reducing hallucination by how documentation is designed, written before any of it was tested against a real codebase. It was later tested against three cloned open-source projects (Apache Amoro, Iceberg, Paimon); that validation and its resulting revisions are recorded in [Validating the Framework: Where Agent Expertise Comes From](framework-validation-research.md).

## Core statement

> A document is easy to read when the structure, relationships, and conditions of its information are written explicitly enough that an LLM never has to "reconstruct them by inference."

## The 12 principles

### 1. Explicitness

A human reader understands "logs in via Kakao OAuth" without elaboration. An LLM reading the same sentence is missing the provider, the grant type, where the token is issued, the distinction between signup and login, what value is stored in the DB, the re-login flow, and which of frontend/backend/external-service calls which. Flows should be numbered and stepped through explicitly, including their conditions.

### 2. Write "why," not just "what"

"We use Redis" says less than "Redis is for session/temporary state only; it never stores permanent data, authorization info, or business data, because entries can expire via TTL." Stating the purpose, what is deliberately excluded, and the reason prevents the LLM from making a plausible-but-wrong design decision, such as "there's a Redis, so let's use it for caching."

### 3. Separate current state from target state

Because both documentation and code enter the model's context together, a document that describes a future or past state as if it were current creates a conflict. Separate `Current implementation` from `Planned change`, or use an explicit state marker like `Status: ACTIVE / DEPRECATED / PLANNED`.

### 4. Glossary

Calling the same concept User/Member/Account/Student interchangeably causes an LLM to treat them as different concepts. Build a term-mapping table, and explicitly list terms that are *not* used (e.g., "Member is not used; use User").

### 5. File structure as "responsibility," not "listing"

A directory tree is already known to the LLM. What matters is describing each layer's responsibility and what it must not do — e.g., "the Controller handles only HTTP request/response and must not contain business logic."

### 6. Make prohibitions explicit (Constraints)

Code changes are more stable when "what must never be done" is clearer than "what can be done." Separate these out explicitly as Architecture Rules / Constraints / Invariants.

### 7. Be precise with numbers and conditions

Instead of "stays valid for a while," write "Access Token TTL 30 minutes, Refresh Token TTL 14 days" — condition, threshold, and result stated as concrete numbers.

### 8. Make code–doc–DB–cache relationships explicit

Listing the related code files, DB tables, and cache keys in a document lets an LLM trace document → code → data.

### 9. Don't make one giant document

Split by topic — `docs/architecture/`, `docs/domain/`, `docs/api/`, `docs/rules/`, `docs/decisions/` — so an agent can read only the part it needs.

### 10. ADR (Architecture Decision Record)

Record "why the structure is the way it is now" using Context/Decision/Alternatives/Consequences — a document that explains why the current code looks the way it does.

### 11. Document hierarchy

```
PROJECT → RULES / ARCHITECTURE / DOMAIN → MODULE → API / DB / CODE
```

Each document covers only what it needs, drawn from: Purpose, Scope, Current State, Responsibilities, Dependencies, Rules/Constraints, Inputs/Outputs, Failure Cases, Related Code/DB, Related Documents, Examples, Status.

### 12. Documentation alone is not enough — a verification system is the core piece

> Instructing an agent to simply "understand the project and modify it" is not sufficient. The agent must be made to **gather verifiable facts before acting**.

```
Task → search related docs → search related code → confirm current implementation
     → check whether docs and code agree → if they disagree, report instead of modifying
     → plan the change → modify the code → test
     → re-verify doc/code agreement after the change
```

**Documentation is the knowledge that tells an LLM about the project; the verification system is the mechanism that stops it from inventing that knowledge freely.** In a large project, the core of suppressing hallucination ultimately comes down to a structure that makes the LLM say "I don't know" when it doesn't know.

## Related pages

- [Validating the Framework: Where Agent Expertise Comes From](framework-validation-research.md) — testing and revising this framework against real open-source projects
- [Instruction Clarity Incident](instruction-clarity-incident.md) — the symmetric problem (how instructions should be given to an LLM, rather than how documents should be written for one)
