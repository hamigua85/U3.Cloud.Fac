import base


class PrintingTask(base.Task):
    def __init__(self, author, start, machine):
        self.author = author
        self.start = start
        self.end = None
        self.progress = None
        self.machine_info = machine
