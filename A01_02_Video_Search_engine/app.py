from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi as yta
import re

app = Flask(__name__)

def print_time(search_word, time):
    result = []
    result.append(f"'{search_word}' was mentioned at:")
    for t in time:
        hours = int(t // 3600)
        min = int((t // 60) % 60)
        sec = int(t % 60)
        result.append(f"{hours:02d}:{min:02d}:{sec:02d}")
    return result

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

def transcribe_video(video_id):
    # Your existing code for transcribing the video
    transcript = yta.get_transcript(video_id, languages=('us', 'en'))
    data = [t['text'] for t in transcript]
    data = [re.sub(r"[^a-zA-Z0–9-ışğöüçiIŞĞÖÜÇİ ]", "", line) for line in data]
    return transcript, data

def give_time_stamps(transcript, data2, search_word):
    # Your existing code for finding timestamps
    time = []
    for i, line in enumerate(data2):
        if search_word in line:
            start_time = transcript[i]['start']
            time.append(start_time)
    return time

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        search_word = request.form['search_word']

        video_id = extract_video_id(youtube_url)

        if video_id:
            transcript = yta.get_transcript(video_id, languages=('us', 'en'))
            data = [t['text'] for t in transcript]
            data = [re.sub(r"[^a-zA-Z0–9-ışğöüçiIŞĞÖÜÇİ ]", "", line) for line in data]

            time = give_time_stamps(transcript, data, search_word)

            return render_template('index.html', youtube_url=youtube_url, search_word=search_word, time=time)

    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
