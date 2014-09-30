class Connection_Info(object):
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.listening_port = 3001
        self.sending_port = 3002
        self.buffer = 1024

    def Get_IP(self):
        return self.ip_address

    def Get_Listen_Port(self):
        return self.listening_port

    def Get_Send_Port(self):
        return self.sending_port

    def Get_Buffer(self):
        return self.buffer