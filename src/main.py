from auxiliary_processor import AuxiliaryProcessor
from central_server import CentralServer
import os
import glob

# modules = glob.glob(os.path.dirname("to_process")+"/*.py")
# __all__ = [ os.path.basename(f)[:-3] for f in modules]

def main():

    print("Welcome to Compute Cluster!\n")
    print("Are you a Server? (y/n)\n")
    input_identity = input()

    #if you're the server
    if input_identity == "y":
        #Fetch folder with list of job files
        process_files = os.listdir("to_process")
        print(process_files)
        server = CentralServer()
        server.start_server()
        print("Server IP: " + server.ip_address)
        for i in process_files:
            server.add_to_queue("to_process/" + i)
        return


    #if you're not the server, you must be a satellite
    else:
        print("Starting Satellite ...\n")
        print("Enter the IP of the server:\n")
        input_serverIP = input()
        satellite = AuxiliaryProcessor(input_serverIP)
        satellite.connect(input_serverIP)
        satellite.listening()
        print("Waiting for incoming jobs...\n")

    return

main()