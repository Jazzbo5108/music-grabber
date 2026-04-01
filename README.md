# music-grabber
A python script which downloads audio from the most popular Youtube video with a provided name. Optimized for music

Usage:
```sh
python3 main.py artist_name [song_names...]
```

The program will query Youtube for each song in the form "<artist_name> <song_name>".
To use if artist name is unknown (or if downloading sound for video without artist) simply pass in "" for either song name or artist name.

```sh
python3 main.py --help
```
Help text will be displayed.
