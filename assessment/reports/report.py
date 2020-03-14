from assessment.reports.funit_dscd_er import funit_dscd_er


# from PollyReports import *


class ReportGenerator(object):
    def __init__(self, name, format, param):
        self.name = name
        self.format = format
        self.param = param

    def generate(self):
        return getattr(self, '%s' % self.name)(self.format, self.param)

    funit_dscd_er = funit_dscd_er
