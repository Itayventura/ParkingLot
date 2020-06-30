from abc import ABC


class Image(ABC):

    #date_timr
    def __init__(self, source, dateTime):
        self.source = source
        self.dateTime = dateTime

    def get_dateTime(self):
        return self.dateTime

    def get_source(self):
        return self.source


class PathImage(Image):

    def __init__(self, path, dateTime):
        Image.__init__(self, path, dateTime)


class UrlImage(Image):
    def __init__(self, url, dateTime):
        Image.__init__(self, url, dateTime)


