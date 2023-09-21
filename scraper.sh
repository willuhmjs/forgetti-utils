#!/bin/bash

# command to download and get frames from youtube video
# use if roboflow video upload isn't working

# Check for the youtube-dl and ffmpeg commands
if ! command -v yt-dlp &>/dev/null; then
    echo "Error: youtube-dl is not installed. Please install it."
    exit 1
fi

if ! command -v ffmpeg &>/dev/null; then
    echo "Error: ffmpeg is not installed. Please install it."
    exit 1
fi

# Check if a YouTube URL is provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <YouTube_URL>"
    exit 1
fi

# Get the YouTube video URL from the first argument
youtube_url="$1"
video_id=$(echo "$youtube_url" | cut -d '=' -f 2)

# Download the video using youtube-dl
#yt-dlp --verbose -f best -o "yt$video_id/video.mp4" "$youtube_url"

# Check if the download was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to download the video."
    exit 1
fi

# Create a folder for frames
mkdir -p yt$video_id/frames

# Slice the video into frames using ffmpeg
ffmpeg -i yt$video_id/video.mp4 -vf "fps=1" yt$video_id/frames/frame%04d.png

# Check if the frame extraction was successful
if [ $? -eq 0 ]; then
    echo "Frames extracted successfully and saved in the 'frames' folder."
else
    echo "Error: Failed to extract frames from the video."
fi
