from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.importers.spreadsheet import import_workbook
from app.schemas.core import SyncRunOut

router = APIRouter(prefix="/api/v1/import", tags=["import"])


@router.post("/spreadsheet", response_model=SyncRunOut)
async def import_spreadsheet(file: UploadFile, db: Session = Depends(get_db)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Hanya file .xlsx yang didukung")

    content = await file.read()
    run = import_workbook(db, file.filename, content)

    return SyncRunOut(
        id=run.sync_run_id,
        sourceFile=run.source_file,
        inserted=run.inserted,
        updated=run.updated,
        duplicate=run.duplicate,
        review=run.review,
        blocked=run.blocked,
        createdAt=run.created_at,
    )
