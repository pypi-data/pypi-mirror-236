import json
from array import array
from datetime import datetime


class SFResponseJob:

    def __init__(self):
        self.job_error: str = ''
        self.job_success: str = ''
        self.job_progress: int = 0

    def progress(self, progress: int):
        self.job_progress = progress

    def success(self, success: str):
        self.job_success = success

    def error(self, error: str):
        self.job_error = error

    def __str__(self):
        return json.dumps({"progress": self.job_progress, "success": self.job_success, "error": self.job_error})

    def __repr__(self):
        return self.__str__()
