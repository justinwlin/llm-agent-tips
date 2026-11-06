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

## Demo videos of a browser flow

Give this to an agent that drives a web UI with Playwright and must record a demo of it. Scripts: [`scripts/demo-video/`](scripts/demo-video/).

1. Record with a CDP screencast, not Playwright's `recordVideo`. `recordVideo` works only in a new context, which loses the signed-in session. A screencast attaches to the tab that is already open: `node record.mjs http://localhost:9334 ./rec`.
2. Keep every step of the flow in that one tab. A new tab is not recorded.
3. Write down the local time when each step starts and ends. You need the times to fast-forward the waits.
4. Stop the recorder with a file, not a signal: `touch ./rec/STOP`. The recorder can then end cleanly from another command.
5. Build the video with `python3 build.py ./rec segments.json demo.mp4`. Give each segment a speed and a caption: 1x while the user and the agent act, 20x while a pod starts or a page loads. A 15-minute session becomes about 6 minutes.
6. Put the captions in a subtitle track, not burned into the frames. Homebrew `ffmpeg` often has no `drawtext`. `build.py` adds a `mov_text` track that QuickTime shows, and it writes `captions.vtt` for a web page `<track>`.
7. Take stills from the finished video with `ffmpeg -ss <seconds> -i demo.mp4 -frames:v 1 step-1.jpg`. Screencast frames show the whole tab. Playwright screenshots of a headed window with a set viewport can be cut off on the right.
8. Look at a strip of the chat panel across the video before you share it. A panel that does not scroll to new messages hides the answer in the frames.
9. Serve the video from a server that supports byte ranges. Without ranges, the video cannot seek, and Safari may not play it. Python's `http.server` does not support ranges.

## Code review: keep code simple

Give this to an agent that writes or reviews code. Each rule comes from a finding that a reviewer made more than once.

Remove what nothing uses:

1. When you remove the last caller of a prop, field, or parameter, remove it too. Linters do not report a field that is only written in an object literal.
2. Trace each analytics or log field from the place that sets it to the place that sends it. A field that the caller never passes is always empty, and a test that sets it by hand hides that.
3. Remove a guard for a state that cannot occur. If the state can occur, handle it completely. A guard that returns early can stop a flow without an error.
4. Remove a type cast such as `as never` or `as any`, then run the type check. Keep a cast only when the check fails, and then use the narrowest cast (`as unknown as Type`).

Keep logic easy to read:

5. Keep each function at a cognitive complexity of 15 or less. Move each branch into a named helper. Return early. Do not nest ternary operators.
6. Replace a long `if` chain with a table of data: an array of `{ pattern, result }` and one loop.
7. Put each repeated value (a duration, a URL, a tool name) in one named constant. Separate display text from lookup keys, and use one case style for all display text.
8. Use the styling and animation system of the framework. Do not add a `<style>` tag in each component instance. Scope hover effects to a named group, so that the effect does not start from an unrelated parent.

Do not lose or leak data:

9. When you convert one shape into another (a proposal into a form, a request into a payload), check every field. Carry each field through, or block the action. Do not drop a field silently.
10. Show only an allowlist of fields to users. Do not show raw tool output or prompts behind a "Details" button.
11. Add a join key (an ID) to each analytics event, so that you can connect the event to the action that caused it.
12. Use `https` in URL constants, also in placeholder URLs.

Make the UI correct for all users:

13. Do not show state only with a color or an icon. Add text, and use a visually hidden span when the text must not show.
14. Mark decorative icons `aria-hidden`. When a button removes itself after a click, move focus to the element that shows the result.
15. Guard each one-time action (approve, submit, switch) against a double click. Disable the control after the first click.
16. Mark component props as read-only.

Check the review before you change code:

17. Prove the reviewer's premise with a test that fails before you fix anything. If the test passes on the old code, the premise is wrong: keep the test as a guard, and reply with the result.
18. Write a test for each side effect (analytics, navigation, focus). Mock the module at its boundary and assert the call and its arguments.

## Fixes in a stack of PRs

Give this to an agent that applies review fixes to a stack of dependent PRs.

1. Make each fix a separate commit at the top of the stack. Run the tests on each commit.
2. Move each fix into the earliest PR after which no later commit changes the fix's files. If you move a fix to an older PR where the code is different, every later commit conflicts.
3. Move the commits with `git rebase -i --update-refs <base>`. Set `GIT_SEQUENCE_EDITOR` to a script that moves each `pick` line above the `update-ref` line of its target branch.
4. Before the rebase, write down every other ref that points into the stack (backups, experiments). `--update-refs` moves them too. Use a tag for a backup, not a branch.
5. After the rebase, compare the old and new top: `git diff <old-top> HEAD` must be empty. Compare each branch with its remote to see which PRs changed.
6. Run the type check and the tests on each changed PR head, not only on the top.
7. Run the full test suite with no other test run in parallel. Under load, tests time out. Run each failed suite again alone before you report a failure.
8. Push with `--force-with-lease=<branch>:<expected-sha>` for each branch. Then reply on each review thread with a link to the commit that fixed it.

## Tools

### Archify

[tt-a1i/archify](https://github.com/tt-a1i/archify) is an agent skill. It turns an idea, a plan, or a codebase into an interactive HTML diagram. It works with Claude Code, Codex, Cursor, and OpenCode.

Install: tell the agent this.

```text
Install Archify for me by reading https://raw.githubusercontent.com/tt-a1i/archify/main/llms.txt
```

Use: ask for a diagram, for example "Use Archify to diagram this repo's request path."
