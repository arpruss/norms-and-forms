from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".tex"):
            print("touched "+event.src_path)
            os.system("pdflatex document")

# Create observer and event handler
observer = Observer()
event_handler = MyHandler()

# Set up observer to watch a specific directory
directory_to_watch = "."
observer.schedule(event_handler, directory_to_watch, recursive=True)

# Start the observer
observer.start()

print("pdf")
os.system("start document.pdf")
print("pdf started")
#observer.join() 

while True:
    time.sleep(0.25)
    pass


# Keep the script running
#try:
#    while True:
#        time.sleep(0.25)
#        pass
#except KeyboardInterrupt:
#    observer.stop()
