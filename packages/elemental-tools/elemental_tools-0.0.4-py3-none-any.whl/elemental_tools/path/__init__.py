import os


def Relative(origin: str = __file__):

    def relative(path):
        return os.path.join(os.path.dirname(origin), path)

