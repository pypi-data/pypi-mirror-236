from colorama import Fore as f
from datetime import datetime as dt


def get_time():
    now = dt.now()
    return f"{now.hour}:{now.minute}:{now.second}.{str(now.microsecond)[:3]}"


class Logger:
    def __int__(self, name):
        self.name = name

    def colored_msg(self, level, msg):
        print(f"{f.BLUE+self.name+f.RESET} {get_time()} - [{level}]: {msg}")

    def logs(self, msg):
        print(f"{f.BLUE+self.name+f.RESET} {get_time()} - {f.LIGHTYELLOW_EX}logs{f.RESET} {get_time()}: {msg}")

    def info(self, msg):
        self.colored_msg(f"{f.LIGHTMAGENTA_EX}INFO{f.RESET}", msg)

    def success(self,msg):
        self.colored_msg(f"{f.LIGHTGREEN_EX}SUCCESS{f.RESET}", msg)

    def warning(self,msg):
        self.colored_msg(f"{f.LIGHTYELLOW_EX}WARNING{f.RESET}", msg)

    def failed(self,msg):
        self.colored_msg(f"{f.LIGHTRED_EX}FAILED{f.RESET}", msg)

    def error(self,msg):
        self.colored_msg(f"{f.LIGHTRED_EX}ERROR{f.RESET}", msg)


