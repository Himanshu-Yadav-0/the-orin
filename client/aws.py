import boto3

class AWSService:
    s3_client = boto3.client('s3')
    
    def get_s3_files(self):
        objs = self.s3_client.list_objects(Bucket='orin-s3-demo-bucket')
        return [obj["Key"] for obj in objs["Contents"]]

    def upload_to_s3(self,file):
        self.s3_client.upload_fileobj(file.file,'orin-s3-demo-bucket',file.filename)
        return {
            "filename":file.filename,
            "content_type":file.content_type
            }
        
aws_service = AWSService()