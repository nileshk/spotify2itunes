#!/usr/bin/env python
"""
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

Credits
-------

Written by: Nilesh Kapadia ( http://nileshk.com )

"""
import optparse
import os
import re
import sys
import urllib
import HTMLParser
from BeautifulSoup import BeautifulSoup

class SpotifyExtract(object):
    def _create_soup(self, url):
        sock = urllib.urlopen(url)
        soup = BeautifulSoup(sock.read())
        sock.close()
        return soup

    def create_song_metadata(self, url):
        soup = self._create_soup(url)
        return self.process_soup(soup, url)

    def process_soup(self, soup, url):
        try:
            artist = soup.find('a', {"href": re.compile('^/artist/')}).string
            album = soup.find('a', {"href": re.compile('^/album/')}).string
            title = soup.find('meta', {"property": 'og:title'})['content']
            return { 'artist': artist, 'album': album, 'title': title }
        except AttributeError:
            print >> sys.stderr, 'Error on: ' + url
        return None

    def process_url_list_file(self, filename):
        h = HTMLParser.HTMLParser()
        with open(filename) as f:
            lines = f.readlines()
        for url in lines:
            try:
                # TODO Handle local URLs by extracting song info from URL
                songdata = self.create_song_metadata(url)
                if songdata:
                    print h.unescape(songdata['title']) + \
                        '\t' + h.unescape(songdata['artist']) + \
                        '\t' + h.unescape(songdata['album'])
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                print  >> sys.stderr, "Unexpected error:", sys.exc_info()[0]
                print  >> sys.stderr, "Error occurred on: " + url

if __name__ == '__main__':
    p = optparse.OptionParser(description = \
        "Convert list of Spotify HTTP URLs to an iTunes-compatible playlist ")
    p.add_option("--file", "-f", \
                 help = "File containing list of Spotify HTTP URLs")
    options, arguments = p.parse_args()

    if not options.file:
        p.error("Must provide filename with -f or --file switch")
    
    print 'Name\tArtist\tAlbum'
    extractor = SpotifyExtract()
    extractor.process_url_list_file(options.file)
