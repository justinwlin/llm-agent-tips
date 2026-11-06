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

## Screenshots that are not cut off

Give this to an agent that takes screenshots of a web UI for PRs, docs, or slides.

1. Capture the element, not the viewport. Use `locator.screenshot()` in Playwright, or take a full-page screenshot and crop it to the element's `getBoundingClientRect()`.
2. Scale the crop when the page has zoom or a device pixel ratio. Multiply each coordinate by `screenshotWidth / window.innerWidth`.
3. Turn off motion before the capture. Inject `html { scroll-behavior: auto !important }`, and set `prefers-reduced-motion`. Wait for fonts and network idle.
4. Hide or allow for sticky headers and floating widgets. They cover the top of the element.
5. Add about 16 px of padding around the crop, so that borders and shadows stay in the image.
6. Use one fixed viewport size and one device pixel ratio for every capture in a set, so that before and after images are the same size.
7. Set an iframe's height to the content's `scrollHeight`. A fixed height cuts off the bottom of the content.
8. In a page or slide, show one image per frame with `object-fit: contain`. Do not tile images or force a fixed height that crops them.
9. Split a very tall capture into parts of about 1300 px for review. Do not shrink it until the text cannot be read.
10. Open every image after you capture it and look at all four edges. Text that ends at an edge is cut off: capture it again.
11. For a before and after pair, capture both from real running builds of each version, with the same data and the same viewport.

## Tools

### Archify

[tt-a1i/archify](https://github.com/tt-a1i/archify) is an agent skill. It turns an idea, a plan, or a codebase into an interactive HTML diagram. It works with Claude Code, Codex, Cursor, and OpenCode.

Install: tell the agent this.

```text
Install Archify for me by reading https://raw.githubusercontent.com/tt-a1i/archify/main/llms.txt
```

Use: ask for a diagram, for example "Use Archify to diagram this repo's request path."
