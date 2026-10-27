# 🤝 Workbuddy

A [Claude Code](https://claude.com/claude-code) skill that turns Claude into a **thinking partner**, not a know-it-all intern.

Most of the time you describe a problem and Claude jumps straight to an answer and starts building. Workbuddy flips that around: Claude sits down with you, asks questions, maps out the problem, researches it, and talks through options. It **only builds when you say "build it"**.

The goal is to **build context together**, so that by the time you pick a solution, you both understand the problem well enough that the choice feels obvious.

## 🧭 How it works

| Stage | What happens |
|---|---|
| 1. 🪑 Sit down | Claude says the problem back in its own words and asks a few questions |
| 2. 🌳 Explore map | A mind map in Obsidian Canvas: the problem in the middle, 4 branches of things to understand |
| 3. 🔍 Dig deep | Research on each branch: real people's voices, edge cases, each finding labeled verified or assumption |
| 4. ⚖️ Causes and solutions | A second mind map: causes on the left, solution directions on the right |
| 5. 💬 Discuss | 3–4 options compared, with Claude playing devil's advocate on each |
| 6. 📋 Plan | A written plan you both agree on |
| 7. 🔨 Build | Only when you say **build it** |

Claude checks in with you at the end of every stage and never skips ahead.

## ✨ Also included

- **📒 Decision log**: what you decided and why
- **🅿️ Parking lot**: side ideas get saved instead of derailing the conversation
- **▶️ Resume**: call it again on the same topic and it recaps where you left off
- **⚡ ADHD-friendly replies**: short, scannable, at most 3 questions at a time

## 🗂️ What it creates

Everything goes in your Obsidian vault, one folder per topic:

```
🤝 Workbuddy/<Topic>/
├── 00 Start here.md
├── 01 Explore map.canvas
├── 02 Causes and solutions.canvas
├── Research/
├── Decision log.md
├── Parking lot.md
└── Plan.md
```

## 📦 Install

You'll need [Claude Code](https://claude.com/claude-code), [Obsidian](https://obsidian.md) and Python 3.

```bash
git clone https://github.com/tharani-venthan/workbuddy.git ~/.claude/skills/workbuddy
```

Then start a new Claude Code session and type:

```
/workbuddy
```

Workbuddy uses whichever Obsidian vault you currently have open, and tells you which one at the start.

## 🛠️ The mind map script

`scripts/mindmap_canvas.py` turns a simple JSON outline into a neatly laid-out Obsidian `.canvas` file, so cards never overlap. Claude uses it for you, but you can also run it yourself:

```bash
python3 scripts/mindmap_canvas.py outline.json "My map.canvas"
```

See the "Mind map canvases" section of [SKILL.md](SKILL.md) for the outline format.

## 📄 License

[MIT](LICENSE)
