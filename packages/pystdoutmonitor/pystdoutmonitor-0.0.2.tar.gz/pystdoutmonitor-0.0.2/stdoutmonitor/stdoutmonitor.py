import subprocess
from threading import Thread

class StdoutMonitorProcess:
    def __init__(self, name = "", callback = None):
        self.isOpen = False
        self._pid = -1
        self._callback = callback
        try:
            self._pid = int(subprocess.check_output(["pidof",name]).decode())
            self._proc = subprocess.Popen(["strace", "-p", str(self._pid), "-v", "-e", "write", "-s", "1000000"], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            self._thread = Thread(target=self._checkStraceOutputThread)
            self._thread.start()
            self.isOpen = True
        except:
            None

    def _checkStraceOutputThread(self):
        while True:
            line = self._proc.stdout.readline()
            if line != "":
                if self._callback != None:
                    beg = line.find('\"')
                    end = line.rfind('\"')
                    if beg >= 0 and end >= 0:
                        self._callback(line[(beg + 1):end].replace("\\n", "\n"))

    def __del__(self):
        if self.isOpen:
            self._proc.kill()
            self._thread.stop()
