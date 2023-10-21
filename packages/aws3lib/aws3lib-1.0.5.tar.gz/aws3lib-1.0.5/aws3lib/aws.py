import json

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError


class ObjectMustBeNotNull(Exception):
    def __init__(self):
        super().__init__("Object must be not null")

class PolicyMustBeNotNull(Exception):
    def __init__(self):
        super().__init__("Policy must be not null")

class AWS3:
    """
    Class for managing AWS S3 storage

    AWS CLI must be configured

    Documentation: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
    """
    def __init__(self,
                 bucket: str,
                 default_object_name: str = "default_object_name",
                 endpoint: str = None):
        """
        :param bucket: Bucket name in AWS S3 storage
        :param default_object_name: Default object name, will be used if object_name arg is None
        :param endpoint: If you are using another S3 storage like Yandex Storage, Selectel etc. You must fill this arg, otherwise leave it.
        """
        if endpoint is None:
            self.__client = boto3.client(service_name="s3")
        else:
            self.__client = boto3.client(service_name="s3", endpoint_url=endpoint)

        self.bucket = bucket
        self.default_object_name = default_object_name

    def upload_file(self,
                    file_path: str,
                    object_name: str = None,
                    public: bool = True,
                    extra_args: dict = None,
                    config: TransferConfig = None) -> bool:
        """
        Method for uploading files via file path

        TransferConfig Docs - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig

        :param file_path: File path
        :param object_name: Object name (Name of the object that will be available on S3)
        :param public: Make this object public (Everyone can read this object)
        :param extra_args: Add extra args
        :param config: Add TransferConfig

        :return: File is uploaded as boolean. If error, returns False.
        """

        if extra_args is None:
            extra_args = {}
        try:
            if object_name is None:
                object_name = self.default_object_name

            if public:
                extra_args['ACL'] = 'public-read'

            self.__client.upload_file(file_path, self.bucket, object_name, ExtraArgs=extra_args, Config=config)

        except ClientError:
            return False
        return True

    def download_file(self,
                      file_path: str,
                      object_name: str,
                      config: TransferConfig = None) -> bool:
        """
        Method for downloading file to destination path

        TransferConfig Docs - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.TransferConfig

        :param file_path: File destination path
        :param object_name: Object name
        :param config: Add TransferConfig

        :return: File is downloaded as boolean. If error, returns False.
        """

        try:
            if object_name is None:
                raise ObjectMustBeNotNull()

            self.__client.download_file(self.bucket, object_name, file_path, Config=config)
        except ClientError:
            return False
        return True

    def create_presigned_url(self,
                             object_name: str,
                             expiration=3600) -> str | None:
        """
        Generate a presigned URL to share an S3 object

        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        if object_name is None:
            raise ObjectMustBeNotNull()

        try:
            response = self.__client.generate_presigned_url('get_object',
                                                            Params={'Bucket': self.bucket,
                                                                    'Key': object_name},
                                                            ExpiresIn=expiration)
        except ClientError:
            return None

        return response

    def get_bucket_acl(self) -> dict | None:
        """
        Get the bucket ACL

        :return: Bucket ACL as dict
        """

        try:
            response = self.__client.get_bucket_acl(Bucket=self.bucket)
        except ClientError:
            return None

        return response

    def put_bucket_policy(self, policy: dict) -> bool:
        """
        Update bucket policies

        Example:
        {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'AddPerm',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': f'arn:aws:s3:::{bucket_name}/*'
            }]
        }

        :param policy: Bucket Policy as dist
        :return: Is bucket policy updated status as boolean
        """

        if policy is None:
            raise PolicyMustBeNotNull()

        bucket_policy = json.dumps(policy)

        try:
            self.__client.put_bucket_policy(Bucket=self.bucket, Policy=bucket_policy)
        except ClientError:
            return False

        return True

    def delete_bucket_policy(self):
        """
        Delete all bucket policies
        """

        self.__client.delete_bucket_policy(Bucket=self.bucket)

    def get_bucket_cors(self) -> list | None:
        """
        Get bucket CORS rules

        :return: CORS rules as list
        """
        try:
            response = self.__client.get_bucket_cors(Bucket=self.bucket)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchCORSConfiguration':
                return []
            else:
                return None
        return response['CORSRules']

    def put_bucket_cors(self,
                        configuration: dict):
        """
        Update bucket CORS rules
        :param configuration: CORS rules as dict
        """
        try:
            self.__client.put_bucket_cors(Bucket=self.bucket,
                   CORSConfiguration=configuration)
        except ClientError:
            return