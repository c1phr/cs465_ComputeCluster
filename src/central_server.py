from connection_info import *
from file_ops import file_ops

class CentralServer(object):
    def __init__(self):
        self.ip_address = Connection_Info.Get_IP()
        self.send_port = Connection_Info.Get_Send_Port()
        self.listen_port = Connection_Info.Get_Listen_Port()
        self.__file = "test.py"
        # self.job_queue = Queue( 10 )
        # Job queue has a max size of 10

    def send( self, to_send ):
        """
        Sends a job to an available compute node. 
        Jobs are just strings of python code which the target compute node
        will execute. They're stored in CentralServer.job_queue. 
        To track which node we should send the job to, we have a "ready
        list," and a "working list;" the former tracks nodes which are ready
        to compute, and the latter tracks which nodes have had a job sent
        and still not gotten any response. When a compute node is ready, the
        server grabs a job from the end of the queue, sends it to that
        node (with this method), and then moves that entry in the ready list into the waiting
        list. 

        to_send: a string containing the job to be sent. 
        """

    def move_to_wait( self, node ):
        """
        node: the node to move to 'waiting' is passed in
        """
        if self.get_ready_list.pop( node ):
            self.set_waiting_list(
                    self.get_waiting_list().append( node )
                    )
        else:
            sys.stderr.write( 'Error: specified node not in ready list' )

    def move_to_ready( self, node ):
        """
        node: the node to move to 'ready' is passed in
        """
        if self.get_waiting_list.pop( node ):
            self.set_ready_list(
                    self.get_ready_list().append( node )
                    )
        else:
            sys.stderr.write( 'Error: specified node not in ready list' )

    def run(self, file):
        '''
        This probably won't look remotely like this in the final version, and thus is not getting formal documentation
        '''
        if not file:
            file = self.__file
        file_array = file_ops.file_to_bytes(file)
        self.send(file_array)
        # TODO: Tory, call your listen function here