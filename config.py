import os
import sys

import yaml

class Config:
    def __init__(self, path):

        self.params = {}
        with open(os.path.join(sys.path[0], path), "r", encoding='utf-8') as stream:
            try:
                self.params = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def getparam(self, k):
        return self.params.get(k)

