#!python3
# Usage -
# 1. open cmd
# 2. cd to the folder where these files are present
# 3. type - python ytdown.py
# the script will start working

import os
import subprocess
from pytube import YouTube
import random
import requests
import re
import string
from moviepy.editor import AudioFileClip
from pytube.exceptions import AgeRestrictedError

#imp functions


def foldertitle(url):

    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False

    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]

    else:
        print('Incorrect attempt.')
        return False

    return cPL



def link_snatcher(url):
    our_links = []
    try:
        res = requests.get(url)
    except:
        print('no internet')
        return False

    plain_text = res.text

    if 'list=' in url:
        eq = url.rfind('=') + 1
        cPL = url[eq:]
    else:
        print('Incorrect Playlist.')
        return False

    tmp_mat = re.compile(r'watch\?v=\S+?list=' + cPL)
    mat = re.findall(tmp_mat, plain_text)

    for m in mat:
        new_m = m.replace('&amp;', '&')
        work_m = 'https://youtube.com/' + new_m
        # print(work_m)
        if work_m not in our_links:
            our_links.append(work_m)

    return our_links


BASE_DIR = os.getcwd()

print('WELCOME TO PLAYLIST DOWNLOADER DEVELOPED AND CONVERTER')

url = str(input("\nspecify you playlist url\n"))

print('\n ALL THE VIDEOS IN THE PLAYLIST WILL BE DOWNLOADED AND CONVERTED MP3 FORMAT :) \n')

our_links = link_snatcher(url)

os.chdir(BASE_DIR)

new_folder_name = foldertitle(url)
print(new_folder_name[:7])

try:
    os.mkdir(new_folder_name[:7])
except:
    print('folder already exists')

os.chdir(new_folder_name[:7])
SAVEPATH = os.getcwd()
print(f'\n files will be saved to {SAVEPATH}')

x=[]
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        pathh = os.path.join(root, name)
        
        if os.path.getsize(pathh) < 1:
            os.remove(pathh)
        else:
            x.append(str(name))

print('\nconnecting . . .\n')

print()

for link in our_links:
    try:
        yt = YouTube(link)
        main_title = yt.title
        main_title = re.sub(r'[^\x00-\x7F]+', "", main_title)  # Remove non-ASCII characters
        main_title = re.sub(r'[\\/*?:"<>|]', "", main_title)  # Remove special characters
        # Check if main_title is empty after sanitizing
        if not main_title:
            main_title = "NOT ASCII TITLE " + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        main_title = main_title + '.mp3'
        if main_title not in x:
            vid = yt.streams.filter(progressive=True, file_extension='mp4', res='360p').first()
            print('Downloading. . . ' + vid.default_filename + ' and its file size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
            vid.download(SAVEPATH)
            print('Video Downloaded')
    except AgeRestrictedError:
        print(f'Skipping age restricted video: {link}')
        continue
    except:
        print('connection problem..unable to fetch video info')
        break
    if main_title not in x:
            vid = yt.streams.filter(progressive=True, file_extension='mp4', res='360p').first()
            print('Downloading. . . ' + vid.default_filename + ' and its file size -> ' + str(round(vid.filesize / (1024 * 1024), 2)) + ' MB.')
            vid.download(SAVEPATH)
            print('Video Downloaded')
            video_path = os.path.join(SAVEPATH, vid.default_filename)
            audio_path = os.path.join(SAVEPATH, main_title)
            audio_clip = AudioFileClip(video_path)
            audio_clip.write_audiofile(audio_path)
            os.remove(video_path)
            print('Video Converted to MP3')
    else:
        print(f'\n skipping "{main_title}" file \n')

print(' downloading finished')
print(f'\n all your videos are saved at --> {SAVEPATH}')
