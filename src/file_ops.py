from random import randrange

class file_ops(object):
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
    def bytes_to_file(arr, path="", name="in_file.py"):
        if len(path) > 0 and path[-1] != "/":
            path += "/"
        new_file = open(path + name, 'w')
        new_file.write(arr)
        new_file.close()
        return name


#Showing off that this all works
if __name__ == "__main__":
    bytes = file_ops.file_to_bytes('file_ops.py')
    file_ops.bytes_to_file(bytes)
    print(bytes)