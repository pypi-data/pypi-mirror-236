'''
:authors: Hleb2702
:license: Apache License, Version 2.0, see LICENSE file

:copyright: (c) 2023 Hleb2702
'''

class WdonateError(Exception):
    def __init__(self, text):
        self.txt = text

