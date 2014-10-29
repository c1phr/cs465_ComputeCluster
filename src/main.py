from auxiliary_processor import AuxiliaryProcessor
from central_server import CentralServer


def main():

    print("Welcome to Compute Cluster!\n")
    print("Are you a Server? (y/n)\n")
    input_identity = input()

    #if you're the server
    if input_identity == "y":
        #Fetch folder with list of job files
        server = CentralServer()

        #some stuff here

    #if you're not the server, you must be a satellite
    else:
        print("Starting Satellite...\n")
        print("Enter the IP of the server:\n")
        input_serverIP = input()
        satellite = AuxiliaryProcessor(input_serverIP)



    return