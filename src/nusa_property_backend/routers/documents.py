import shutil
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..config import UPLOAD_DIR
from ..database import get_db
from ..models import Document
from ..schemas import DocumentsSummaryResponse, DocumentItemSchema

router = APIRouter(prefix="/api/documents", tags=["Documents"])


@router.get("", response_model=DocumentsSummaryResponse)
def get_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.order_index.asc()).all()
    total = len(docs)
    uploaded = sum(1 for d in docs if d.status in ("VERIFIED", "UPLOADED"))
    pct = round((uploaded / total) * 100) if total > 0 else 0

    return DocumentsSummaryResponse(
        totalDocuments=total,
        uploadedCount=uploaded,
        summaryText=f"{uploaded} dari {total} Diunggah",
        completionPercent=pct,
        documents=docs
    )


@router.get("/{document_id}", response_model=DocumentItemSchema)
def get_document_by_id(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
    return doc


@router.post("/{document_id}/upload", response_model=DocumentItemSchema)
def upload_document(
    document_id: str,
    file: Optional[UploadFile] = File(None),
    status: Optional[str] = Form(None),
    status_label: Optional[str] = Form(None),
    action_label: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")

    if file:
        file_extension = file.filename.split(".")[-1] if "." in file.filename else "dat"
        saved_filename = f"{doc.id}_{file.filename}"
        file_path = UPLOAD_DIR / saved_filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        size_mb = file_path.stat().st_size / (1024 * 1024)
        doc.file_name = file.filename
        doc.file_meta = f"Ukuran berkas {size_mb:.1f} MB"
        doc.file_path = str(file_path)
        doc.status = "UPLOADED"
        doc.status_label = "Upload Berhasil"
        doc.action_label = "Ganti"

    if status:
        doc.status = status
    if status_label:
        doc.status_label = status_label
    if action_label:
        doc.action_label = action_label

    db.commit()
    db.refresh(doc)
    return doc


@router.get("/{document_id}/download")
def download_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.file_path:
        raise HTTPException(status_code=404, detail="File not found on server")
    return FileResponse(path=doc.file_path, filename=doc.file_name or "document.pdf")
