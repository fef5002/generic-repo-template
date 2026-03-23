# generic-repo-template

A starter template with the basics already in place for cloud-first project development.

Includes:

- `.github/copilot-instructions.md` — Copilot custom instructions (vibe coder/designer context, cloud execution, whitelisted dev sites, code style, branching workflow, review checklist, config design, debugging, modularity, sidecar files, profile selection)
- `.github/rulesets/main-requires-pr.json` — GitHub ruleset template that, when applied via repository/organization settings or API, requires a pull request to merge anything into `main` and blocks direct pushes and force-pushes
- `.github/rulesets/multi-bot-open-branches.json` — GitHub ruleset template that, when applied via repository/organization settings or API, keeps `bot-*` and `copilot/*` branches open for direct bot commits while blocking force-pushes
- `.github/workflows/check.yml` — GitHub Actions workflow: installs dependencies and verifies all packages are importable on every push
- `scripts/utils.py` — Shared helpers used by all scripts: debug logging, execution pausing, timestamped log files, config loading with profile support, and dependency checking
- `scripts/generate_sidecars.py` — Scans a directory (local or cloud-mounted) and writes a `.yml` metadata sidecar file next to every file it finds
- `scripts/check_dependencies.py` — Checks every package in `requirements.txt` is installed; prints a friendly fix message for anything missing
- `config/template_settings.yaml` — Template base config with a `default_profile` setting (copy to `config/settings.yaml`)
- `config/profiles/template_local.yaml` — Template local profile (copy to `config/profiles/local.yaml`)
- `config/profiles/template_cloud.yaml` — Template cloud profile (copy to `config/profiles/cloud.yaml`)
- `requirements.txt` — Python package list (`pyyaml`); install with `pip install -r requirements.txt`
- `.gitignore` — Ignores real config files, log files, `.env`, and Python cache folders
- `LICENSE` — MIT license

## AI Branch Workflow

This repository uses a **multi-AI branch model** where each AI contributor gets its own long-lived branch.

### Branch names

| Branch | Purpose |
|--------|---------|
| `copilot` | GitHub Copilot contributions |
| `codex` | OpenAI Codex contributions |
| `gemini` | Google Gemini contributions |
| `claude` | Anthropic Claude contributions |
| `sonnet` | Claude Sonnet contributions |
| `deepseek` | DeepSeek contributions |
| `mistral` | Mistral contributions |

### Rules

- Each AI branch is **long-lived** — it is never automatically deleted.
- Each AI branch allows **direct commits** without requiring a pull request.
- **Force-pushes are blocked** on all AI branches (to preserve history).
- Only `main` requires a pull request before merging.

### How `main` stays stable

`main` is the **stable trunk**. AI agents commit freely to their own named branch, then open a pull request when work is ready. A human reviewer decides which PRs get merged into `main`. No AI commits directly to `main` unless explicitly instructed.

### Automation

The `.github/workflows/apply-ruleset.yml` workflow runs on every push to `main` and can be triggered manually. It:
1. Creates any missing AI-named branches.
2. Applies the `.github/rulesets/ai-branches.json` ruleset via the GitHub API so the rules above are enforced automatically.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify everything is installed
python scripts/check_dependencies.py

# 3. Copy and fill in your config
cp config/template_settings.yaml config/settings.yaml
cp config/profiles/template_local.yaml config/profiles/local.yaml
# edit config/profiles/local.yaml and set scan_dir to your files folder

# 4. Generate sidecar metadata files for a directory
python scripts/generate_sidecars.py --dir /path/to/your/files --profile local

# 5. Run with debug output and step-by-step pauses
python scripts/generate_sidecars.py --dir /path/to/your/files --debug
```

