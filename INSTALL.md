# Install skill-ab-eval

<details>
<summary><strong>Claude Code</strong></summary>

### Install

```bash
claude plugin marketplace add cskwork/skill-ab-eval
claude plugin install skill-ab-eval@skill-ab-eval
```

Type `/skill-ab-eval`.

### Verify

```bash
claude plugin list
```

### Update

```bash
claude plugin marketplace update skill-ab-eval
```

### Uninstall

```bash
claude plugin uninstall skill-ab-eval
claude plugin marketplace remove skill-ab-eval
```

</details>

<details>
<summary><strong>Codex</strong></summary>

### Install

```bash
codex plugin marketplace add cskwork/skill-ab-eval --ref main
codex plugin add skill-ab-eval@skill-ab-eval
```

Type `$skill-ab-eval`.

### Verify

```bash
codex plugin list
```

### Uninstall

```bash
codex plugin remove skill-ab-eval
codex plugin marketplace remove skill-ab-eval
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

### Install (extension, always-on)

```bash
gemini extensions install https://github.com/cskwork/skill-ab-eval
```

### Install (command, opt-in)

```bash
mkdir -p ~/.gemini/commands
curl -fsSL https://raw.githubusercontent.com/cskwork/skill-ab-eval/main/skills/skill-ab-eval/agents/gemini.toml \
  -o ~/.gemini/commands/skill-ab-eval.toml
```

Type `/skill-ab-eval` in a new session.

### Verify

```bash
gemini extensions list
```

### Uninstall

```bash
gemini extensions uninstall skill-ab-eval
```

</details>

<details>
<summary><strong>Cursor, OpenCode, Amp, and other agent-skills harnesses</strong></summary>

### Install

```bash
npx skills add cskwork/skill-ab-eval
npx skills add cskwork/skill-ab-eval -g
```

Type `/skill-ab-eval` in a new agent chat.

### Verify

```bash
npx skills list
```

### Update

```bash
npx skills update skill-ab-eval
```

### Uninstall

```bash
npx skills remove skill-ab-eval
```

</details>

<details>
<summary><strong>Antigravity (agy)</strong></summary>

### Install

```bash
agy plugin install https://github.com/cskwork/skill-ab-eval
```

### Verify

```bash
agy plugin list
```

### Uninstall

```bash
agy plugin uninstall skill-ab-eval
```

</details>
