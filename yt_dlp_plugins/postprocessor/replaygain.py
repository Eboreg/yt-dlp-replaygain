import subprocess

from yt_dlp.postprocessor.common import PostProcessor


class ReplayGainPP(PostProcessor):
    no_album = False
    extensions = ["aiff", "flac", "ape", "mp2", "mp3", "m4a", "mpc", "ogg", "oga", "spx", "opus", "wav", "wv", "wma"]

    def __init__(self, downloader=None, **kwargs):
        super().__init__(downloader)
        if "no_album" in kwargs:
            self.no_album = True

    def run(self, information):
        filepaths = []
        rsgain_args = ["rsgain", "custom", "--tagmode=i", "--loudness=-18", "--opus-mode=r"]
        if not self.no_album:
            rsgain_args.append("--album")

        for entry in information.get("entries", []):
            for download in entry.get("requested_downloads", []):
                filepath = download.get("filepath")
                if filepath and filepath.split(".")[-1] in self.extensions:
                    filepaths.append(filepath)

        if filepaths:
            subprocess.run(rsgain_args + filepaths)

        return super().run(information)
