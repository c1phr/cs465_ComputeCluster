from connection_info import *
from file_ops import file_ops
from stdout_redirect import stdout_redirect
import socket, select

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

    def listening(self):
        self.connection = connection_info(socket.gethostbyname(socket.gethostname()))
        self.socket_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # open socket
        self.socket_con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_con.bind((socket.gethostname(), self.connection.listening_port))
        self.socket_con.listen(15)  # up to fifteen users can message at once. Can change later
        self.socket_con.setblocking(False)  # opens the non blocking channel

        if self.socket_con:
            input = [self.socket_con]
            while True:
                input_ready, output_ready, errors = select.select(input, [], [])

                for sock in input_ready:
                    if sock is self.socket_con:
                        client, address = sock.accept()
                        input.append(client)
                    else:
                        data = sock.recv(self.connection.buffer).decode()
                        if data:
                            self.process(data, address[0])
                        else:
                            sock.close()
                            input.remove(sock)