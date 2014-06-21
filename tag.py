#!/usr/bin/env python3


"""
This is a quick hack script to tag songs downloaded from
soundcloud (or elsewhere) using spotify/itunes's api
"""

__author__ = 'Ayush Shanker'

import sys, os
import json

try:
    import argparse
    import requests
    from mutagenx.mp3 import MP3
    from mutagenx.mp4 import MP4, MP4Cover
    from mutagenx.id3 import TIT2, TALB, TPE1, WOAF, TCOM, TCON, TDRC, APIC
except ImportError:
    print("dependencies not installed")



def chooseTag(data):
    for i in range(data['resultCount']):
        track = data['results'][i]
        print(color.BOLD + '\033[4m' + color.YELLOW + str(i), end=" : ")
        print(color.RED + track['trackName'])
        try:
            print(color.BLUE + track['collectionName'], end=" - ")
        except KeyError:
            print("no album art :'(")
        print(color.PURPLE + track['artistName'] + color.END)
    print("enter your choice(0/1/2/3/4)")
    choice = int(input())
    return data['results'][choice]


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def normalise(keywords):
    keywords=keywords.replace(' featuring',' ')
    keywords=keywords.replace(' Featuring','')      # should move all .replace() keys 
    keywords=keywords.replace('feat.','')           # to a seperate file for cleaner code
    keywords=keywords.replace('Feat.','')
    keywords=keywords.replace('feat','')
    keywords=keywords.replace('Feat','')
    keywords=keywords.replace('OUT NOW','')
    keywords=keywords.replace('DOWNLOAD','')
    keywords=keywords.replace('Out now','')
    keywords=keywords.replace('Premiere','')
    keywords=keywords.replace('Exclusive','')
    keywords=keywords.replace('EDM.com','')
    keywords=keywords.replace('ft.','')
    keywords=keywords.replace(' by',' ')
    keywords=keywords.replace('ft.','')
    keywords=keywords.replace('ft.','')
    keywords=keywords.replace('ft.','')
    keywords=keywords.replace('ft.','')
    keywords=keywords.replace('ft.','')
    keywords=keywords.replace('ft.','')
    keywords=keywords.replace('Free Download','')
    keywords=keywords.replace('FREE','')
    keywords=keywords.replace('Thissongissick.com','')
    keywords=keywords.replace('Available','')
    keywords=keywords.replace('Offical','')
    keywords=keywords.replace(' OUT NOW','')
    keywords=keywords.replace(' Out Now','')
    keywords=keywords.replace(' Feat','')
    keywords=keywords.replace(' Ft.','')
    keywords=keywords.replace('Clip','')
    keywords=keywords.replace('CLIP','')
    keywords=keywords.replace(' - ',' ')
    keywords=keywords.replace(' & ',' ')
    keywords=keywords.replace('Original Mix',' ')
    keywords=keywords.replace('TEASER','')
    keywords=keywords.replace('Remix','')
    keywords=keywords.replace('remix','')
    keywords=keywords.replace('TEASER','')
    keywords=keywords.replace('Teaser','')
    keywords=keywords.replace('PREVIEW','')
    keywords=keywords.replace('PREVIEW','')
    keywords=keywords.replace('Preview','')
    keywords=keywords.replace('\"', '')
    keywords=keywords.replace('!', '')
    keywords=keywords.replace(',', '')
    keywords=keywords.rstrip()
    keywords=keywords.replace(' ','+')
    keywords=keywords.replace('-','+')
    keywords=keywords.replace('+++','+')
    keywords=keywords.replace('[]', '')
    keywords=keywords.replace('(+)', '')
    keywords=keywords.replace('[+]', '')
    keywords=keywords.replace('()', '')
    keywords=keywords.replace('(', '')
    keywords=keywords.replace(')', '')
    keywords=keywords.replace('**', '')
    print("accept " + color.GREEN + keywords + color.END + "(y/n)")
    choice = input()
    if choice.lower() == 'e':
        exit()                      # a quick exit in case the file is tagged already
    if choice.lower() == 'y':
        return keywords
    if choice.lower() == 'n':
        text = input()
        return text
    return keywords

def searchItunes(args, query):
    url = "https://itunes.apple.com/search?term=%s&entity=musicTrack&limit=5" % query.replace(' ','+')
    response = requests.get(url, verify=False)
    j = json.loads(r.text)
    for i in range(j['resultCount']):
        track = j['results'][i]
        print(color.YELLOW+str(i), end=" : ")
        print(color.RED+ track['name'])
        print(color.BLUE + track['album']['name'], end=" - ")
        artists = ""
        for i in track['artists']:
            artists = artists + i['name']+ ", "
        print(color.PURPLE + artists + color.END)
    print("choose (0/1/2/3/4) ")
    choice = str(input())
    trackSelected = j['results'][choice]
    tag = {'api':'itunes'}
    tag['title'] = trackSelected['trackName']
    tag['artist'] = trackSelected['artistName']
    tag['album'] = trackSelected['collectionName']
    tag['album'] = trackSelected['primaryGenreName']
    tag['trackNumber'] = trackSelected['trackNumber']
    tag['totalTracks'] = trackSelected['trackCount']
    if args.b:
        tag['artworkURL'] = trackSelected['artworkUrl100'].replace('100x100', '600x600')
    else:
        tag['artworkURL'] = trackSelected['artworkUrl100'].replace('100x100', '400x400')
    tag['uri'] = trackSelected['collectionId'] + ":" + trackSelected['trackId']
    return tag

