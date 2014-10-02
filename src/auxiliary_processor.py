from connection_info import *
from file_ops import file_ops
from stdout_redirect import stdout_redirect
import socket, select

class AuxiliaryProcessor(object):
    def __init__(self):
        self.connection = connection_info(socket.gethostbyname(socket.gethostname()))
        self.ip_address = self.connection.Get_IP()
        self.send_port = self.connection.Get_Send_Port()
        self.listen_port = self.connection.Get_Listen_Port()

    def run_file(self, file):
        output = ""
        with stdout_redirect(stdout=output):
            exec(open(file).read())
        return output

    def process(self, data, ip):
        central_ip = ip
        in_file = file_ops.bytes_to_file(data)
        result = self.run_file(in_file)
        #open the socket, set connections, connect to servers listen port,
        #send process result, then close
        self.socket_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_a.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_a.connect(central_ip, self.listen_port)
        self.socket_a.send(result)
        self.socket_a.close()

    def listening(self):
        self.connection = connection_info(socket.gethostbyname(socket.gethostname()))
        self.socket_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # open socket
        self.socket_con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_con.bind((socket.gethostname(), self.connection.listening_port))
        self.socket_con.listen(15)  # up to fifteen users can message at once. Can change later
        self.socket_con.setblocking(False)  # opens the non blocking channel
        print(self.ip_address)

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


if __name__ == "__main__":
    aux = AuxiliaryProcessor()
    aux.listening()
