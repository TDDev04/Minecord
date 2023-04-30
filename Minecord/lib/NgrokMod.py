from threading import Thread, Event
from subprocess import Popen, PIPE
from os import name as sysname
from asyncio import sleep
from queue import Queue
from os import system

class NgrokRunner():
    def __init__(self):
        self.thread = None
        self.kill = Event()
        self.lines = Queue()

    def run(self, protocol, port):
        proc = Popen(["ngrok", protocol, port], stdout=PIPE)
        while proc.poll() == None and not self.kill.isSet():
            self.lines.put(proc.stdout.readline())

        if not self.kill.isSet():
            for line in proc.stdout.readlines(): self.lines.put(line)

    async def start(self, protocol, port):
        self.thread = Thread(target=self.run, args=(protocol, port,))
        self.thread.start()

        await sleep(1)
        while not self.lines.empty():
            line = self.lines.get().decode("utf-8")
            if line.find("url=") != -1:
                return line[line.rfind("://")+3:len(line)]

    async def quit(self):
        self.kill.set()
        if sysname == "posix": system("pkill ngrok")
        else: system("taskkill /F /IM ngrok.exe")
        self.thread.join()