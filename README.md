# fast-minio-service 🚀
## ▶ chunked uploads to minIO object storage, sqlAlchemy Neon DB serverless postgress.
### imp: clone ui project as a sibling folder next to fast-minio-service in same parent folder
#### to build a Docker environment: 
add a .env file having
- DATABASE_URL=""
- MINIO_ENDPOINT="minio" 
- MINIO_ACCESS_KEY=""
-  MINIO_SECRET_KEY=""

**MINIO_ENDPOINT** should be same as minio service name in docker compose file (so minio as default case) 
##### add 127.0.0.1  minio in hosts file
where again *minio* will be same minio service name in docker compose file
**DATABASE_URL** should be postgress or serverless postgress db URL (NeonDB) (https://neon.tech/)

WRT to docker compose file the folder structure should be
![image](https://github.com/user-attachments/assets/d662e415-a928-4b63-b935-ec1d72e36adb)


Now in frontend UI service add file .env.local having

NEXT_PUBLIC_API_BACKEND_SERVICE=http://127.0.0.1:<Port>/

where Port is mapped to backend service as in our default case 8080, so it will be NEXT_PUBLIC_API_BACKEND_SERVICE=http://127.0.0.1:8080/
#### Now finally

in the root fast-minio-service directory:
run 

![image](https://github.com/user-attachments/assets/240cc5f1-5167-44b2-8ea0-9c0e79bc813a)


**$ docker compose up -d --build** to build and start our services


*something like this*    

![image](https://github.com/user-attachments/assets/21145cc9-ce44-4f86-a0dd-120f5c9b7488)


