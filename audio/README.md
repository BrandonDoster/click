# audio/

Drop audio files here, one per animal. Filename (minus extension) becomes
the URL slug and must match an entry in `../animals.json`.

Supported formats (in preference order — first match wins):

- `.mp3` — best mobile compatibility, small files
- `.m4a` — good iOS support
- `.wav` — large but works everywhere
- `.ogg` — small, but no iOS Safari support

Example:

```
audio/bear.mp3      →   animals.json: "bear":   "🐻"   →   /bear/
audio/lizard.mp3    →   animals.json: "lizard": "🦎"   →   /lizard/
audio/red-panda.mp3 →   animals.json: "red-panda": "🐼" →   /red-panda/
```

An audio file with no matching `animals.json` entry is silently ignored.
An `animals.json` entry with no matching audio file is logged as a
build warning and skipped.
