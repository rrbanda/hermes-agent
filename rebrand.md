# Rebrand this checkout

The product name lives in `brand.json`. Run one command to change it. No code edits.

Python modules stay `hermes_*`. The environment variable stays `HERMES_HOME`. A missing `brand.json` keeps the Hermes names.

## 1. Clone the fork

```bash
git clone https://github.com/rrbanda/hermes-agent.git ~/acme-agent
cd ~/acme-agent
```

Use this repository. The installer defaults to `NousResearch/hermes-agent` and that tree is still named Hermes.

## 2. Choose a name

`<cli>` is the command. Lowercase letters, digits, and hyphens, up to 64 characters, starting with a letter. `<Name>` is the display name: one line, 1–64 characters. The banner title becomes `<Name> Agent`. The data directory is `$HOME/.<cli>`.

```bash
python3 scripts/rebrand.py --cli acme --name "Acme"
```

Run it again to replace the previous name. `xyz` / `Xyz` is only an example.

Check the two files it writes:

```bash
cat brand.json
```

`pyproject.toml` must contain `acme = "hermes_cli.main:main"` and `acme-acp = "acp_adapter.entry:main"`. The `hermes-agent` script line stays.

## 3. Commit and push before installing

`scripts/install.sh` resets this directory to `origin/main`. A rename that is not on `origin` is discarded.

```bash
git add brand.json pyproject.toml
git commit -m "Set the product name to Acme"
git push
```

## 4. Install into an empty data directory

```bash
bash scripts/install.sh --dir "$PWD" --channel main \
  --hermes-home "$HOME/.acme" \
  --skip-browser --skip-computer-use
```

`$HOME/.acme` must be empty or absent. Do not pass `~/.hermes` if a Hermes install is already there. `--dir "$PWD"` keeps this fork. `--channel main` follows this branch. The browser and computer-use flags only shorten the install.

Keys and tokens go in `$HOME/.acme/.env` after install. Do not commit that file.

## 5. Check

Open a new terminal so the command is on `PATH`, then:

```bash
acme --version
```

The version line should start with `Acme Agent`. Start `acme` once. The wordmark is the new name. Quit and start again after any later rename. The name is read when the process starts.

An unedited Hermes persona file in the data directory is replaced with the new name. A persona you edited is left as it is.

## What stays Hermes

- Python module names and `HERMES_*` environment variables
- The `hermes-agent` skill id and the documentation URL
- Locales and the desktop app
- The systemd unit name `hermes-gateway`

The macOS LaunchAgent label follows the command: `ai.acme.gateway`. It does not replace an existing `ai.hermes.gateway` job.

## Bring in upstream later

Add the upstream remote once: `git remote add upstream https://github.com/NousResearch/hermes-agent.git`.

Rebase this branch onto `upstream/main`. If `pyproject.toml` conflicts on the script lines, keep one main line and one acp line, then run `python3 scripts/rebrand.py` again with the same `--cli` and `--name`.
