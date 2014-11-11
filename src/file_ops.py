class file_ops(object):
    """
    Static: Takes in the fully-qualified name of a file, opens it and returns a byte array representation
    :param file_name:
    :return array:
    """
    @staticmethod
    def file_to_bytes(file_name):
        # Open the file for reading and read the contents into a byte array
        file_content = open(file_name, 'r').read()
        return file_content

    """
    Static: Takes in a byte array representation of a file and saves it out as a Python program
    :param byte array of file, optional path to save file to, optional file output name:
    :return name of Python program:
    """
    @staticmethod
    def bytes_to_file(arr, path="", name="in_file.py"):
        # Add a trailing slash if a path was passed in but the user forgot to include one
        if len(path) > 0 and path[-1] != "/":
            path += "/"

        # Open a new empty file to write the contents to
        new_file = open(path + name, 'w')
        # Write the byte array to the file, Python will handle the conversion
        new_file.write(arr)
        new_file.close()
        return name

if __name__ == "__main__":
    print("This module cannot be run alone")