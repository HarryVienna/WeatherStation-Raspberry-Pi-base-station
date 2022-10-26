import yaml

class Config:
    def __init__(self, path):

        self.params = {}
        with open(path, "r", encoding='utf-8') as stream:
            try:
                self.params = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def getparam(self, k):
        return self.params.get(k)

