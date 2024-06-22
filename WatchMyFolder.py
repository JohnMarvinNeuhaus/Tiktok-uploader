import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from Tiktok_uploader import uploadVideo
import requests


session_id = "87214cb9062df9515024e0ae4ef82359"
# file = "my_video.mp4"
title = "MY SUPER TITLE"
tags = ["Funny", "Joke", "fyp"]

class Watcher:
    DIRECTORY_TO_WATCH = r"D:\Einfach alles\Streaming\Arizona\Twitch\Clips"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(15)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            print(f"Received created event - {event.src_path}")
            upload_to_tiktok(event.src_path)



def upload_to_tiktok(file_path):
    url = "https://api.tiktok.com/upload"
    files = {'file': open(file_path, 'rb')}
    data = {'some': 'data'}

    uploadVideo(session_id, file_path, title, tags, verbose=True)

    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        print("Upload erfolgreich")
    else:
        print("Upload fehlgeschlagen")

if __name__ == '__main__':
    w = Watcher()
    w.run()