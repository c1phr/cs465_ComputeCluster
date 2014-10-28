
class Connection_Info(object):
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.listening_port = 3001
        self.sending_port = 3002
        self.buffer = 1024

    def get_ip(self):
        return self.ip_address

    def get_listening_port(self):
        return self.listening_port

    def get_send_port(self):
        return self.sending_port

    def get_buffer(self):
        return self.buffer