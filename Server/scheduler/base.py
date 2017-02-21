class Scheduler:
    def __init__(self):
        self.waiting_task = {}
        self.printing_task = {}
        self.online_machine = {}
