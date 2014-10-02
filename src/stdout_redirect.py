import sys

'''
    Initialize with the new stdout (probably file pointer)
    :param new_stdout:
'''

class StdoutRedirect(object):
    def __init__(self, stdout=None):
        self._stdout = stdout or sys.stdout        

    def __enter__(self):
        self.old_stdout= sys.stdout
        self.old_stdout.flush()
        sys.stdout= self._stdout

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush()
        sys.stdout = self.old_stdout