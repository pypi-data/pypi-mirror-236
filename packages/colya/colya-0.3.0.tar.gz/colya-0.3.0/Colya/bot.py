
from Colya.Config import Config
config = Config()
from Colya.service import Work

class Bot:
    def __init__(self) -> None:
        self.work = Work()
        
    def run(self):
        self.work.start()