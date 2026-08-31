# Files

- [Framework validation research](framework-validation-research.md)
- [Instruction Clarity Incident: Misreading a Lookup as a Decision](instruction-clarity-incident.md) - A recorded failure case where an agent mistook a fact it could have looked up (a starred GitHub repo, resolvable from known account plus tool access) for a decision only the user could make, asked unnecessary clarifying questions, and the instruction-writing guidance derived from it.
- [Instruction Resolution Gate Design](instruction-resolution-gate.md) - A proposed natural-language-to-execution interpretation layer that classifies ambiguity as either lookup-resolvable or requiring user judgment, built from the instruction clarity incident, and the argument for why it must be a structural gate rather than something left to model judgment.
- [LLM-Friendly Documentation Framework](llm-friendly-documentation.md) - A 12-principle framework for writing documentation that an LLM can consume without inference gaps — covering explicitness, state separation, glossaries, constraints, ADRs, document layering, and a verification loop — proposed as the starting methodology for this research session.
