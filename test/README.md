# Tests

Run tests from the repository root:

```bash
python3 -m unittest discover -s test
```

This suite includes transcript output coverage for `scripts/watch.py`, including:
- YouTube filename derivation (`yt-<videoId>.md`) including Shorts URLs
- Default filename fallback (`transcript.md`)
- Transcript markdown file persistence while keeping transcript output on stdout
- Default working directory under `~/yt-videos/`: `watch-<videoId>` for YouTube, `watch-<stem>` for local files, tempfile (then optional rename) for other URLs; backward-compatible `default_watch_work_dir()` still uses `mkdtemp`

It also covers `scripts/save_summary.py` (stdin → `summary.md` in a work directory).
