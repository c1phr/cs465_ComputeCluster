from random import randrange

class FileOps(object):
    def __init__(self):
        pass

    '''
    Takes in the fully-qualified name of a file, opens it and returns a byte array representation
    :param file_name:
    :return array:
    '''
    @staticmethod
    def file_to_bytes(file_name):
        file_content = open(file_name, 'r').read()
        return file_content


    '''
    Takes in a byte array representation of a file and saves it out as a Python program
    :param array of file contents:
    :return name of Python program:
    '''
    @staticmethod
    def bytes_to_file(arr):
        new_name = str(randrange(1000)) + '.py'
        new_file = open(new_name, 'w')
        new_file.write(arr)
        new_file.close()
        return new_name


#Showing off that this all works
if __name__ == "__main__":
    bytes = FileOps.file_to_bytes('FileOps.py')
    FileOps.bytes_to_file(bytes)
    print(bytes)