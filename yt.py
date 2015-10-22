#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pafy
import os
import subprocess
import logging
logging.getLogger().setLevel(logging.ERROR)


def aria(stream):
    args = ['aria2c', '-o',stream.filename, stream.url]
    subprocess.call(args)

def convaudio(file):
    conv_args = ['ffmpeg', '-i', file, '-c:a', 'libfdk_aac', '-profile:a', 
                'aac_he_v2', '-b:a', '24k', file[0:-4]+'-done.m4a']
    subprocess.call(conv_args) 
    os.remove(file)
    os.rename(file[0:-4]+'-done.m4a', file)

def getvideo(videostreams):
    #print(videostreams)
    l = [ "video:webm@854x480", "video:m4v@854x480", "video:webm@640x480",
        "video:m4v@640x360"]
    for i in l:
        for vid in videostreams:
            if vid.__str__() == i:
                print(vid)
                return vid

def getyt(url):
    return pafy.new(url)


def techtalk(yt):
    audio = yt.audiostreams.pop()
    video = getvideo(yt.videostreams)
    # print("====================="+video.__str__())
    aria(audio)
    convaudio(audio.filename)
    if video:
        aria(video)
        conv_args = ['ffmpeg', '-i', video.filename, '-i', audio.filename, '-c:a',
                 'copy', '-c:v', 'copy', audio.filename[0:-4]+'.'+'mkv']
        if subprocess.call(conv_args) == 0:
            os.remove(video.filename)
            os.remove(audio.filename)

url = ""

pl = pafy.get_playlist(url)
for i in pl['items']:
    techtalk(i['pafy'])



