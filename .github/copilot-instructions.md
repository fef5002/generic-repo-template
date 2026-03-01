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
