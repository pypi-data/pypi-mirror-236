import json

class Sample:

    def __init__(self, title, artistName, duration, releasedOn, url, albumName=None):
        self.title = title
        self.artistName = artistName
        self.albumName = albumName
        self.duration = duration
        self.releasedOn = releasedOn
        self.url = url

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True)