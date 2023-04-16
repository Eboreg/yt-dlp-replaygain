Postprocessor that applies replaygain to downloaded files if possible. If an entire playlist has been downloaded, it will be treated as an album, i.e. album replaygain will be set (unless explicitly disabled; see below).

It uses [rsgain](https://github.com/complexlogic/rsgain), so make sure that is installed first. Other software may be enabled in the future, if I can be bothered with it (I just put this together in a couple of hours, for my own benefit).

As a bonus, I have included my Bash script for downloading albums from Youtube: [yt-albumdownload]. It arranges the files in the structure: `[artist]/[album]/[track number] [track name].[extension]`, where `artist` is taken from the playlist uploader name (with that pesky " - Topic" suffix stripped). It also strips date from the metadata, as those are mostly incorrect.

## Installation

```shell
python3 -m pip install -U https://github.com/Eboreg/yt-dlp-replaygain/archive/master.zip
```

## Usage

A `when` argument of either `playlist` or `after_move` must be used, otherwise replaygain may not be done on the final files, but on intermediary, pre-transcoding ones.

```shell
# Download a playlist, set album gain:
yt-dlp --use-postprocessor ReplayGain:when=playlist [playlist URL]

# Download a playlist, do NOT set album gain:
yt-dlp --use-postprocessor "ReplayGain:when=playlist;no_album=true" [playlist URL]

# Alternative syntax for the above, because freedom:
yt-dlp --use-postprocessor ReplayGain:when=playlist --postprocessor-args ReplayGain:no_album [playlist URL]

# Download a single track:
yt-dlp --use-postprocessor ReplayGain:when=after_move [playlist URL]
```
