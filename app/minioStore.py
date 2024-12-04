import os
from minio import Minio
from dotenv import load_dotenv
import logging


logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MinioStorage:
    load_dotenv(dotenv_path=".env")
    MINIO_ACCESS = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
    def __init__(
        self, 
        endpointUrl: str = MINIO_ENDPOINT,
        accessKey: str = MINIO_ACCESS, 
        secretKey: str = MINIO_SECRET,
        bucketName: str = 'fileupload'
    ):
        """
        creating a session object for minIO and then creating a bucket if it doesnt exist
        
        """
        if not endpointUrl:
            raise ValueError("MinIO endpoint URL is required")
        
        if not accessKey or not secretKey:
            raise ValueError("Access key and secret key are required")
        try:
            self.endpointUrl = endpointUrl+":9000"
            self.accessKey = accessKey
            self.secretKey = secretKey
            self.bucketName = bucketName
            

            client = Minio(endpointUrl+":9000",
                            accessKey,
                            secretKey,
                            secure=False
                        )
        
        
            found = client.bucket_exists(bucketName)
            if not found:
                print(f"Creating Bucket {bucketName} first.... :)")
                client.make_bucket(bucketName)
            else:
                print(f"Bucket {bucketName} already exists")


            self.session = client
        
        except Exception as e:
            logger.error(f"Unexpected error during MinIO initialization: {str(e)}")
            raise
   
