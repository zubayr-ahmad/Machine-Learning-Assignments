from youtube_transcript_api import YouTubeTranscriptApi as yta
import re

def print_time(search_word,time):
    print(f"'{search_word}' was mentioned at:")
    # calculate the accurate time according to the video's duration
    for t in time:
        hours = int(t // 3600)
        min = int((t // 60) % 60)
        sec = int(t % 60)
        print(f"{hours:02d}:{min:02d}:{sec:02d}")

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

youtube_url = "https://www.youtube.com/watch?v=1aA1WGON49E"
video_id = extract_video_id(youtube_url)
print(f"Converting the video to text, please wait...")
transcript = yta.get_transcript(video_id, languages=('us', 'en'))

data = [t['text'] for t in transcript]
data = [re.sub(r"[^a-zA-Z0–9-ışğöüçiIŞĞÖÜÇİ ]", "", line) for line in data]


def give_time_stamps(transcript,data2, search_word):
    time = []
    for i, line in enumerate(data2):
        if search_word in line:
            start_time = transcript[i]['start']
            time.append(start_time)
    return time
search_word = "I"
time = give_time_stamps(transcript, data, search_word)
print(time)
