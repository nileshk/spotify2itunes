spotify2itunes.py
====================

This script helps convert Spotify playlists to iTunes playlists. It
achieves this goal by taking as input a file that contains a list of
Spotify HTTP URLs (which point to songs), scrapes the HTML page for
song information, and outputs a tab-delimited text file containing the
song data. This text file can then be imported into iTunes (with only
the songs in your iTunes library showing up in the playlist).

Usage
-----

In Spotify, select all songs in a particular playlist (or specifically
the songs you want), copy and paste into a text file.  You should end
up with a list of HTTP URLs.  Navigating to one of the URLs should
show song information.

Run the script providing the file containing Spotify HTTP URLs using
the -f command line parameter and redirect the output to the
destination file (it writes the output to stdout).

For example, where `starred_tracks.txt` contains the Spotify HTTP URLs:

    ./spotify2itunes.py -f starred_tracks.txt > itunes_playlist.txt

The resulting file `itunes_playlist.txt` can be used with the iTunes
"Import Playlist" option.

Requirements
------------

* Python 2.7 or later (may work with previous version, but wasn't tested)
* BeautifulSoup (Python library)

Note that this is subject to breakage if Spotify changes their HTML page layout.
