import subprocess
from typing import Iterable, List, Set, Tuple

from yt_dlp.postprocessor.common import PostProcessor  # type: ignore


class ReplayGainApplication:
    def __init__(self, name: str, args: str, args_no_album: str, extensions: str, test: str):
        self.name = name
        self.args = args.split(" ")
        self.args_no_album = args_no_album.split(" ")
        self.extensions = extensions.lower().split(" ")
        self.test = test.split(" ")

    def exec(self, filepaths: Iterable[str], no_album=False) -> Set[str]:
        matching = self.filter(filepaths, no_album)
        if no_album:
            result = subprocess.run(self.args_no_album + list(matching))
        else:
            result = subprocess.run(self.args + list(matching))
        if result.returncode == 0:
            return matching
        return set()

    def exists(self) -> bool:
        result = subprocess.run(self.test, capture_output=True)
        return result.returncode == 0

    def filter(self, filepaths: Iterable[str], no_album=False) -> Set[str]:
        return {f for f in filepaths if f.split(".")[-1].lower() in self.extensions}


class Metaflac(ReplayGainApplication):
    def exec(self, filepaths: Iterable[str], no_album=False) -> Set[str]:
        if no_album:
            handled = set()
            matching = self.filter(filepaths, no_album)
            for path in matching:
                result = subprocess.run(self.args + [path])
                if result.returncode == 0:
                    handled.add(path)
            return handled
        return super().exec(filepaths, no_album)


class ReplayGainPP(PostProcessor):
    no_album = False
    applications: List[ReplayGainApplication] = [
        ReplayGainApplication(
            name="rsgain",
            args="rsgain custom --tagmode=i --loudness=-18 --opus-mode=r --album",
            args_no_album="rsgain custom --tagmode=i --loudness=-18 --opus-mode=r",
            extensions="aiff flac ape mp2 mp3 m4a mpc ogg oga spx opus wav wv wma",
            test="rsgain",
        ),
        ReplayGainApplication(
            name="mp3gain",
            args="mp3gain -a",
            args_no_album="mp3gain -r",
            extensions="mp3",
            test="mp3gain -h",
        ),
        ReplayGainApplication(
            name="vorbisgain",
            args="vorbisgain --album",
            args_no_album="vorbisgain",
            extensions="ogg",
            test="vorbisgain --version",
        ),
        Metaflac(
            name="metaflac",
            args="metaflac --add-replay-gain",
            args_no_album="metaflac --add-replay-gain",
            extensions="flac",
            test="metaflac --version",
        )
    ]

    def __init__(self, downloader=None, **kwargs):
        super().__init__(downloader)
        if "no_album" in kwargs:
            self.no_album = True

    def run(self, information):
        filepaths = set()

        if "no_album" in self._configuration_args("ReplayGain"):
            self.no_album = True

        if "filepath" in information:
            filepaths.add(information["filepath"])

        for entry in information.get("entries", []):
            for download in entry.get("requested_downloads", []):
                if "filepath" in download:
                    filepaths.add(download["filepath"])

        for app in self.applications:
            if not filepaths:
                break
            if app.exists():
                handled = app.exec(filepaths, self.no_album)
                filepaths = filepaths.difference(handled)

        return super().run(information)
