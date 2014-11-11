from connection_info import Connection_Info
from file_ops import file_ops
import socket, select, message, os, json

class AuxiliaryProcessor(object):
    def __init__(self):
        self.connection = Connection_Info(socket.gethostbyname(socket.gethostname()))
        self.ip_address = self.connection.get_ip()
        self.send_port = self.connection.get_send_port()
        self.listen_port = self.connection.get_listening_port()
        self.central_ip = ""
        self.jobs = []


    def run_file(self, file):
        module = __import__(file[:-3])
        try:
            return module.main()
        except AttributeError:
            return "Bad program format"

    def process(self, data, ip):
        data_dict = json.loads(data)

        if data_dict["flag"] == "j":
            in_file = file_ops.bytes_to_file(data_dict["body"], "")
            out = self.run_file(in_file)
            return_message = message.Message("r", out)
            print("Sending from file: " + in_file + " data: " + out)
            self.send_message(return_message)
            os.remove(in_file)

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
        self.socket_con.listen(5) # Queue up 5 connections, this is just the default
        self.socket_con.setblocking(False)  # opens the non blocking channel

        if self.socket_con:
            input = [self.socket_con]
            while True:
                # We're going to ignore output_ready and errors, but we need to stuff select's full output somewhere
                input_ready, output_ready, errors = select.select(input, [], [])

                for sock in input_ready:
                    # If the item in input_ready is our socket connection
                    if sock is self.socket_con:
                        client, address = sock.accept()
                        input.append(client)
                    else: # We have new input to process
                        # Decode the bytestream representing the program to be executed into a string so that it can be
                        # dumped into a .py for execution
                        data = sock.recv(self.connection.buffer).decode()
                        if data:
                            self.process(data, address[0])
                        else:
                            sock.close()
                            input.remove(sock)


if __name__ == "__main__":
    aux = AuxiliaryProcessor()
    aux.listening()
