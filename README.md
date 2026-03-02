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

