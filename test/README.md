# Tests

Run tests from the repository root:

```bash
python3 -m unittest discover -s test
```

This suite includes transcript output coverage for `scripts/watch.py`, including:
- YouTube filename derivation (`yt-<videoId>.md`)
- Default filename fallback (`transcript.md`)
- Transcript markdown file persistence while keeping transcript output on stdout
- Default working directory parent `~/yt-videos` with per-run `watch-*` subfolders
