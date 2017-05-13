#!/usr/bin/python3
from __future__ import unicode_literals
import youtube_dl
import urllib
import urllib.request
from bs4 import BeautifulSoup
from multiprocessing import Process
def main():
    document = open("raplist.txt", "r")
    song_list = []
    for name in document:
        song_list.append(name.rstrip("\n").strip('"'))
    document.close()
    for songs in song_list:
        process = Process(target=threadx, args=(songs, ))
        process.start()
def threadx(searchtext):
    query = urllib.parse.quote(searchtext)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    link = youtubelink(soup)
    download(link)

def download(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

def youtubelink(soup):
        vid = soup.find(attrs={'class': 'yt-lockup-title'})
        liste = str(vid).split('href="')
        return "http://www.youtube.com" + str(liste[1].split('"')[0]).rstrip("\n")

main()