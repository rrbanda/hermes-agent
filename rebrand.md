# Rebrand and install on a Mac

This sets the product name, installs that checkout on a Mac, and points chat at an OpenAI-compatible model. No code edits. Replace `acme` and `Acme` everywhere below with your command and display name.

Python modules stay `hermes_*`. The environment variable that selects the data directory stays `HERMES_HOME`. A checkout with no `brand.json` keeps the Hermes names.

## Before you start

- Use Terminal. `git --version` must print a version. If `git` is missing, run `xcode-select --install`, wait for it to finish, and open a new terminal.
- You need the model id your server expects, the API base URL, and an API key. The base URL is the root the server documents for chat, usually ending in `/v1`, because the client calls `/v1/chat/completions`. Do not put `/chat/completions` in the base URL.
- Pick an empty data directory. `$HOME/.acme` is the one used below. Do not point it at an existing `~/.hermes` directory.

## 1. Clone this fork

```bash
git clone https://github.com/rrbanda/hermes-agent.git ~/acme-agent
cd ~/acme-agent
```

Clone this repository. A plain install from `NousResearch/hermes-agent` is still named Hermes.

## 2. Set the name

The command is lowercase letters, digits, and hyphens, up to 64 characters, and it must start with a letter. The display name is one line, 1–64 characters. The banner title becomes `Acme Agent`. The default data directory is `$HOME/.acme`.

```bash
python3 scripts/rebrand.py --cli acme --name "Acme"
cat brand.json
```

`brand.json` should show `"cli": "acme"` and `"name": "Acme"`. `pyproject.toml` must contain `acme = "hermes_cli.main:main"` and `acme-acp = "acp_adapter.entry:main"`. The `hermes-agent` script line stays. Run the same command again to replace a previous name.

## 3. Commit and push before installing

The installer resets this directory to `origin/main`. A rename that is not on `origin` is discarded.

```bash
git add brand.json pyproject.toml
git commit -m "Set the product name to Acme"
git push
```

## 4. Install

```bash
bash scripts/install.sh --dir "$PWD" --channel main \
  --hermes-home "$HOME/.acme" \
  --non-interactive --skip-browser --skip-computer-use
```

`--dir "$PWD"` installs this fork instead of cloning the upstream repository. `--channel main` follows this branch. `--hermes-home` must be empty or absent, and it must be `$HOME/.<command>` so later sessions find it without an extra variable. `--non-interactive` skips the menus. The browser flags only skip those downloads.

The installer adds `$HOME/.local/bin` to `~/.zshrc`. Open a new terminal after it finishes. If `acme` is not found, run `source ~/.zshrc`.

## 5. Configure the model

Edit the `model:` block in `$HOME/.acme/config.yaml`. Change these four lines and leave the rest of the file:

```yaml
model:
  provider: custom
  default: "your-model-id"
  base_url: https://your-host.example/v1
  key_env: LLM_API_KEY
```

`default` is the model id. `provider: custom` means an OpenAI-compatible endpoint. `key_env` names the variable that holds the key. That variable is used only when the request goes to this same `base_url`.

Put the key in `$HOME/.acme/.env`, not in `config.yaml`:

```bash
printf 'LLM_API_KEY=%s\n' 'your-key-here' >> "$HOME/.acme/.env"
chmod 600 "$HOME/.acme/.env"
```

Leave `CUSTOM_BASE_URL` unset. If it is set to a different URL, it overrides `model.base_url` and `LLM_API_KEY` is not sent. `OPENAI_BASE_URL` does not choose this endpoint.

## 6. Check

In a new terminal:

```bash
acme --version
acme -z "Reply with the single word pong."
```

The version line starts with `Acme Agent`. The second command prints the model's reply and exits. Then run `acme` for the chat. The wordmark uses the new name. Quit and start again after any later rename. The name is read when the process starts.

An unedited Hermes persona file in the data directory is replaced with the new name. A persona you edited is left as it is.

## What stays Hermes

- Python module names and `HERMES_*` environment variables
- The `hermes-agent` skill id and the documentation URL
- Locales and the desktop app
- The systemd unit name `hermes-gateway`

The macOS LaunchAgent label follows the command: `ai.acme.gateway`. It does not replace an existing `ai.hermes.gateway` job.

## Bring in upstream later

Add the upstream remote once: `git remote add upstream https://github.com/NousResearch/hermes-agent.git`.

Rebase this branch onto `upstream/main`. If `pyproject.toml` conflicts on the script lines, keep one main line and one acp line, then run `python3 scripts/rebrand.py --cli acme --name "Acme"` again.
