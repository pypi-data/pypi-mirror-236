import string, random
import os
from datetime import datetime
import time


os.system("cls")


class core:
    def __init__(self):
        self.timestamp = lambda: str(datetime.fromtimestamp(time.time())).split(' ')[1]

    def consolelog(self, message, type=None):
        if type == "print":
            print('\x1b[38;2;73;73;73m[%s]\x1b[0m %s' % (self.timestamp(), message))
        elif type == "input":
            input('\x1b[38;2;73;73;73m[%s]\x1b[0m %s' % (self.timestamp(), message))
        else:
            print('\x1b[38;2;73;73;73m[%s]\x1b[0m %s' % (self.timestamp(), "ConsoleLog Function Error: Type Invalid Or Incorrect."))
            input()
            exit()