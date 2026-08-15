from client.aws import aws_service

def get_presigned_diff(dir_files: list) -> list:
    s3_files = aws_service.get_s3_files()
    diff_files = [file for file in s3_files if file not in dir_files]
    presigned_urls = []
    for file in diff_files:
        presigned_urls.append(aws_service.create_presigned_url(object_name=file))
    return presigned_urls
        