def searchSpotify(args, query):
    url = "https://api.spotify.com/v1/search?q=%s&type=track&limit=5" % query.replace(' ','%20')
    response = requests.get(url, verify=False)
    j = json.loads(r.text)['tracks']
    iterLimit = min(j['total']-j['offset']+1, j['limit'])
    for i in range(iterLimit):
        track = j['items'][i]
        print(color.YELLOW+str(i), end=" : ")
        print(color.RED+ track['name'])
        print(color.BLUE + track['album']['name'], end=" - ")
        artists = ""
        for i in track['artists']:
            artists = artists + i['name']+ ", "
        print(color.PURPLE + artists + color.END)
    print("choose (0/1/2/3/4) ")
    choice = str(input())
    trackSelected = j['items'][choice]
    tag = {'api':'spotify'}
    tag['title'] = trackSelected['name']
    tag['artist'] = trackSelected['artists'][0]['name']
    tag['album'] = trackSelected['album']['name']
    tag['trackNumber'] = trackSelected['track_number']
    tag['totalTracks'] = 0
    if args.b:
        tag['artworkURL'] = trackSelected['album']['images'][0]['url']
    else:
        tag['artworkURL'] = trackSelected['album']['images'][1]['url']
    tag['uri'] = trackSelected['href']
    return tag

def determineFormat(audio, track):
    """
    determines the file format of audio file
    :returns: mutagen audio object, search query text
    """
    name = track.lower()

    if name.endswith("mp3"):
        audio = MP3(os.path.abspath(track))
        try:
            print(str(audio['TPE1']))
            track = str(audio['TIT2'])
        except Exception:
            track = str(track)[0:-4]

    if name.endswith("mp4") or name.endswith("m4a") or name.endswith("m4v"):
        audio = MP4(os.path.abspath(track))
        try:
            track = str(audio[b'\xa9nam'][0])
        except Exception:
            track = str(track)[0:-4]

    return audio, track


def main(argv):
    parser = argparse.ArgumentParser(description='Tag your mp3/m4a files using Spotify/Itunes metadata API')
    parser.add_argument("-i","--itunes", help="retag using itunes",action="store_true")
    parser.add_argument('songs', metavar='audiofile', nargs='+', help="audio files")
    args = parser.parse_args()
    for track in args.songs:
        audio, keywords = determineFormat(track)
        keywords = ' '.join(keywords.split())
        keywords = normalise(keywords)
        if args.i:
            data = searchItunes(keywords)
        else:
            data = searchSpotify(keywords)
        try:
            tagmp3(data, audio)
            print(color.GREEN + "tagged!  ⋆ ᴗ ⋆" + color.END)
        except Exception:
            print(color.RED + "failed!  (；ᴗ；)" + color.END)


def tagmp3(tagdata, audio):
    audio["TIT2"] = TIT2(encoding=3, text=tagdata['title'])
    audio["TPE1"] = TPE1(encoding=3, text=tagdata['artist'])
    try:
        audio["TALB"] = TALB(encoding=3, text=tagdata['album'])
    except KeyError:
        print("no album info provided :'(")                         # itunes sometimes doesn't return album field
    try:
        audio["TDRC"] = TDRC(encoding=3, text=tagdata['trackNumber'])
    except Exception:
        pass
    #if 'TCON' not in audio.keys():
    #    audio["TCON"] = TCON(encoding=3, text=tagdata['genre'])
    if 'APIC:' not in audio.keys():
        audio["APIC"]                                                           # to do
    audio["WOAF"] = WOAF(encoding=3, text=tagdata['api']+tagdata['uri'])
    audio.save()


def tagmp4(tagdata, audio):
    audio[b'aART'] = tagdata['artist']
    audio[b'\xa9nam'] = tagdata['title']
    try:
        audio[b'\xa9alb'] = tagdata['album']
    except KeyError:
        print("no album art :'(")
    audio[b'\xa9ART'] = tagdata['artist']
    #audio[b'\xa9gen'] = tagdata['genre']
    audio[b'trkn'] = [tagdata['trackNumber'], tagdata['totalTracks']]
    audio[b'\xa9cmt'] = tagdata['api']+tagdata['uri']
    pic = requests.get(tagdata['artworkURL'])
    covr = []
    covr.append(MP4Cover(pic.content, MP4Cover.FORMAT_JPEG))
    audio[b'covr'] = covr
    audio.save()


main(sys.argv)