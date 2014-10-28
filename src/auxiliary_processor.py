from connection_info import *
from file_ops import file_ops
import socket, select, message, multiprocessing

class AuxiliaryProcessor(object):
    def __init__(self):
        self.ip_address = Connection_Info.Get_IP()
        self.send_port = Connection_Info.Get_Send_Port()
        self.listen_port = Connection_Info.Get_Listen_Port()
        self.central_ip = ""
        self.jobs = []
        self.avail_threads = multiprocessing.cpu_count()
        self.__proc_pool = multiprocessing.Pool()  # Creates a process pool with the number of cores the machine has

    def run_file(self, file):
        module = __import__(file[:-3])
        module.main()

    def process(self, data, ip):
        in_file = file_ops.bytes_to_file(data)
        self.run_file(in_file)
        file_arr = file_ops.file_to_bytes("out.txt")
        #open the socket, set connections, connect to servers listen port,
        #send process result, then close
        self.socket_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_a.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_a.connect((ip, self.listen_port))
        self.socket_a.send(file_arr)
        self.socket_a.close()

    def listening(self):
        self.connection = Connection_Info(socket.gethostbyname(socket.gethostname()))
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
                            # The following will send off the file to be processed async by a process from the pool
                            proc = self.__proc_pool.apply_async(self.process, [data, address[0]])
                        else:
                            sock.close()
                            input.remove(sock)


if __name__ == "__main__":
    aux = AuxiliaryProcessor()
    aux.listening()
