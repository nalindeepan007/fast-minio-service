import uuid
import io
import os
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, File, UploadFile, HTTPException, Form, Depends, status
from fastapi.responses import JSONResponse
from app.db import getDb
from app.dbModel import FileMetadata
from app.minioStore import MinioStorage
router = APIRouter()

fileStore = MinioStorage()

@router.post("/")
async def uploadFiles(file: UploadFile = File(...),  fileName: str = Form(...), chunkNumber: int = Form(0), totalChunks: int = Form(1),  db: AsyncSession = Depends(getDb),):
  
    uploadedFiles = []

    isLast = (int(chunkNumber) + 1) == int(totalChunks)
 

    
    try:

        fileChunkName = f"{fileName}_{chunkNumber}"
        with open(f"{fileChunkName}", "wb") as buffer:
            buffer.write(await file.read())
        buffer.close()
        if isLast:

            fileId = str(uuid.uuid4())
            fileNameFinal = f"{fileId}_{fileName}"

            with open(f"{fileNameFinal}", "wb") as buffer:
                chunk = 0
                while chunk < totalChunks:
                    with open(f"{fileName}_{chunk}", "rb") as infile:
                        buffer.write(infile.read())
                        infile.close()
                    os.remove(f"{fileName}_{chunk}")
                    chunk = chunk + 1

            buffer.close()


            with open(fileNameFinal, "rb") as fileObj:
                mergedFile = fileObj.read()
            
            
            fileMetadata = FileMetadata(id=fileId, filename=fileNameFinal, size=len(mergedFile))
            db.add(fileMetadata)
            await db.commit()
            await db.refresh(fileMetadata)
            
      
            outF = fileStore.session.put_object(fileStore.bucketName,
                f"csvFiles/{fileNameFinal}",
                io.BytesIO(mergedFile),
            
                length=len(mergedFile),
                part_size=10*1024*1024,
                content_type="text/csv")
            
            fileMetadata.completed = True
            await db.commit()
            uploadedFiles.append(fileMetadata.filename)
            os.remove(f"{fileNameFinal}")
            return JSONResponse(
            {"message": "File Uploaded", "progress": "done", "size": len(mergedFile)}, status_code=status.HTTP_200_OK
        )
    except Exception as e:
        await db.rollback()
        print(f"printing error exception:-   {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed for {file.filename}: {str(e)}")
    
    

    return JSONResponse(
            {"progress": "ongoing", "status": chunkNumber}, status_code=status.HTTP_200_OK
        )

