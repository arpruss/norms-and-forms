from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import subprocess

PDF_VIEWER = "C:/Users/alexander_pruss/AppData/Local/SumatraPDF/SumatraPDF.exe"
EDITOR = "c:/program files/notepad++/notepad++.exe"
DIRECTORY = "."
MAIN_FILE = "document"
TEMP_FILE = "__temp__" + MAIN_FILE

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".tex"):
            print("touched "+event.src_path)
            try:
                subprocess.run(["pdflatex", "-interaction=nonstopmode", "-jobname=" + TEMP_FILE, MAIN_FILE])
                os.unlink(MAIN_FILE + ".pdf")
                os.rename(TEMP_FILE + ".pdf", MAIN_FILE + ".pdf")
            except subprocess.CalledProcessError:
                print("error!")

# Create observer and event handler
observer = Observer()
event_handler = MyHandler()

# Set up observer to watch a specific directory
directory_to_watch = DIRECTORY
observer.schedule(event_handler, directory_to_watch, recursive=True)

# Start the observer
observer.start()

print("edit")
subprocess.Popen([EDITOR,])
print("pdf")
subprocess.Popen([PDF_VIEWER, "document.pdf"])
#observer.join() 

while True:
    time.sleep(0.25)
    pass
    
print("Done!")


# Keep the script running
#try:
#    while True:
#        time.sleep(0.25)
#        pass
#except KeyboardInterrupt:
#    observer.stop()
