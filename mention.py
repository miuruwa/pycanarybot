class MentionPy:
    def __init__(self):
        self.args = ['betabot']

    def getMent(self, string):
        return string in self.args