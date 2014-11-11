import json
import socket
import select
import queue

from connection_info import Connection_Info
from file_ops import file_ops
from message import Message


class CentralServer(object):
    def __init__(self):
        self.connection = Connection_Info(socket.gethostbyname(socket.gethostname()))
        self.ip_address = self.connection.get_ip()              #grabs it owns ip
        self.send_port = self.connection.get_send_port()        #grabs the send to send through
        self.listen_port = self.connection.get_listening_port() #grabs listening port
        self.lock = 0                   #locking mechanism
        self._peer_list = {}            #grabs a list of aux peers that are connected currently
        self.job_queue = queue.Queue()  #Holds the queue for the files to be processed
        self._user_list = []            #holds the list of suers connected
        self._user_job_table = {}  # {aux_ip, user_ip} -> Used so we know what user gets output from who

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

    def listening(self):        #opens the listening line
        self.connection = Connection_Info(socket.gethostbyname(socket.gethostname()))
        self.socket_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # open socket
        self.socket_con.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_con.bind((socket.gethostname(), self.connection.listening_port))
        self.socket_con.listen(15)  # up to fifteen users can message at once. Can change later
        self.socket_con.setblocking(False)  # opens the non blocking channel

        #if something came in, process it
        if self.socket_con:
            input = [self.socket_con]
            while True:
                input_ready, output_ready, errors = select.select(input, [], [])

                for sock in input_ready:
                    if sock is self.socket_con:
                        client, address = sock.accept()
                        input.append(client)
                    else:
                        data = sock.recv(self.connection.buffer).decode()   #decode the message out of JSON
                        if data:
                            self.process(data, address[0])  #process the data that came in from particualr ip
                        else:
                            sock.close()        #close out the socket
                            input.remove(sock)  #Remove the socket

                if len(self._peer_list) > 0:    #if there is a peer connected, send a job
                    for ip, avail in self._peer_list.items():
                        if avail:   #if peer is available, send net job
                            # Lock the aux processor so it doesn't get more jobs until this one is done
                            self._peer_list[ip] = False
                            if (self.job_queue.qsize()) > 0:    #if jobs are currently waiting
                                # Operation will block if there is nothing in the queue until we have a job to execute
                                job = self.job_queue.get()  #get the next job fro the queue
                                file_array = file_ops.file_to_bytes(job[1]) #convert the file to bytes
                                job_message = Message('j', bytes(file_array, 'UTF-8'))  #create the message with the job
                                print("Sending job from: " + job[0])
                                self._user_job_table[ip] = job[0]   #gets the next ip from the table
                                self.send(job_message, ip)      #sends file to working ip

    def process(self, data, ip):
        data_dict = json.loads(data)    #convert data to JSON standard

        # Processor Connection
        if data_dict["flag"] == "pc":
            if ip:
                self._peer_list[ip] = True
                print(ip + " connected!")

        #User Connection
        if data_dict["flag"] == "uc":
            if ip:
                self._user_list.append(ip)
                print("User connected from: " + ip)

        #Disconnect
        if data_dict["flag"] == "d":
            if ip:
                del self._peer_list[ip]

        #Returning data
        if data_dict["flag"] == "r":
            print("From: " + ip + "For: " + self._user_job_table[ip] + " --> " + data_dict["body"])
            # Forward the message onto the user and remove their relation in the user job table
            self.send(data, self._user_job_table[ip])
            del self._user_job_table[ip]
            self._peer_list[ip] = True  # Set the flag for the aux processor so it can do more work

        #Recieving File
        if data_dict["flag"] == "f":
            print("Recieved file from " + ip)
            self.job_queue.put([ip, data_dict["body"]])