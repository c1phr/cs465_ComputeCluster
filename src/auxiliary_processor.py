from connection_info import *
from file_ops import file_ops
from stdout_redirect import stdout_redirect
import socket, select, message

class AuxiliaryProcessor(object):
    def __init__(self):
        self.ip_address = Connection_Info.Get_IP()
        self.send_port = Connection_Info.Get_Send_Port()
        self.listen_port = Connection_Info.Get_Listen_Port()
        self.central_ip = ""
        self.avail_threads = 4

    def run_file(self, file):
        output = ""
        with stdout_redirect(stdout=output):
            exec(open(file).read())
        return output

    def process(self, data, ip):
        in_file = file_ops.bytes_to_file(data)
        result = self.run_file(in_file)
        #TODO: Chris, send result

    def connect(self, ip):
        # Connect to the central server and tell it how many threads we have
        join_message = message.Message('c', self.avail_threads)
        self.send_message(join_message)


    def send_message(self, message):
        to_send = message.To_Json().encode()  # Serialize the data into JSON so it can
        # be sent over the socket

        self.socket_con2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # open socket
        self.socket_con2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_con2.connect((self.central_ip, self.connection.Get_Listen_Port()))  # connect to particular ip
        self.socket_con2.send(to_send)  # send the JSON encoded message
        self.socket_con2.close()  # close the socket


    def listening(self):
        self.connection = Connection_Info(socket.gethostbyname(socket.gethostname()))
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


if __name__ == "__main__":
    pass # TODO: We should probably remove this if we have an interface