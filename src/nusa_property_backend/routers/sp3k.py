from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Sp3kApplication, Sp3kStep, MortgageAdvisor
from ..schemas import (
    Sp3kDetailsSchema,
    AkadScheduleRequest,
    Sp3kStepSchema,
    MortgageAdvisorSchema
)
from ..utils import format_rupiah

router = APIRouter(prefix="/api/sp3k", tags=["SP3K & Application Status"])


@router.get("", response_model=Sp3kDetailsSchema)
def get_sp3k_details(db: Session = Depends(get_db)):
    sp3k = db.query(Sp3kApplication).first()
    if not sp3k:
        raise HTTPException(status_code=404, detail="SP3K record not found")

    advisor = db.query(MortgageAdvisor).first()
    advisor_schema = MortgageAdvisorSchema.model_validate(advisor) if advisor else None

    steps_schema = [
        Sp3kStepSchema.model_validate(step)
        for step in sorted(sp3k.steps, key=lambda s: s.step_number)
    ]

    return Sp3kDetailsSchema(
        registrationNumber=sp3k.registration_number,
        developer=sp3k.developer,
        unitName=sp3k.unit_name,
        approvedAmount=sp3k.approved_amount,
        approvedAmountFormatted=format_rupiah(sp3k.approved_amount),
        interestRateText=sp3k.interest_rate_text,
        monthlyInstallment=sp3k.monthly_installment,
        monthlyInstallmentFormatted=format_rupiah(sp3k.monthly_installment),
        tenorYears=sp3k.tenor_years,
        dpPaid=sp3k.dp_paid,
        dpPaidFormatted=format_rupiah(sp3k.dp_paid),
        status=sp3k.status,
        akadDate=sp3k.akad_date,
        akadLocation=sp3k.akad_location,
        steps=steps_schema,
        advisor=advisor_schema
    )


@router.post("/schedule-akad", response_model=Sp3kDetailsSchema)
def schedule_akad(payload: AkadScheduleRequest, db: Session = Depends(get_db)):
    sp3k = db.query(Sp3kApplication).filter(
        Sp3kApplication.registration_number == payload.registrationNumber
    ).first()

    if not sp3k:
        raise HTTPException(
            status_code=404,
            detail=f"SP3K application with registration number '{payload.registrationNumber}' not found"
        )

    sp3k.akad_date = payload.akadDate
    sp3k.akad_location = payload.akadLocation

    for step in sp3k.steps:
        if step.step_number == 2:
            step.status = "FINISHED"
            step.status_badge_text = "Jadwal Terpilih"
        elif step.step_number == 3:
            step.status = "ACTIVE"
            step.status_badge_text = "Langkah Selanjutnya"

    db.commit()
    db.refresh(sp3k)

    return get_sp3k_details(db)


@router.get("/pdf")
def download_sp3k_pdf(db: Session = Depends(get_db)):
    sp3k = db.query(Sp3kApplication).first()
    if not sp3k:
        raise HTTPException(status_code=404, detail="SP3K application not found")
    reg_no = sp3k.registration_number

    pdf_content = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 180 >>
stream
BT
/F1 16 Tf
50 720 Td
(SURAT PENEGASAN PERSETUJUAN PENYEDIAAN KREDIT (SP3K)) Tj
/F1 12 Tf
0 -30 Td
(Nomor Registrasi: {reg_no}) Tj
0 -25 Td
(Status: DISETUJUI / APPROVED) Tj
0 -25 Td
(Platform: Nusa Property Indonesia) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 6
0000000000 65535 f 
0000000010 00000 n 
0000000059 00000 n 
0000000116 00000 n 
0000000224 00000 n 
0000000456 00000 n 
trailer
<< /Size 6 /Root 1 0 R >>
startxref
535
%%EOF
""".encode("latin-1")

    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="SP3K_{reg_no}.pdf"'
        }
    )
