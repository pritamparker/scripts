#!/usr/bin/python3
# -*- coding: utf-8 -*-

description = "This script downloads individual streams from YT and muxes them"

import pafy
import os, sys
import subprocess
import logging
import argparse
logging.getLogger().setLevel(logging.ERROR)

HDVideo = os.getenv("HDVideo")
HDAudio = os.getenv("HDAudio")

def getyt(url):
    return pafy.new(url)


def aria(stream, filename=None):
    if not filename:
        filename = stream.filename
    if not os.path.exists(filename):
        args = ['aria2c', '-o', filename, stream.url_https]
        subprocess.call(args)


def getaudio(audiostreams):
    stream = None
    if HDAudio:
        stream = audiostreams[-1]
    else:
        stream = audiostreams[0]
    # stream.filename = stream.filename.replace("webm", "ogg")
    return stream


def getvideo(videostreams):
    #print(videostreams)
    if HDVideo:
        res = 720
    else:
        res = 480
    for vid in videostreams:
        if str(vid).startswith("video") and vid.dimensions[1] <= res:
            return vid
    print(videostreams)


def download(yt):
    yt.videostreams.sort(key=lambda x: x.dimensions[1], reverse=True)
    audio = getaudio(yt.audiostreams)
    video = getvideo(yt.videostreams)
    audiofile = audio.filename.replace("webm", "ogg")
    aria(audio, audiofile)
    aria(video)
    conv_args = ['ffmpeg', '-i', video.filename, '-i', audiofile,
                 '-c:a', 'copy', '-c:v', 'copy', video.title +'.mkv']
    if subprocess.call(conv_args) == 0:
        os.remove(video.filename)
        os.remove(audiofile)


def main():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-p','--pl', help='playlist url')
    parser.add_argument('-v', '--video', nargs='?', help='video url')
    args = parser.parse_args()
    if args.video:
        for video in args.video:
            download(getyt(video))
    if args.pl:
        print args.pl
        playlist = pafy.get_playlist(args.pl)
        for i in playlist['items']:
            download(i['pafy'])


if __name__ == '__main__':
    main()
