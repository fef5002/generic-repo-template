# GitHub Copilot Custom Instructions

## About Me

I am a vibe coder and designer — not a professional developer. I describe what I want code to do, and I rely on Copilot and other AI tools to write the actual code. Please keep this in mind in all responses:

- Explain what code does in plain English, not in developer jargon.
- When something could break or has an important caveat, call it out clearly.
- Prefer simple, readable solutions over clever or compact ones.
- Add brief comments in the code itself explaining *what* each section does.
- I am working on a **Surface Pro 3**, so I cannot run local language models. All AI, compute, and heavy processing must use cloud services.

## Execution Environment

All code in this template and projects derived from it should target **cloud execution**:

- Prefer cloud-hosted runtimes: GitHub Codespaces, GitHub Actions, Google Colab, or similar.
- Do **not** assume a powerful local machine — avoid local GPU/ML dependencies.
- Scripts should be runnable from a browser-based terminal or a lightweight cloud shell.
- When a tool requires installation, provide the exact `pip install` or equivalent command.

## Whitelisted Development Sites

The following sites are trusted references and allowed endpoints for this project and any projects derived from this template:

### AI & Coding Assistants
- https://github.com/
- https://github.dev/
- https://copilot.microsoft.com/
- https://copilot.github.com/
- https://docs.github.com/

### Cloud Platforms
- https://portal.azure.com/
- https://console.cloud.google.com/
- https://onedrive.live.com/
- https://drive.google.com/

### Developer Documentation
- https://docs.python.org/
- https://pypi.org/
- https://rclone.org/
- https://developer.microsoft.com/
- https://docs.microsoft.com/

### Package Registries & Tools
- https://npmjs.com/
- https://hub.docker.com/

## Code Style Preferences

- **Python** is the preferred language for scripts and automation.
- Use clear, descriptive variable names (e.g. `output_folder` not `o`).
- Prefer standard library modules over heavy third-party dependencies when practical.
- Include a short docstring at the top of every script explaining what it does.
- Handle errors gracefully with friendly messages — not raw stack traces — wherever possible.
- When writing file paths, use `pathlib.Path` (not raw string concatenation).

## Project Structure Conventions

New projects from this template should follow this structure:

```
project-name/
├── .github/
│   ├── copilot-instructions.md   # these instructions, copied forward
│   └── rulesets/                 # branch protection rulesets
├── config/                       # user-editable configuration files
├── docs/                         # documentation and how-to guides
├── scripts/                      # runnable Python scripts
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Security & Privacy

- Never hardcode credentials, API keys, or passwords in source code.
- Always read secrets from environment variables or a `.env` file that is listed in `.gitignore`.
- Do not commit large binary files, media assets, or personal data to the repository.

## Communication Style

When responding in chat or in comments:

- Use bullet points and short paragraphs — not walls of text.
- If there are multiple steps, number them.
- If something could go wrong, put it in a **> ⚠️ Note:** block.
- Assume I have not seen the code before; briefly remind me what it does before changing it.

## Branching & PR Workflow

Each AI agent (bot) works in its **own branch**, never directly on `main`:

- Branch names follow the pattern `bot-<agent>` or `copilot/<task>` (e.g. `bot-copilot`, `copilot/add-feature`).
- Bots **commit and push** to their own branch freely.
- Bots **open a pull request** when work is ready, but **do not merge it**. Merging is done by the repo owner or a designated reviewer.
- The owner reviews open PRs and decides which to merge into `main`.
- Force-pushes to `main` are blocked by the `main-requires-pr` ruleset.

## Code Review Checklist

Before any code is merged into `main`, verify all of the following:

- **No hardcoded values** — file paths, URLs, usernames, account names, and credentials must never be written directly in the script files. Use config files or environment variables instead.
- **Environment-agnostic** — the code must run correctly regardless of operating system, user account, or cloud provider. Do not assume `C:\Users\...`, `/home/alice/`, or any specific machine.
- **Idempotent** — running the script more than once must be safe. It should not duplicate data, re-create things that already exist, or error out on a second run. Use checks like "skip if already exists."
- **No personal data in source code** — no real file paths, email addresses, or account identifiers committed to the repo.

## Config Design: Self-Detecting at Runtime

Config files and scripts must detect their own environment rather than relying on hardcoded paths:

- Resolve the project root dynamically (e.g. using `pathlib.Path(__file__).parent` in Python — this finds the folder containing the current script, wherever it is run from).
- Config files (e.g. `config/settings.yaml`) should use **relative paths** or **placeholder tokens** that get substituted at runtime.
- Provide a `config/template_*.yaml` example alongside every real config file; real config files belong in `.gitignore`.
- When a required config value is missing, the script should print a clear, friendly message explaining what to set and where — not crash silently.

## Debugging Standards

Every script must include a **debug mode** that can be enabled without editing source code:

- Accept a `--debug` flag on the command line, or check for a `DEBUG=true` environment variable.
- In debug mode:
  - Print a step-by-step execution log showing what the script is about to do before it does it.
  - Pause at key checkpoints and ask the user to press Enter to continue (so they can inspect state before each major action).
  - Write a timestamped log file to a `logs/` folder (or the path specified in config).
- In normal mode, keep output concise — only print success/failure summaries.
- Log files must never contain credentials or personal data.

## Modularity

Code must be split into small, single-purpose modules so that any one part can be read, tested, or replaced in isolation:

- Each script file should do **one thing** (e.g. `gather_metadata.py`, `build_index.py`, `execute_plan.py`).
- Shared helper functions live in a dedicated `utils.py` (or a `utils/` package).
- A top-level `main.py` or `run.py` may orchestrate the steps but should contain minimal logic itself — just the sequence of calls.
- Avoid putting unrelated logic in the same function (a function is a named block of code that does one specific task). If a function is longer than ~30 lines, consider splitting it.

