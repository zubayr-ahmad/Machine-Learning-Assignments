import tkinter as tk
from tkinter import ttk
from youtube_transcript_api import YouTubeTranscriptApi as yta
import re

def extract_video_id(youtube_url):
    # Check if the URL is a valid YouTube video URL
    if "youtube.com/watch" not in youtube_url:
        print("Invalid YouTube URL")
        return None

    # Find the index of 'v=' in the URL
    index_v = youtube_url.find('v=')

    # Check if 'v=' is found in the URL
    if index_v == -1:
        print("Video ID not found in the URL")
        return None

    # Extract the video ID starting from 'v='
    video_id_start = index_v + 2  # Move past 'v='
    video_id_end = youtube_url.find('&', video_id_start)
    video_id = youtube_url[video_id_start:video_id_end] if video_id_end != -1 else youtube_url[video_id_start:]

    return video_id

def get_transcript(youtube_url):
    video_id = extract_video_id(youtube_url)
    print(f"Converting the video to text, please wait...")
    transcript = yta.get_transcript(video_id, languages=('us', 'en'))
    data = [t['text'] for t in transcript]
    data = [re.sub(r"[^a-zA-Z0-9-1şğöüçiIŞĞÖÜÇİ ]", "", line) for line in data]
    return transcript, data

def search_and_display(search_word):
    time = give_time_stamps(transcript, data, search_word)
    result_label.config(text=f"Timestamps for '{search_word}': {time}")

def give_time_stamps(transcript, data2, search_word):
    time = []
    for i, line in enumerate(data2):
        if search_word in line:
            start_time = transcript[i]['start']
            time.append(start_time)
    return time

def play_video_from_timestamp(timestamp):
    timestamp_str = f"{int(timestamp//3600):02d}:{int((timestamp//60)%60):02d}:{int(timestamp%60):02d}"
    print(f"Video will play from timestamp: {timestamp_str}")

# GUI Setup
root = tk.Tk()
root.title("YouTube Transcript Search")

# Widgets
url_label = ttk.Label(root, text="YouTube URL:")
url_entry = ttk.Entry(root, width=40)

text_label = ttk.Label(root, text="Search Text:")
text_entry = ttk.Entry(root, width=40)

search_button = ttk.Button(root, text="Search", command=lambda: search_and_display(text_entry.get()))

result_label = ttk.Label(root, text="")

# Grid Layout
url_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
url_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2, sticky="ew")

text_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
text_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky="ew")

search_button.grid(row=2, column=0, columnspan=3, pady=10)

result_label.grid(row=3, column=0, columnspan=3, pady=10)

# Dummy data for demonstration
youtube_url = "https://www.youtube.com/watch?v=1aA1WGON49E"
transcript, data = get_transcript(youtube_url)

# Run the Tkinter main loop
root.mainloop()
