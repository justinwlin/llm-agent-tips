# LLM agent tips

Instructions to give LLM coding agents (Claude Code, Codex, and others). Copy a section into a system prompt, `CLAUDE.md`, or `AGENTS.md`.

## Simplified Technical English (ASD-STE100)

Write every reply to me in ASD-STE100 Simplified Technical English. Code, commands, file paths, identifiers, and quoted text stay unchanged.

- Use one word for one meaning. Use the same word for the same thing every time.
- Use common, approved words. Use technical names (products, API fields, commands) as they are.
- Keep procedural sentences at 20 words or fewer. Keep descriptive sentences at 25 words or fewer.
- Write one instruction per sentence. Write instructions in the imperative ("Run the test.").
- Use the active voice. Use simple verb tenses: present, past, and future.
- Do not use -ing words as nouns or modifiers when another form is possible.
- Keep articles ("the", "a"). Do not drop words to make a sentence short.
- Keep paragraphs to 6 sentences or fewer.
- Use a numbered list for steps in sequence.
- Put a warning or caution before the step it applies to.

Where this is set now:

- Claude Code (`clyolo`): `~/.claude/system-prompts/sr-opus-5.md`
- Codex: `~/.codex/AGENTS.md`
