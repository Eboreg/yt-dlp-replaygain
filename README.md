Postprocessor that applies replaygain to downloaded files if possible. If an entire playlist has been downloaded, it will be treated as an album, i.e. album replaygain will be set (unless explicitly disabled; see below).

It tries to use these applications, in this order:

1. [rsgain](https://github.com/complexlogic/rsgain)
2. [mp3gain](https://mp3gain.sourceforge.net/)
3. [vorbisgain](https://sjeng.org/vorbisgain.html)
4. [metaflac](https://xiph.org/flac/documentation_tools_metaflac.html)

As a bonus, I have included my Bash script for downloading albums from Youtube: [yt-albumdownload](https://github.com/Eboreg/yt-dlp-replaygain/blob/master/yt-albumdownload). It arranges the files in the structure: `[album artist]/[album]/[track number] [track name].[extension]`, where `album artist` is taken from the playlist uploader name (with that pesky " - Topic" suffix stripped).

## Installation

```shell
python3 -m pip install -U https://github.com/Eboreg/yt-dlp-replaygain/archive/master.zip
```

## Usage

A `when` argument of either `playlist` or `after_move` must be used, otherwise replaygain may not be done on the final files, but on intermediary, pre-transcoding ones.

```shell
# Download a playlist, set album gain:
yt-dlp --use-postprocessor ReplayGain:when=playlist {playlist URL}

# Download a playlist, do NOT set album gain:
yt-dlp --use-postprocessor "ReplayGain:when=playlist;no_album=true" {playlist URL}

# Alternative syntax for the above, because freedom:
yt-dlp --use-postprocessor ReplayGain:when=playlist --postprocessor-args ReplayGain:no_album {playlist URL}

# Or, if freedom is not your bag, just use my script!
yt-albumdownload [--various] {playlist URL}

# Download a single track:
yt-dlp --use-postprocessor ReplayGain:when=after_move {track URL}
```
