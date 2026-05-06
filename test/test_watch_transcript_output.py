import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from scripts import watch


class DefaultWatchWorkDirTests(unittest.TestCase):
    def test_default_watch_work_dir_uses_yt_videos_and_mkdtemp(self):
        with tempfile.TemporaryDirectory() as td:
            fake_home = Path(td) / "home"
            fake_home.mkdir()
            yt_root = fake_home / "yt-videos"

            def fake_mkdtemp(prefix="", dir=None):
                self.assertEqual(prefix, "watch-")
                self.assertEqual(dir, str(yt_root))
                yt_root.mkdir(parents=True, exist_ok=True)
                run = yt_root / "watch-abc"
                run.mkdir()
                return str(run)

            with mock.patch.object(watch.Path, "home", return_value=fake_home):
                with mock.patch("scripts.watch.tempfile.mkdtemp", side_effect=fake_mkdtemp):
                    work = watch.default_watch_work_dir()

            self.assertEqual(work, yt_root / "watch-abc")
            self.assertTrue(yt_root.is_dir())


class TranscriptFilenameTests(unittest.TestCase):
    def test_youtube_watch_url_uses_video_id_filename(self):
        source = "https://www.youtube.com/watch?v=epzzALZ8oYo"
        self.assertEqual(watch.transcript_filename_for_source(source), "yt-epzzALZ8oYo.md")

    def test_non_youtube_url_uses_default_filename(self):
        source = "https://vimeo.com/123456"
        self.assertEqual(watch.transcript_filename_for_source(source), "transcript.md")


class TranscriptSaveBehaviorTests(unittest.TestCase):
    @mock.patch("scripts.watch.download")
    @mock.patch("scripts.watch.get_metadata")
    @mock.patch("scripts.watch.extract")
    @mock.patch("scripts.watch.parse_vtt")
    @mock.patch("scripts.watch.format_transcript")
    def test_main_writes_markdown_and_keeps_stdout_transcript(
        self,
        format_transcript_mock,
        parse_vtt_mock,
        extract_mock,
        get_metadata_mock,
        download_mock,
    ):
        with tempfile.TemporaryDirectory(prefix="watch-test-") as tmp:
            work = Path(tmp)
            subtitle = work / "download" / "video.en.vtt"
            subtitle.parent.mkdir(parents=True, exist_ok=True)
            subtitle.write_text("WEBVTT\n", encoding="utf-8")

            download_mock.return_value = {
                "video_path": work / "download" / "video.mp4",
                "subtitle_path": subtitle,
                "info": {},
            }
            get_metadata_mock.return_value = {"duration_seconds": 5.0, "width": 640, "height": 360, "codec": "h264"}
            extract_mock.return_value = []
            parse_vtt_mock.return_value = [{"start": 0.0, "end": 1.0, "text": "hello"}]
            format_transcript_mock.return_value = "[00:00] hello"

            argv = [
                "watch.py",
                "https://www.youtube.com/watch?v=epzzALZ8oYo",
                "--out-dir",
                str(work),
                "--no-whisper",
            ]
            with mock.patch("sys.argv", argv):
                out = io.StringIO()
                with redirect_stdout(out):
                    result = watch.main()

            self.assertEqual(result, 0)
            content = out.getvalue()
            self.assertIn("## Transcript", content)
            self.assertIn("[00:00] hello", content)
            self.assertIn("Saved markdown:", content)

            transcript_path = work / "yt-epzzALZ8oYo.md"
            self.assertTrue(transcript_path.exists())
            self.assertEqual(transcript_path.read_text(encoding="utf-8"), "[00:00] hello\n")
            summary_path = work / "summary.md"
            self.assertTrue(summary_path.exists())
            summary_content = summary_path.read_text(encoding="utf-8")
            self.assertIn("# Video Summary", summary_content)
            self.assertIn("https://www.youtube.com/watch?v=epzzALZ8oYo", summary_content)
            self.assertIn("[00:00] hello", summary_content)


if __name__ == "__main__":
    unittest.main()
