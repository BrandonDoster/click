#!/usr/bin/env python3
"""
Build static animal-click pages from audio files + animals.json.

For each entry in animals.json with a matching audio file in audio/:
  dist/{slug}/index.html         (rendered from template/animal.html)
  dist/{slug}/{slug}.{ext}       (copied audio)

Then renders dist/index.html (landing page) from template/index.html,
linking every animal that was successfully built.

Stdlib only — no requirements.txt needed.
"""

import json
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
AUDIO_DIR = ROOT / "audio"
TEMPLATE_DIR = ROOT / "template"
CONFIG_PATH = ROOT / "animals.json"

# Audio extensions in preference order — best mobile compat first.
AUDIO_EXTS = (".mp3", ".m4a", ".wav", ".ogg")


def find_audio(slug: str) -> Path | None:
    """Return the first matching audio file for `slug`, or None."""
    for ext in AUDIO_EXTS:
        p = AUDIO_DIR / f"{slug}{ext}"
        if p.is_file():
            return p
    return None


def render(template: str, **values: str) -> str:
    """Replace `{{KEY}}` placeholders with values. Simple string substitution
    — keep templates free of literal `{{...}}` that aren't meant to be
    substituted."""
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def main() -> int:
    if not CONFIG_PATH.is_file():
        print(f"::error::Missing {CONFIG_PATH.name}", file=sys.stderr)
        return 1

    animals = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(animals, dict):
        print("::error::animals.json must be a JSON object", file=sys.stderr)
        return 1

    animal_tpl = (TEMPLATE_DIR / "animal.html").read_text(encoding="utf-8")
    index_tpl = (TEMPLATE_DIR / "index.html").read_text(encoding="utf-8")

    # Clean dist
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    built: list[dict] = []
    skipped: list[str] = []

    for slug, emoji in sorted(animals.items()):
        if not isinstance(emoji, str) or not emoji:
            print(f"::warning::Entry '{slug}' has no emoji — skipping")
            skipped.append(slug)
            continue

        audio = find_audio(slug)
        if not audio:
            exts = ", ".join(e for e in AUDIO_EXTS)
            print(f"::warning::No audio file for '{slug}' (looked for {slug} + one of {exts}) — skipping")
            skipped.append(slug)
            continue

        animal_dir = DIST / slug
        animal_dir.mkdir()

        sound_file = f"{slug}{audio.suffix}"
        shutil.copy2(audio, animal_dir / sound_file)

        # Human-readable display name. `red-panda` -> `Red Panda`.
        name = slug.replace("-", " ").title()

        html = render(
            animal_tpl,
            ANIMAL_NAME=name,
            ANIMAL_EMOJI=emoji,
            ANIMAL_EMOJI_URL=quote(emoji),
            SOUND_FILE=sound_file,
        )
        (animal_dir / "index.html").write_text(html, encoding="utf-8")

        built.append({"slug": slug, "emoji": emoji, "name": name})
        print(f"  ✓ /{slug}/")

    # Landing page
    cards = "\n".join(
        f'      <a class="card" href="./{a["slug"]}/" aria-label="{a["name"]}">\n'
        f'        <span class="card-emoji">{a["emoji"]}</span>\n'
        f'        <span class="card-name">{a["name"]}</span>\n'
        f'      </a>'
        for a in built
    )
    index_html = render(index_tpl, CARDS=cards, COUNT=str(len(built)))
    (DIST / "index.html").write_text(index_html, encoding="utf-8")

    # Preserve CNAME for custom-domain deployments
    cname = ROOT / "CNAME"
    if cname.is_file():
        shutil.copy2(cname, DIST / "CNAME")

    print(f"\nBuilt {len(built)} animal page(s) → dist/")
    if skipped:
        print(f"Skipped: {', '.join(skipped)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
