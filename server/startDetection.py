import sys
import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mdetection import detectMovement
import logging

"""
  Watch a directory for new directories (each new dir is a new user), start processing the dir in a thread
"""
class DirCreatedEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        self.process(event)
    def process(self, event):
        threading.Thread(target=detectMovement, args=(event.src_path,)).start()

class DirWatcher:
    def __init__(self, src_path):
        self.__src_path = src_path
        self.__event_handler = DirCreatedEventHandler()
        self.__event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=False
        )

if __name__ == "__main__":
    baseDir = os.getcwd()
    logging.basicConfig(filename=baseDir + '/detector.log', format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info("Detection Initialized")
    src_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    DirWatcher(src_path).run()
