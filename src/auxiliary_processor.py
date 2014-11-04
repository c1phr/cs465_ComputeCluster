from connection_info import Connection_Info
from file_ops import file_ops
import socket, select, message, threading, os

class AuxiliaryProcessor(object):
    def __init__(self):
        self.connection = Connection_Info(socket.gethostbyname(socket.gethostname()))
        self.ip_address = self.connection.get_ip()
        self.send_port = self.connection.get_send_port()
        self.listen_port = self.connection.get_listening_port()
        self.central_ip = ""
        self.jobs = []
        self.avail_threads = 4
        self.__lock = threading.Lock()


    def run_file(self, file):
        module = __import__(file[:-3])
        return module.main()

    def process(self, data, ip):
        with self.__lock:
            in_file = file_ops.bytes_to_file(data, "processing/")
            out = self.run_file(in_file)
            return_message = message.Message("r", out)
            print("Sending from file: " + in_file + " data: " + out)
            os.remove(in_file)
            self.send_message(return_message)

    def connect(self, ip):
        """
        Connect to a central server using the given ip
        """
        # Connect to the central server and tell it how many threads we have
        self.central_ip = ip
        join_message = message.Message('pc', self.avail_threads)
        self.send_message(join_message)

    def send_message(self, message):
        # Serialize the data into JSON so it can be sent over the socket
        to_send = message.To_Json().encode()
        self.socket_con2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # open socket
        self.socket_con2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_con2.connect((self.central_ip, self.connection.get_listening_port()))  # connect to particular ip
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
                            #proc = self.__proc_pool.apply_async(self.process, [data, address[0]])
                            #proc.start()
                            proc = threading.Thread(target=self.process, args=(data, address[0],))
                            proc.start()
                            #self.process(data, address[0])
                        else:
                            sock.close()
                            input.remove(sock)


if __name__ == "__main__":
    aux = AuxiliaryProcessor()
    aux.listening()
