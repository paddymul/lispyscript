import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
projects = {
    'lispy' : {
        'input': '.',
        'output' : '.'
        }
    }

def build(input_, output_):

    #command = "lispy src/lispy.ls lib/lispy.js && lispy src/repl.ls
    #lib/repl.js && lispy src/node.ls lib/node.js && lispy
    #src/browser.ls lib/browser.js"
    command = "lispy %s %s" % (input_, output_)
    print command
    proc = subprocess.Popen(command, shell=True,
                            stdout=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    data = proc.communicate()
    print data[0]
    print data[1]

pairs = [
    ['src/lispy.ls',   'lib/lispy.js'],
    ['src/repl.ls',    'lib/repl.js'],
    ['src/node.ls',    'lib/node.js'],
    ['src/browser.ls', 'lib/browser.js'],
    ['test/test.ls', 'test/test.js']
    ]

def build_all():
    for p in pairs:
        build(p[0], p[1])

class MyHandler(PatternMatchingEventHandler):
    def __init__(self, inputs, outputs):
        super(MyHandler, self).__init__(
            patterns=["*.ls"], case_sensitive=True)
        self.inputs = inputs
        self.outputs = outputs

    def on_any_event(self, event):
        if "#" in event.src_path:
            return
        print event
        build_all()

if __name__ == "__main__":
    """
    usage:
    python build.py build -builds all projects once
    python build.py watch - builds all projects once, then watches for changes.
    """
    if len(sys.argv) >= 2 and  sys.argv[1] == "build":
        build_all()
    else:
        build_all()
        observer = Observer()
        for project in projects:
            inputs = projects[project]['input']
            outputs = projects[project]['output']
            event_handler = MyHandler(inputs, outputs)
            print inputs
            observer.schedule(event_handler, path=inputs, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
