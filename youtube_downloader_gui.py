import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube

class YouTubeDownloaderGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("YouTube Downloader")

        # URL input
        tk.Label(master, text="YouTube URL:").grid(row=0, column=0, sticky="w")
        self.url_var = tk.StringVar()
        tk.Entry(master, textvariable=self.url_var, width=50).grid(row=0, column=1, columnspan=3, padx=5, pady=5)
        tk.Button(master, text="Fetch", command=self.fetch_streams).grid(row=0, column=4, padx=5)

        # Resolution dropdown
        tk.Label(master, text="Resolution:").grid(row=1, column=0, sticky="w")
        self.res_var = tk.StringVar(value="720p")
        self.res_menu = tk.OptionMenu(master, self.res_var, "720p")
        self.res_menu.grid(row=1, column=1, padx=5, pady=5, sticky="we")

        # Download type radio buttons
        self.download_type = tk.StringVar(value="video")
        tk.Radiobutton(master, text="Video + Audio", variable=self.download_type, value="video").grid(row=2, column=0, sticky="w")
        tk.Radiobutton(master, text="Audio Only", variable=self.download_type, value="audio").grid(row=2, column=1, sticky="w")

        # Output file selection
        tk.Button(master, text="Choose Save Location", command=self.choose_location).grid(row=3, column=0, padx=5, pady=5)
        self.save_path_var = tk.StringVar()
        tk.Entry(master, textvariable=self.save_path_var, width=50).grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="we")

        # Download button
        tk.Button(master, text="Download", command=self.download).grid(row=4, column=0, columnspan=5, pady=10)

        self.streams = None

    def fetch_streams(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        try:
            yt = YouTube(url)
            progressive_streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            resolutions = [stream.resolution for stream in progressive_streams]
            if not resolutions:
                messagebox.showerror("Error", "No progressive streams available")
                return
            menu = self.res_menu['menu']
            menu.delete(0, 'end')
            for res in resolutions:
                menu.add_command(label=res, command=tk._setit(self.res_var, res))
            self.res_var.set(resolutions[0])
            self.streams = progressive_streams
            messagebox.showinfo("Success", "Resolutions fetched")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch streams: {e}")

    def choose_location(self):
        filetypes = [('MP4 files', '*.mp4'), ('All files', '*.*')]
        if self.download_type.get() == 'audio':
            filetypes = [('MP3 files', '*.mp3'), ('All files', '*.*')]
        path = filedialog.asksaveasfilename(defaultextension='.mp4', filetypes=filetypes)
        if path:
            self.save_path_var.set(path)

    def download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        save_path = self.save_path_var.get().strip()
        if not save_path:
            messagebox.showerror("Error", "Please choose a save location")
            return
        try:
            yt = YouTube(url)
            if self.download_type.get() == 'audio':
                audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                temp_file = audio_stream.download(filename='temp_audio')
                base, _ = os.path.splitext(save_path)
                final_path = base + '.mp3'
                os.rename(temp_file, final_path)
            else:
                res = self.res_var.get()
                stream = yt.streams.filter(progressive=True, file_extension='mp4', resolution=res).first()
                if not stream:
                    messagebox.showerror("Error", f"Resolution {res} not available")
                    return
                stream.download(filename=save_path)
            messagebox.showinfo("Done", "Download completed")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
