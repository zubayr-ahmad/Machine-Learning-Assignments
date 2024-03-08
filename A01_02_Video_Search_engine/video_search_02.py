import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip

def search_text_in_video(video_path, search_text):
    clip = VideoFileClip(video_path)
    timestamps = []

    for i, frame in enumerate(clip.iter_frames()):
        # Add your text detection logic here
        # If text is found, append the timestamp to the list
        if search_text in frame:
            timestamps.append(clip.frame_to_timecode(i))

    clip.close()
    return timestamps

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
    entry_video_path.delete(0, tk.END)
    entry_video_path.insert(0, file_path)

def search_and_display():
    video_path = entry_video_path.get()
    search_text = entry_search_text.get()
    timestamps = search_text_in_video(video_path, search_text)

    result_text.delete(1.0, tk.END)  # Clear previous results
    for timestamp in timestamps:
        result_text.insert(tk.END, f"{timestamp}\n")

# GUI setup
root = tk.Tk()
root.title("Video Text Search")

label_video_path = tk.Label(root, text="Video Path:")
label_video_path.grid(row=0, column=0, padx=10, pady=10)

entry_video_path = tk.Entry(root, width=40)
entry_video_path.grid(row=0, column=1, padx=10, pady=10)

btn_browse = tk.Button(root, text="Browse", command=browse_file)
btn_browse.grid(row=0, column=2, padx=10, pady=10)


label_search_text = tk.Label(root, text="Search Text:")
label_search_text.grid(row=1, column=0, padx=10, pady=10)

entry_search_text = tk.Entry(root, width=40)
entry_search_text.grid(row=1, column=1, padx=10, pady=10)

btn_search = tk.Button(root, text="Search", command=search_and_display)
btn_search.grid(row=1, column=2, padx=10, pady=10)

result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
