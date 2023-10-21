from abc import ABC, abstractmethod

class StorageManager(ABC):
    """
    Abstract base class representing a generic storage manager.
    
    This class provides an interface for basic storage operations, 
    such as writing, reading, deleting, and checking the existence of data.
    Implementations should provide concrete implementations for these operations.
    """
    
    @abstractmethod
    def write(self, data: any, path: str):
        """
        Writes the specified data to the specified path.
        
        :param data: The data to be written.
        :param path: The path where data should be written.
        :raises NotImplementedError: If this method is called on the abstract base class itself.
        """
        raise NotImplementedError("`instance(StorageManager).write()` is an abstract function. So it can not be called.")

    @abstractmethod
    def read(self, path: str, __default: str) -> any:
        """
        Reads data from the specified path. If data is not found, the default value is returned.
        
        :param path: The path from where data should be read.
        :param __default: The default value to return if data is not found.
        :return: The data read from the path or the default value if data is not found.
        :raises NotImplementedError: If this method is called on the abstract base class itself.
        """
        raise NotImplementedError("`instance(StorageManager).read()` is an abstract function. So it can not be called.")

    @abstractmethod
    def delete(self, path: str):
        """
        Deletes data from the specified path.
        
        :param path: The path from where data should be deleted.
        :raises NotImplementedError: If this method is called on the abstract base class itself.
        """
        raise NotImplementedError("`instance(StorageManager).delete()` is an abstract function. So it can not be called.")

    @abstractmethod
    def exists(self, path: str) -> bool:
        """
        Checks if the specified data exists.
        
        :param path: The path on which to check if the data exists.
        :return: True if the data exists, False otherwise.
        :raises NotImplementedError: If this method is called on the abstract base class itself.
        """
        raise NotImplementedError("`instance(StorageManager).exists()` is an abstract function. So it can not be called.")
