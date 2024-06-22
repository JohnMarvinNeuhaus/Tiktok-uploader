import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

# Stelle sicher, dass der Import korrekt ist
try:
    from Tiktok_uploader import uploadVideo
except ImportError as e:
    print(f"Fehler beim Importieren von 'Tiktok_uploader': {e}")
    raise

session_id = "87214cb9062df9515024e0ae4ef82359"
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
                time.sleep(5)
        except KeyboardInterrupt:
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
            time.sleep(5)  # Verzögerung, um sicherzustellen, dass die Dateioperation abgeschlossen ist
            upload_to_tiktok(event.src_path)        

def upload_to_tiktok(file_path):
    try:
        with open(file_path, 'rb') as f:
            # Logging hinzufügen
            print(f"Versuche, Datei hochzuladen: {file_path}")
            uploadVideo(session_id, file_path, title, tags, verbose=True)
        print("Upload erfolgreich")
    except PermissionError as e:
        print(f"Fehler beim Öffnen der Datei (Permission denied): {e}")
    except Exception as e:
        print(f"Fehler beim Hochladen des Videos: {e}")


if __name__ == '__main__':
    w = Watcher()
    w.run()
