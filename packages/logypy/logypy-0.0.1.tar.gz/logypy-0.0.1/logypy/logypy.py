import sys
import datetime

class LogyPy:
    def __init__(self, log_level="INFO", log_file=None):
        self.log_levels = {
            "DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL": 50
        }
        self.log_level = self.log_levels.get(log_level, self.log_levels["INFO"])
        self.log_file = log_file

    def log(self, level, message):
        current_time = datetime.datetime.now().strftime("%d/%b/%Y %H:%M:%S")
        log_message = f"[{current_time}] [{level}] {message}"
        if self.log_file:
            with open(self.log_file, 'a') as file:
                file.write(log_message + "\n")
        else:
            sys.stdout.write(log_message + "\n")
            sys.stdout.flush()

    def debug(self, message):
        if self.log_level <= self.log_levels["DEBUG"]:
            self.log("DEBUG", message)

    def info(self, message):
        if self.log_level <= self.log_levels["INFO"]:
            self.log("INFO", message)

    def warning(self, message):
        if self.log_level <= self.log_levels["WARNING"]:
            self.log("WARNING", message)

    def error(self, message):
        if self.log_level <= self.log_levels["ERROR"]:
            self.log("ERROR", message)

    def critical(self, message):
        if self.log_level <= self.log_levels["CRITICAL"]:
            self.log("CRITICAL", message)


