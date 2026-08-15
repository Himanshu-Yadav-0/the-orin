from client.aws import aws_client

class CloudService:

    def get_presigned_diff(self,dir_files: list) -> list:
        s3_files = aws_client.get_s3_files()
        diff_files = [file for file in s3_files if file not in dir_files]
        presigned_urls = []
        for file in diff_files:
            presigned_urls.append(aws_client.create_presigned_url(object_name=file))
        return presigned_urls
        

cloud_client = CloudService()

__all__ = [
    cloud_client
]