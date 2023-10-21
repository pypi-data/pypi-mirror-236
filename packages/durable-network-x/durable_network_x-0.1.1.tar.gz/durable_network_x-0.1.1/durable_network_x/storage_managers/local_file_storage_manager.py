import os
from durable_network_x.storage_managers import StorageManager

class LocalFileStorageManager(StorageManager):
    """
    A local storage manager implementation using the file system.
    
    This class provides concrete implementations for basic storage operations 
    such as writing, reading, deleting, and checking the existence of data using 
    the local file system. All paths provided are considered relative to the 
    specified root directory.
    """
    
    def __init__(self, root_dir: str) -> None:
        """
        Initializes a new instance of the LocalFileStorageManager.
        
        :param root_dir: The root directory for the file storage.
        """
        super().__init__()
        self.__root_dir: str = root_dir

    def read(self, path: str, __default: str = "") -> str:
        """
        Reads data from the specified path. If the file is not found or any 
        other exception occurs, the default value is returned.
        
        :param path: The path from where data should be read, relative to the root directory.
        :param __default: The default value to return if the file is not found or an error occurs.
        :return: The data read from the path or the default value.
        """
        _path = os.path.join(self.__root_dir, path)
        try:
            with open(_path, 'r') as file:
                return file.read()
        except Exception as err:
            print(err)
            return __default
    
    def write(self, data: str, path: str):
        """
        Writes data to the specified path.
        
        If the directory doesn't exist, it gets created.
        
        :param data: The data to be written.
        :param path: The path where the data should be written, relative to the root directory.
        """
        _path = os.path.join(self.__root_dir, path)
        # Ensure the directory exists
        directory = os.path.dirname(_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"File {_path} has been written successfully.")
        with open(_path, 'w') as file:
            file.write(data)
    
    def delete(self, path: str):
        """
        Deletes the file at the specified path.
        
        If the file doesn't exist, an informational message is printed.
        
        :param path: The path of the file to be deleted, relative to the root directory.
        """
        _path = os.path.join(self.__root_dir, path)
        try:
            os.remove(_path)
            print(f"File {_path} has been deleted successfully.")
        except FileNotFoundError:
            print(f"File {_path} not found.")
    
    def exists(self, path: str) -> bool:
        """
        Checks if a file at the specified path exists.
        
        :param path: The path to check, relative to the root directory.
        :return: True if the file exists, False otherwise.
        """
        _path = os.path.join(self.__root_dir, path)
        return os.path.exists(_path)
