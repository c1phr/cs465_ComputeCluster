from auxiliary_processor import AuxiliaryProcessor
from central_server import CentralServer
from user import User
import os
import glob

def main():

    print("Welcome to Compute Cluster!\n")
    print("Are you a (s)erver, (p)rocessor or (u)ser? (s/p/u)\n")
    input_identity = input()

    #if you're the server
    if input_identity == "s":
        #Fetch folder with list of job files
        process_files = os.listdir("to_process")
        print(process_files)
        server = CentralServer()
        #server.start_server()
        print("Server IP: " + server.ip_address)
        # We don't need this part anymore since we have a separate peer connection
        # for i in process_files:
        #     server.add_to_queue("to_process/" + i)
        server.listening()
        return


    #if you're not the server, are you a satellite?
    elif input_identity == "p":
        print("Starting Satellite ...\n")
        print("Enter the IP of the server:\n")
        input_serverIP = input()
        satellite = AuxiliaryProcessor()
        satellite.connect(input_serverIP)
        satellite.listening()
        print("Waiting for incoming jobs...\n")

    else:
        print("Starting user mode...\n")
        print("Enter the IP of the server:\n")
        input_serverIP = input()
        print("Enter the path of the file that you would like to run:\n")
        input_file = input()
        user = User()
        user.connect(input_serverIP)
        user.send_file(input_file)
        user.listening()

    return

main()