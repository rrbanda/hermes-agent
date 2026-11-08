---
name: rebrand-checkout
description: Rename this checkout to any product name.
version: 1.0.0
author: rrbanda
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [rebrand, brand, fork, upstream, checkout]
    related_skills: [hermes-agent]
---

# Rebrand Checkout Skill

Set the user-facing product name for this checkout. `scripts/rebrand.py` writes `brand.json` and the two setuptools script lines. Python reads `brand.json` at runtime, so the name is not hardcoded in modules. A missing or invalid `brand.json` keeps Hermes. Python module names stay `hermes_*`.

## When to Use

- The checkout should present a name other than Hermes.
- An upstream rebase conflicted with the brand hooks, and the name has to be restored.
- Another machine will install this fork under a chosen command and display name.

Do not use this to rename Python modules, `HERMES_*` environment variables, the `hermes-agent` skill id, or the docs host.

## Prerequisites

- This checkout, with `scripts/rebrand.py` present.
- `python3` on `PATH`.
- No API keys, tokens, or `auth.json` contents in the commit. Those belong in the data directory's `.env`, which is gitignored.

## How to Run

Run this with `terminal` from the checkout root. `<cli>` is the command token. `<Name>` is the display name, one to 64 characters, one line.

```text
python3 scripts/rebrand.py --cli <cli> --name "<Name>" --tagline "<line>"
```

`<cli>` must match `^[a-z][a-z0-9-]{0,63}$`. The display name becomes `<Name> Agent`. The data directory stem becomes `.<cli>`. Example tokens `xyz` and `Xyz` are examples, not the only allowed brand. Running the script again replaces the previous brand. `--tagline` is optional. Omit it to keep an existing slogan. An empty `--tagline` clears it. A renamed checkout with no tagline shows no chat-banner slogan. `--hero-file` sets the session-panel figure from a text file of at most 30 lines and 80 columns. Omit it to keep an existing figure. `--hero ""` clears it. A renamed checkout with no figure shows none.

## Quick Reference

| Item | After a rebrand |
|---|---|
| `brand.json` | `{"cli","name"}`, plus optional `tagline` and `hero` |
| `pyproject.toml` `[project.scripts]` | `<cli>` and `<cli>-acp` only. `hermes-agent` stays |
| Command, banner, skin, help, fallback persona | `brand_cli`, `brand_name`, `brand_display_name`, `apply_brand` |
| Data directory | `~/.<cli>` on POSIX, `<cli>` under LocalAppData on Windows |
| LaunchAgent label | `ai.<cli>.gateway` |
| Env var for the data directory | still `HERMES_HOME` |
| Modules, skill id `hermes-agent`, docs URL | unchanged |
| Locales, desktop product identity, systemd unit `hermes-gateway` | unchanged |

New user-facing copy calls `apply_brand` or the `brand_*` helpers in `hermes_constants.py`. Do not add a second copy of the name.

## Procedure

1. With `read_file`, open `brand.json` if it exists, and the `[project.scripts]` table in `pyproject.toml`.
2. Choose `<cli>` and `<Name>`. Confirm `<cli>` is a new command, not a rename of an existing Hermes install the user still wants.
3. Run the script with `terminal`.
4. With `search_files`, confirm `brand.json` and the two script lines match the chosen names, and that `hermes-agent = "agent.legacy_cli:main"` is still present.
5. Keep the rebrand on its own branch. Add an `upstream` remote for the Hermes repository. Rebase the branch onto upstream `main`.
6. If the rebase conflicts in `[project.scripts]`, keep one main line and one acp line, then run the script again so those lines match `brand.json`.
7. If the rebase conflicts in a file that calls `apply_brand` or a `brand_*` helper, keep the helper call. Upstream text stays the source string; the helper swaps the product name.
8. Commit only checkout files. Do not commit a data directory, `.env`, `auth.json`, or a home-directory config.
9. Push the branch before installing. `scripts/install.sh` fast-forwards the checkout to `origin/<branch>` and resets when that is not possible, which drops an unpushed rebrand.
10. On another machine, clone that branch, run the script only if that machine needs a different name, commit and push that name, then install:

```text
bash scripts/install.sh --dir "$PWD" --channel main --hermes-home "$HOME/.<cli>"
```

Point `--hermes-home` at an empty directory. Do not reuse an existing Hermes data directory.

## Pitfalls

- A global text replace of `hermes` breaks imports. The loader's word-boundary replace leaves `hermes-agent` and the docs host alone.
- Skin defaults, the fallback identity, the banner wordmark, and the banner tagline are fixed at import. Start a new process after changing `brand.json`.
- An unedited Hermes `SOUL.md` is upgraded to the current brand. A file the user edited is left alone, including a persona seeded by a previous brand. Delete that unedited persona, or edit it, or the model keeps the old name.
- The banner credits "Nous Research" only when the provider is `nous` or `nous-api`. A custom endpoint must not gain that credit.
- `install.sh` against a dirty or unpushed checkout resets the brand back to whatever `origin` has.
- The launchd label `ai.<cli>.gateway` must not replace an existing `ai.hermes.gateway` job.

## Verification

With `terminal`, from the checkout root:

```text
python3 -c "from hermes_constants import brand_cli, brand_display_name; print(brand_cli(), brand_display_name())"
```

Expect `<cli>` and `<Name> Agent`. With `read_file`, confirm `pyproject.toml` has `<cli> = "hermes_cli.main:main"` and `<cli>-acp = "acp_adapter.entry:main"`. Start a new process and read the banner: the wordmark and title use the new name, and a custom model line does not say Nous Research. With `search_files`, confirm the staged diff has no `.env`, `auth.json`, or key material.
