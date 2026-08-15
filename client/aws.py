import boto3        
import logging
from botocore.exceptions import ClientError
from botocore.config import Config

class AWSService:
    s3_client = boto3.client('s3')
    BUCKET_NAME ='orin-s3-demo-bucket'
    
    def get_s3_files(self):
        objs = self.s3_client.list_objects(Bucket=self.BUCKET_NAME)
        return [obj["Key"] for obj in objs["Contents"]]

    def upload_to_s3(self,file):
        self.s3_client.upload_fileobj(file.file,self.BUCKET_NAME,file.filename)
        return {
            "filename":file.filename,
            "content_type":file.content_type
            }

    def create_presigned_url(self, object_name):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param region_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """
        region_name="ap-south-1"
        expiration=3600
        # Generate a presigned URL for the S3 object
        s3_client = boto3.client(
            's3',
            region_name=region_name,
            config=Config(
                signature_version='s3v4',
                s3={'addressing_style': 'virtual'},
            ),
        )
        try:
            response = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.BUCKET_NAME, 'Key': object_name},
                ExpiresIn=expiration,
            )
        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL
        return response
        
aws_service = AWSService()