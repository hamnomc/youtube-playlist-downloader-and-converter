import os
import subprocess
from pytube import YouTube
import random
import requests
import re
import string
from moviepy.editor import AudioFileClip
from pytube.exceptions import AgeRestrictedError
import tkinter as tk
from tkinter import ttk

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
        if work_m not in our_links:
            our_links.append(work_m)

    return our_links

def download_and_convert(our_links, SAVEPATH, progress_label):
    x = []

    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            pathh = os.path.join(root, name)
            
            if os.path.getsize(pathh) < 1:
                os.remove(pathh)
            else:
                x.append(str(name))

    for link in our_links:
        try:
            yt = YouTube(link)
            main_title = yt.title
            main_title = re.sub(r'[^\x00-\x7F]+', "", main_title)  # Remove non-ASCII characters
            main_title = re.sub(r'[\\/*?:"<>|]', "", main_title)  # Remove special characters
            
            if not main_title:
                main_title = "NOT_ASCII_TITLE_" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

            main_title = main_title + '.mp3'

            if main_title not in x:
                vid = yt.streams.filter(progressive=True, file_extension='mp4', res='360p').first()
                progress_label.config(text=f'Downloading {vid.default_filename} - {round(vid.filesize / (1024 * 1024), 2)} MB')
                vid.download(SAVEPATH)
                progress_label.config(text=f'Downloaded {vid.default_filename}')
        except AgeRestrictedError:
            print(f'Skipping age restricted video: {link}')
            continue
        except:
            print('Connection problem.. Unable to fetch video info')
            break

        if main_title not in x:
            vid = yt.streams.filter(progressive=True, file_extension='mp4', res='360p').first()
            progress_label.config(text=f'Converting {vid.default_filename}')
            vid.download(SAVEPATH)
            video_path = os.path.join(SAVEPATH, vid.default_filename)
            audio_path = os.path.join(SAVEPATH, main_title)
            audio_clip = AudioFileClip(video_path)
            audio_clip.write_audiofile(audio_path)
            os.remove(video_path)
            progress_label.config(text=f'Converted {vid.default_filename} to MP3')
        else:
            progress_label.config(text=f'Skipping {main_title}')

    progress_label.config(text='Downloading finished')

def start_download(url_entry, progress_label):
    url = url_entry.get()
    BASE_DIR = os.getcwd()

    our_links = link_snatcher(url)

    os.chdir(BASE_DIR)

    new_folder_name = foldertitle(url)

    try:
        os.mkdir(new_folder_name[:7])
    except:
        print('Folder already exists')

    os.chdir(new_folder_name[:7])
    SAVEPATH = os.getcwd()

    progress_label.config(text=f'Files will be saved to {SAVEPATH}')
    
    download_and_convert(our_links, SAVEPATH, progress_label)

# Create GUI
root = tk.Tk()
root.title("Playlist Downloader and Converter")

# Playlist URL Entry
url_label = tk.Label(root, text="Enter Playlist URL:")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)

# Download Button
download_button = tk.Button(root, text="Download", command=lambda: start_download(url_entry, progress_label))
download_button.pack(pady=10)

# Progress Label
progress_label = tk.Label(root, text="")
progress_label.pack(pady=10)

# Run GUI
root.mainloop()
