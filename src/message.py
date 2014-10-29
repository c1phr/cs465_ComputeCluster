import time, json


class Message(object):
    """
    Messages contain the chat data passed between individual Peers. Through
    the use of flags, they can also indicate other information about
    individual peer state
    """

    def __init__(self, flag, body):
        self.flag = flag
        self.body = body
        self.time = time.time()
        self.text_rep = ""

    def __str__(self):
        timestamp = str(time.localtime(self.time)[3]) + ":" \
                    + str(time.localtime(self.time)[4])
        if isinstance(self.body, str):
            return timestamp + " --- " + self.body
        else:
            return "No body"

    def Get_Flag(self):
        return self.flag

    def Get_Body(self):
        return self.body

    def Get_Timestamp(self):
        return self.time

    def To_Json(self):
        self.text_rep = self.__str__()  # Store the text representation before
        # serialization
        return json.dumps(self,
                          default=lambda o: o.__dict__, sort_keys=True, indent=4)
