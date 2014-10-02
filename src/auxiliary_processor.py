from connection_info import *
from file_ops import file_ops
from stdout_redirect import stdout_redirect

class AuxiliaryProcessor(object):
    def __init__(self):
        self.ip_address = connection_info.Get_IP()
        self.send_port = connection_info.Get_Send_Port()
        self.listen_port = connection_info.Get_Listen_Port()

    def run_file(self, file):
        output = ""
        with stdout_redirect(stdout=output):
            exec(open(file).read())
        return output

    def process(self, data, ip):
        in_file = file_ops.bytes_to_file(data)
        result = self.run_file(in_file)
        #TODO: Chris, send result


if __name__ == "__main__":
    # TODO: Tory, put your listen method call here
    pass