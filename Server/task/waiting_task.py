import base


class WaitingTask(base.Task):
    def __init__(self, author):
        self.author = author
