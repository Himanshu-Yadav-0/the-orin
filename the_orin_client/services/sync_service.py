from the_orin_server.services import cloud_client
from the_orin_client.utils.os_op import utils

DIR_PATH = "C:/Users/Himanshu Yadav/Documents/the-orin-SyncDIR"

class SyncService:
    
    def sync(self):
        files = cloud_client.get_presigned_diff(utils.get_dir_files(DIR_PATH))
        if files:
            for file in files:
                utils.download_file(file, DIR_PATH)

            print("Done Downloading")
        else:
            print("Nothing to download")
            
sync_service = SyncService()