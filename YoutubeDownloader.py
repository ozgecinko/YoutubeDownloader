# Download a youtube video into desktop

import tkinter as tk
from pytube import YouTube

window = tk.Tk()
window.geometry("{}x{}".format(500, 200))
window.configure(bg="#c39191")
window.title("Youtube Downloader")

logo = tk.PhotoImage(file="youtube.png")

link_label = tk.Label(window,text="Image",image=logo, justify=tk.CENTER, bg="#c39191")
link_label.grid(column=0, row=2, padx=5, pady=5)

link_label = tk.Label(window, text="Download Link", fg="#610606", width=15, bg="#c39191")
link_label.grid(column=0, row=0, padx=5, pady=5)

link_label = tk.Label(window, text="Save Video As", fg="#610606", width=15, bg="#c39191")
link_label.grid(column=0, row=1, padx=5, pady=5)

link_entry = tk.Entry(master=window, width=35)
link_entry.grid(column=1, row=0, padx=5)
name_entry = tk.Entry(master=window, width=35)
name_entry.grid(column=1, row=1, padx=5)

def downloader():
    link = link_entry.get()
    name = name_entry.get()
    # it'll downloaded given path
    path = r"/Users/ozgecinko/Desktop"
    extension = "mp4"
    yt = YouTube(link)
    yt_stream = yt.streams.filter(progressive=True, file_extension=extension).order_by('resolution').desc().first()
    yt_stream.download(path, filename=name)
    link_label = tk.Label(window, text="Downloaded!", fg="#610606", width=15, bg="#c39191")
    link_label.grid(column=1, row=3, padx=5, pady=5)


download_button = tk.Button(window, text="Download", command=downloader, fg="#610606", width=15)
download_button.grid(column=1, row=2)


window.mainloop()