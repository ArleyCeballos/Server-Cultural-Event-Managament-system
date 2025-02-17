from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import JSONResponse

from app.schemas.bucket import FileData
from app.services.bucket import service_bucket

router = APIRouter()


@router.get("")
async def list_files_in_folder(prefix: Optional[str] = Query(None)):
    try:
        files = await service_bucket.get_all_files_in_folder(prefix)
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/download-file/{file_path:path}",
    response_class=JSONResponse,
    response_model=FileData,
)
async def download_file_from_gcs(file_path: str):
    try:
        file_data = await service_bucket.get_file_by_route(file_path)
        if file_data["file_bytes"] is not None:
            headers = {
                "Content-Disposition": f'attachment; filename={file_data["file_name"]}'
            }
            return Response(
                content=file_data["file_bytes"],
                headers=headers,
                media_type=file_data["content_type"],
            )
        else:
            return HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download-folder/{folder_path:path}")
async def download_files_from_folder(folder_path: str):
    try:
        files_data = await service_bucket.download_blobs_in_folder(folder_path)
        if files_data:
            return files_data
        else:
            raise HTTPException(
                status_code=404, detail="No files found in the specified folder"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-file/{file_path:path}")
async def delete_file_from_gcs(file_path: str):
    try:
        success = await service_bucket.delete_file_by_route(file_path)
        if success:
            return {"message": "File deleted successfully."}
        else:
            return {"message": "Failed to delete the file."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
