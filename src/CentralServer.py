from Connection_Info import *

class CentralServer(object):
    def __init__(self):
        self.ip_address = self.Get_IP()
        self.send_port = self.Get_Send_Port()
        self.listen_port = self.Get_Listen_Port()

