# animal-click

Static animal sound pages, generated from audio files. Inspired by
[lizard.click](https://lizard.click/).

```
animal-click/
├── .github/workflows/deploy.yml   # Builds + deploys on push to main
├── audio/                         # Drop audio files here ({slug}.mp3, etc.)
├── template/
│   ├── animal.html                # Per-animal page template
│   └── index.html                 # Landing page template
├── animals.json                   # { slug: emoji } mapping
└── build.py                       # Build script (stdlib only)
```

## Adding an animal

1. Add an audio file: `audio/bear.mp3` (or `.m4a`, `.wav`, `.ogg`).
2. Add a line to `animals.json`:
   ```json
   { "bear": "🐻" }
   ```
3. Commit and push. The workflow rebuilds and redeploys.

That's it. The slug (key in `animals.json`) and the audio filename (without
extension) must match exactly. Slugs can use lowercase letters, digits, and
hyphens — `red-panda` → `/red-panda/`, display name "Red Panda".

## URLs after deploy

- `/` — landing page with a grid of every built animal
- `/bear/` — bear page
- `/frog/` — frog page

## Local preview

```sh
python build.py
python -m http.server -d dist 8000
# → http://localhost:8000
```

No Python dependencies — uses stdlib only.

## Deploy on GitHub Pages

1. Push this repo to GitHub.
2. Settings → Pages → **Source: GitHub Actions**.
3. Push to `main`. The workflow runs, builds, and deploys.

### Custom domain

1. Add a `CNAME` file at the repo root containing your domain (e.g. `clicks.example.com`). `build.py` copies it into `dist/` on each build.
2. Set DNS:
   - Subdomain: CNAME `clicks` → `<username>.github.io`
   - Or apex: A records to `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
3. Settings → Pages → check **Enforce HTTPS** once the cert provisions (usually a few minutes after DNS resolves).

## What's not in here

- **No PWA / install prompt** — dropped per scope.
- **No click counters** (personal or global) — no backend, no localStorage.
- **No build tooling beyond `python build.py`** — string substitution into HTML templates. Each generated page is a single self-contained file (~5KB) plus its audio.

## What the build does

For each entry in `animals.json` with a matching audio file:

1. Creates `dist/{slug}/`.
2. Copies the audio file in as `dist/{slug}/{slug}.{ext}`.
3. Renders `template/animal.html` with `{{ANIMAL_NAME}}`, `{{ANIMAL_EMOJI}}`, `{{ANIMAL_EMOJI_URL}}` (URL-encoded for the favicon SVG), `{{SOUND_FILE}}` substituted in. Writes the result to `dist/{slug}/index.html`.

Then it renders `template/index.html` with a card grid of every successfully built animal and writes that to `dist/index.html`. Missing audio files or invalid entries are logged as workflow warnings, not errors — the build doesn't fail on partial coverage.

## Sourcing audio

Sound effect sites with usable licenses:

- [freesound.org](https://freesound.org/) — Creative Commons; check per-clip license.
- [pixabay.com/sound-effects](https://pixabay.com/sound-effects/) — Pixabay license, royalty-free.
- [BBC Sound Effects](https://sound-effects.bbcrewind.co.uk/) — free for personal/educational use.

Keep clips short (under ~1 second) so rapid clicks feel snappy and the audio pool doesn't bottleneck.
