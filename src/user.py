import json
# noinspection PyUnresolvedReferences
from multiprocessing import *
from connection_info import Connection_Info
from file_ops import file_ops
import socket, select, sys
from message import Message


class User(object):
    def __init__(self):
        self.connection = Connection_Info(socket.gethostbyname(socket.gethostname()))
        self.ip_address = self.connection.get_ip()
        self.send_port = self.connection.get_send_port()
        self.listen_port = self.connection.get_listening_port()
        self.server_ip = ""


    def send(self, to_send, aux_ip):
        """
        Sends a job to an available compute node. Jobs are just strings of
        python code which the target compute node will execute. They're
        stored in CentralServer.job_queue. To track which node we should
        send the job to, we have a "ready list," and a "working list;" the
        former tracks nodes which are ready to compute, and the latter
        tracks which nodes have had a job sent and still not gotten any
        response. When a compute node is ready, the server grabs a job from
        the end of the queue, sends it to that node (with this method), and
        then moves that entry in the ready list into the waiting list.

        aux_ip directs the ip to which the job should be sent.

        to_send: a message containing the job to be sent. send() converts the
        string into JSON.
        """

        # JSON-ify the message to be sent.
        #to_send.To_Json().encode()

        # Socket options: use ipv4
        self.socket_cx = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
            )
        # More options: socket level, reuse socket
        self.socket_cx.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
            )
        # Establish a connection
        self.socket_cx.connect(
            (aux_ip, self.listen_port)
            )
        self.socket_cx.send(to_send)
        self.socket_cx.close()

    def send_message(self, message):
        # Serialize the data into JSON so it can be sent over the socket
        to_send = message.To_Json().encode()
        self.socket_con2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # open socket
        self.socket_con2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_con2.connect((self.server_ip, self.connection.get_listening_port()))  # connect to particular ip
        self.socket_con2.send(to_send)  # send the JSON encoded message
        self.socket_con2.close()  # close the socket

    def listening(self):
        self.connection = Connection_Info(socket.gethostbyname(socket.gethostname()))
        self.socket_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # open socket
        self.socket_con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_con.bind((socket.gethostname(), self.connection.listening_port))
        self.socket_con.listen(5)
        self.socket_con.setblocking(False)  # opens the non blocking channel


        #If a connection has been established, receive the data
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

    def process(self, data, ip):
        data_dict = json.loads(data)

        #Returning data
        if data_dict["flag"] == "r":
            #prints original sent out data
            print("Raw data --> " + data)
            #prints new data it was just given by central server
            print("Returned data --> " + data_dict["body"])
            self._peer_list[ip] = True
            print(self._peer_list)

    #sends the file to be processed to the central server
    def send_file(self, file):
        #converts the file into bytes
        file_bytes = file_ops.file_to_bytes(file)
        #sends the file as a message to the central server to denote receiving from this user
        to_send = Message("f", file_bytes)
        self.send(to_send, self.server_ip)

    def connect(self, ip):
        """
        Connect to a central server using the given ip
        """
        # Connect to the central server and tell it how many threads we have
        self.server_ip = ip
        join_message = Message('uc', "")
        self.send_message(join_message)

    def run(self):
        pass

    def start_server(self):
        #Server_Run = Process(target=self.run)
        #Server_Run.start()
        #Server_List = Process(target=self.listening)
        #Server_List.start()
        pass
