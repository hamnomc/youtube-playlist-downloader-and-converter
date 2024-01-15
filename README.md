# youtube-playlist-downloader-and-converter 
A simple script to download an entire youtube playlist and convert them to mp3.
Made with Python3

> NOTE: I do not encourage to download any copyright content from Youtube, this script is for educational purpose only.



# Usage
<ul>
    <li>open cmd and cd to the folder where this script is present</li>
    <li>type - python ytdown.py</li>
    <li>Press Enter and and follow the instructions to download the playlist :) </li>
</ul>

# Features
<ul>
    <li>Download every video from a playlist and convert them to mp3</li>
    <li>Starts from the previous state when the download has been interrupted for any reason</li>
    <li>Get notified when download is complete</li>
    <li>Get details about the download size of video while they are downloading </li>
</ul>


# Requirements
<ul>
    <li>requests (pip install requests)</li>
    <li>pytube (pip install pytube)</li>
    <li>youtube-dl (pip install youtube-dl)</li>
    <li>moviepy (pip install moviepy)</li>
</ul>




# How it works?
At its core we are using Pytube to download videos and convert them to mp3 format and then delete the video by using moviepy, i made this because i didnt find anything like this when i needed it 
