from Connection_Info import *
import queue.py

class CentralServer(object):
    def __init__(self):
        self.ip_address = self.Get_IP()
        self.send_port = self.Get_Send_Port()
        self.listen_port = self.Get_Listen_Port()
        self.job_queue = Queue( 10 )
        # Job queue has a max size of 10

