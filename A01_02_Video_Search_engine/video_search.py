import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from moviepy.video.io.VideoFileClip import VideoFileClip

class VideoPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player with Timestamps")

        # Video player variables
        self.video_path = None
        self.video_clip = None

        # GUI components
        self.create_widgets()

    def create_widgets(self):
        # Video selection button
        btn_select_video = tk.Button(self.root, text="Select Video", command=self.select_video)
        btn_select_video.pack(pady=10)

        # Text input for the word/dialog
        self.entry_word = tk.Entry(self.root, width=30)
        self.entry_word.pack(pady=10)

        # Button to find timestamps
        btn_find_timestamps = tk.Button(self.root, text="Find Timestamps", command=self.find_timestamps)
        btn_find_timestamps.pack(pady=10)

        # Timestamp listbox
        self.listbox_timestamps = tk.Listbox(self.root, selectmode=tk.SINGLE, width=30)
        self.listbox_timestamps.pack(pady=10)

        # Button to play video from selected timestamp
        btn_play_from_timestamp = tk.Button(self.root, text="Play from Timestamp", command=self.play_from_timestamp)
        btn_play_from_timestamp.pack(pady=10)

    def select_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
        if self.video_path:
            self.video_clip = VideoFileClip(self.video_path)
            messagebox.showinfo("Video Loaded", f"Video '{self.video_path}' loaded successfully.")

    def find_timestamps(self):
        if not self.video_clip:
            messagebox.showwarning("No Video Loaded", "Please select a video first.")
            return

        target_word = self.entry_word.get().lower()
        timestamps = []

        segment_duration = 5  # Adjust this based on your video characteristics

        for t in range(0, int(self.video_clip.duration), segment_duration):
            segment = self.video_clip.subclip(t, t + segment_duration)
            for i, frame in enumerate(segment.iter_frames(fps=1)):
                if target_word in str(frame).lower():
                    timestamps.append(t + i)

        self.listbox_timestamps.delete(0, tk.END)

        if timestamps:
            for ts in timestamps:
                self.listbox_timestamps.insert(tk.END, f"{int(ts // 60)}:{int(ts % 60):02d}")
        else:
            messagebox.showinfo("No Match", f"No occurrences of '{target_word}' found in the video.")

    def play_from_timestamp(self):
        if not self.video_clip:
            messagebox.showwarning("No Video Loaded", "Please select a video first.")
            return

        selected_index = self.listbox_timestamps.curselection()

        if not selected_index:
            messagebox.showwarning("No Timestamp Selected", "Please select a timestamp from the list.")
            return

        timestamp = float(self.listbox_timestamps.get(selected_index[0]))

        if 0 <= timestamp <= self.video_clip.duration:
            self.video_clip.subclip(timestamp, min(timestamp + 5, self.video_clip.duration)).preview()
        else:
            messagebox.showwarning("Invalid Timestamp", "Selected timestamp is outside the video duration.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()
