from PollyReports import *


class MyReport(Report):
    def __init__(self, *args, **kwargs):
        self.bottommargin = 15
        self.topmargin = 15
        self.leftmargin = 15
        super().__init__(self, *args, **kwargs)
