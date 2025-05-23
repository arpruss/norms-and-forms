from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import subprocess
import sys

PDFLATEX = "pdflatex"
PDF_VIEWER = os.getenv('LOCALAPPDATA')+"/SumatraPDF/SumatraPDF.exe"
EDITOR = os.getenv('ProgramFiles')+"/notepad++/notepad++.exe"
EDITOR_FILE = ""
DIRECTORY = "./"
MAIN_FILE = "document"
TEMP_PREFIX = "__watch_temp__"
#MODE = "batchmode" 
MODE = "nonstopmode"

viewerStart = False

def viewer():
    subprocess.Popen([PDF_VIEWER, DIRECTORY+MAIN_FILE+".pdf"])

def pdflatex():
    try:
        subprocess.run([PDFLATEX, "-interaction=" + MODE, "-jobname=" + TEMP_FILE, "-output-directory=" +DIRECTORY, MAIN_FILE])
        try:
            os.unlink(os.path.join(DIRECTORY, MAIN_FILE + ".pdf"))
        except:
            pass
        print("renaming")
        os.rename(os.path.join(DIRECTORY, TEMP_FILE + ".pdf"), os.path.join(DIRECTORY, MAIN_FILE + ".pdf"))
        print("processed successfully")
        return True
    except FileNotFoundError:
        print("missing file")
        return False
    except subprocess.CalledProcessError:
        print("error processing!")
        return False

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.times = {}

    def on_modified(self, event):
        global viewerStart
        if not event.is_directory and event.src_path.lower().endswith(".tex"):
            try:
                t = os.path.getmtime(event.src_path)
                #print(event, t, time.time())
                if t + 1 < startTime:
                    print("oddly old mod time, ignoring")
                    return
                if event.src_path in self.times and t == self.times[event.src_path]:
                    print("duplicate event")
                    return
                self.times[event.src_path] = t
            except FileNotFoundError:
                try:
                    del self.times[event.src_path]
                    t = 0
                except KeyError:
                    pass

            time.sleep(0.25) # let the write get finished
            if pdflatex() and not viewerStart:
                viewerStart = True
                viewer()
            print("modified: "+event.src_path)
                
    def on_created(self,event):
        self.on_modified(event)

if len(sys.argv)>1:
    DIRECTORY,MAIN_FILE = os.path.split(os.path.splitext(sys.argv[1])[0])
    EDITOR_FILE = MAIN_FILE + ".tex"
if len(sys.argv)>2:
    EDITOR_FILE = sys.argv[2]
if len(DIRECTORY)==0:
    DIRECTORY = "./"
pdf = os.path.join(DIRECTORY,MAIN_FILE+".pdf")
TEMP_FILE = TEMP_PREFIX + MAIN_FILE

startTime = time.time()
viewerStart = True
if not os.path.exists(pdf):
    pdflatex()
    if not os.path.exists(pdf):
        print("Could not create "+pdf)
        viewerStart = False

print("Monitoring %s with main file %s.tex\n" % (DIRECTORY,MAIN_FILE))

observer = Observer()
handler = MyHandler()

observer.schedule(handler, DIRECTORY, recursive=True)
observer.start()

if EDITOR:
    subprocess.Popen([EDITOR, EDITOR_FILE] if len(EDITOR_FILE) else [EDITOR,])

if viewerStart:
    viewer()

print("Press CTRL-c to terminate")

while True:
    time.sleep(0.25)
    

