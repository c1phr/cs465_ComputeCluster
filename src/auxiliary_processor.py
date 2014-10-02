from connection_info import *
from file_ops import file_ops
from stdout_redirect import stdout_redirect

class AuxiliaryProcessor(object):
    def __init__(self):
        self.ip_address = Connection_Info.Get_IP()
        self.send_port = Connection_Info.Get_Send_Port()
        self.listen_port = Connection_Info.Get_Listen_Port()

    def run_file(self, file):
        output = ""
        with stdout_redirect(stdout=output):
            exec(open(file).read())
        return output

    def run(self):
        #TODO: Tory, put your listen method call here
        #Ryan: I assume that the data read in from the socket is a variable called "in_bytes"
        #Delete this when you actually write your section, I just don't want PyCharm angry with me
        in_bytes = ""
        in_file = file_ops.bytes_to_file(in_bytes)
        result = self.run_file(in_file)
        #TODO: Chris, send result