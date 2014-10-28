import json
# noinspection PyUnresolvedReferences
from multiprocessing import Queue
from connection_info import *
from file_ops import file_ops
import socket, select, sys
from message import Message


class CentralServer(object):
    def __init__(self):
        self.ip_address = Connection_Info.Get_IP()
        self.send_port = Connection_Info.Get_Send_Port()
        self.listen_port = Connection_Info.Get_Listen_Port()
        self._peer_list = {}
        self.job_queue = Queue()

    def add_to_queue(self, file_name):
        self.job_queue.put(file_name)

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

        ** For Proof-of-Concept **
        aux_ip directs the ip to send the job to.

        to_send: a string containing the job to be sent.
        """
        # Socket options: use ipv4
        self.socket_cx = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
            )
        # More options: socket level, reuse socket
        self.socket_cx.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
            )
        self.socket_cx.connect(
            (aux_ip, self.listen_port)
            )
        self.socket_cx.send(to_send)
        self.socket_cx.close()

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

    def process(self, data, ip):
        data_dict = json.loads(data)

        #Connect
        if data_dict["flag"] == "c":
            if ip:
                self._peer_list[ip] = True

        #Disconnect
        if data_dict["flag"] == "d":
            if ip:
                del self._peer_list

        #Returning data
        if data_dict["flag"] == "r":
            print(ip + " --> " + data_dict["body"])
            self._peer_list[ip] = True

    def run(self):
        print(self.ip_address)

        while True:
            for ip, avail in self._peer_list:
                if avail:
                    self._peer_list[ip] = not avail
                    if len(self.job_queue) > 0:
                        # Operation will block if there is nothing in the queue until we have a job to execute
                        file = self.job_queue.get(block=True)
                        file_array = file_ops.file_to_bytes(file)
                        job_message = Message('j', (file, bytes(file_array, 'UTF-8')))
                        self.send(job_message, ip)

        # TODO: We need to run this in a separate thread somehow
        self.listening()

if __name__ == "__main__":
    serv = CentralServer()
    serv.run()
