import boto3
from durable_network_x.storage_managers import StorageManager
from botocore.exceptions import ClientError

class S3StorageManager(StorageManager):
    """
    A StorageManager implementation for storing data on Amazon S3.
    
    This class provides methods to write, read, delete, and check existence
    of files in a specified S3 bucket.
    """

    def __init__(
        self, 
        bucket_name: str, 
        aws_access_key_id: str = None, 
        aws_secret_access_key: str = None
    ):
        """
        Initializes an instance of the S3StorageGraphML with the given parameters.

        :param bucket_name: Name of the S3 bucket to operate on.
        :param aws_access_key_id: AWS access key ID (optional if configured elsewhere).
        :param aws_secret_access_key: AWS secret access key (optional if configured elsewhere).
        """
        self.__bucket_name = bucket_name
        self.__s3 = boto3.client(
            's3', 
            aws_access_key_id=aws_access_key_id, 
            aws_secret_access_key=aws_secret_access_key
        )

    def write(self, data: str, path: str):
        """
        Writes the specified data to the given path on S3.

        :param data: The string data to be written.
        :param path: The S3 key/path where data should be written.
        """
        self.__s3.put_object(Body=data, Bucket=self.__bucket_name, Key=path)
        print(f"File {path} has been written successfully in bucket {self.__bucket_name}.")

    def read(self, path: str, __default: str = "") -> str:
        """
        Reads the data from the given path on S3. If data is not found, returns a default value.

        :param path: The S3 key/path from where data should be read.
        :param __default: The default value to return if data is not found.
        :return: The data read from the path or the default value if data is not found.
        """
        try:
            response = self.__s3.get_object(Bucket=self.__bucket_name, Key=path)
            data = response['Body'].read().decode('utf-8')
            return data
        except ClientError as ex:
            if ex.response.get("Error", dict()).get("Code") == 'NoSuchKey':
                print(f"File {path} not found in bucket {self.__bucket_name}.")
                return __default
            else:
                raise ex
            
    def delete(self, path: str):
        """
        Deletes the data from the given path on S3.

        :param path: The S3 key/path from where data should be deleted.
        """
        try:
            self.__s3.delete_object(Bucket=self.__bucket_name, Key=path)
            print(f"File {path} deleted successfully from bucket {self.__bucket_name}.")
        except ClientError as ex:
            if ex.response.get("Error", dict()).get("Code") == '404':
                print(f"File {path} not found in bucket {self.__bucket_name}.")
            else:
                raise ex
            
    def exists(self, path: str) -> bool:
        """
        Check if the given path exists in the S3 bucket.

        :param path: The path (key) of the object to check.
        :return: True if the object exists, False otherwise.
        """
        try:
            self.__s3.head_object(Bucket=self.__bucket_name, Key=path)
            return True
        except ClientError as ex:
            if ex.response.get("Error", dict()).get("Code") == '404':
                return False
            else:
                raise ex
