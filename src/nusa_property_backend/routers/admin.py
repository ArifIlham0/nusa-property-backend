from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import (
    Property,
    Document,
    Sp3kApplication,
    Sp3kStep,
    MortgageAdvisor,
    Notification,
    UserProfile
)
from ..schemas import (
    AdminActionResponse,
    PropertyItemSchema,
    PropertyCreateSchema,
    PropertyUpdateSchema,
    DocumentItemSchema,
    DocumentCreateSchema,
    DocumentUpdateSchema,
    Sp3kDetailsSchema,
    Sp3kApplicationCreateSchema,
    Sp3kApplicationUpdateSchema,
    Sp3kStepCreateSchema,
    Sp3kStepSchema,
    MortgageAdvisorSchema,
    MortgageAdvisorCreateSchema,
    MortgageAdvisorUpdateSchema,
    UserProfileSchema,
    UserProfileCreateSchema,
    UserProfileUpdateSchema,
    NotificationSchema,
    NotificationCreateSchema
)
from ..utils import format_rupiah

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.post("/properties", response_model=PropertyItemSchema, status_code=status.HTTP_201_CREATED)
def admin_create_property(payload: PropertyCreateSchema, db: Session = Depends(get_db)):
    prop_id = payload.id
    if not prop_id:
        count = db.query(Property).count()
        prop_id = f"prop_{count + 1}"
        while db.query(Property).filter(Property.id == prop_id).first():
            count += 1
            prop_id = f"prop_{count + 1}"
    else:
        existing = db.query(Property).filter(Property.id == prop_id).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Property with ID '{prop_id}' already exists")

    price_formatted = format_rupiah(payload.price)
    installment_est = f"Cicilan mulai Rp {payload.price // 150_000_000},5 Jt/bln"

    new_prop = Property(
        id=prop_id,
        title=payload.title,
        location=payload.location,
        price=payload.price,
        price_formatted=price_formatted,
        installment_estimate=installment_est,
        bedrooms=payload.bedrooms,
        bathrooms=payload.bathrooms,
        carports=payload.carports,
        building_area=payload.building_area,
        surface_area=payload.surface_area,
        electricity_va=payload.electricity_va,
        certificate_type=payload.certificate_type,
        tag_text=payload.tag_text,
        tag_type=payload.tag_type.upper(),
        image_url=payload.image_url,
        developer_name=payload.developer_name,
        address_detail=payload.address_detail,
        is_favorite=False,
        is_featured=payload.is_featured
    )
    db.add(new_prop)
    db.commit()
    db.refresh(new_prop)
    return new_prop


@router.put("/properties/{property_id}", response_model=PropertyItemSchema)
def admin_update_property(property_id: str, payload: PropertyUpdateSchema, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail=f"Property '{property_id}' not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "tag_type" and value:
            value = value.upper()
        setattr(prop, field, value)

    if "price" in update_data and update_data["price"] is not None:
        prop.price_formatted = format_rupiah(prop.price)
        prop.installment_estimate = f"Cicilan mulai Rp {prop.price // 150_000_000},5 Jt/bln"

    db.commit()
    db.refresh(prop)
    return prop


@router.delete("/properties/{property_id}", response_model=AdminActionResponse)
def admin_delete_property(property_id: str, db: Session = Depends(get_db)):
    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        raise HTTPException(status_code=404, detail=f"Property '{property_id}' not found")

    db.delete(prop)
    db.commit()
    return AdminActionResponse(message=f"Property '{property_id}' successfully deleted")

@router.post("/documents", response_model=DocumentItemSchema, status_code=status.HTTP_201_CREATED)
def admin_create_document(payload: DocumentCreateSchema, db: Session = Depends(get_db)):
    doc_id = payload.id
    if not doc_id:
        count = db.query(Document).count()
        doc_id = f"doc_{count + 1}"
        while db.query(Document).filter(Document.id == doc_id).first():
            count += 1
            doc_id = f"doc_{count + 1}"
    else:
        existing = db.query(Document).filter(Document.id == doc_id).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Document with ID '{doc_id}' already exists")

    doc = Document(
        id=doc_id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        status_label=payload.status_label,
        action_label=payload.action_label,
        order_index=payload.order_index,
        file_name=payload.file_name,
        file_meta=payload.file_meta
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.put("/documents/{document_id}", response_model=DocumentItemSchema)
def admin_update_document(document_id: str, payload: DocumentUpdateSchema, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(doc, field, value)

    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/documents/{document_id}", response_model=AdminActionResponse)
def admin_delete_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found")

    db.delete(doc)
    db.commit()
    return AdminActionResponse(message=f"Document '{document_id}' successfully deleted")

@router.post("/sp3k", response_model=Sp3kDetailsSchema, status_code=status.HTTP_201_CREATED)
def admin_create_sp3k(payload: Sp3kApplicationCreateSchema, db: Session = Depends(get_db)):
    reg_number = payload.registration_number
    if not reg_number:
        import datetime, random
        year = datetime.datetime.now().year
        rand_num = random.randint(1000, 9999)
        reg_number = f"KPR-{year}-NUSA-{rand_num}"
        while db.query(Sp3kApplication).filter(Sp3kApplication.registration_number == reg_number).first():
            rand_num = random.randint(1000, 9999)
            reg_number = f"KPR-{year}-NUSA-{rand_num}"
    else:
        existing = db.query(Sp3kApplication).filter(
            Sp3kApplication.registration_number == reg_number
        ).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"SP3K with registration number '{reg_number}' already exists"
            )

    sp3k = Sp3kApplication(
        registration_number=reg_number,
        developer=payload.developer,
        unit_name=payload.unit_name,
        approved_amount=payload.approved_amount,
        interest_rate_text=payload.interest_rate_text,
        monthly_installment=payload.monthly_installment,
        tenor_years=payload.tenor_years,
        dp_paid=payload.dp_paid,
        status=payload.status,
        akad_date=payload.akad_date,
        akad_location=payload.akad_location
    )
    db.add(sp3k)
    db.flush()

    for step_data in payload.steps:
        step = Sp3kStep(
            registration_number=sp3k.registration_number,
            step_number=step_data.step_number,
            title=step_data.title,
            subtitle=step_data.subtitle,
            status=step_data.status,
            status_badge_text=step_data.status_badge_text
        )
        db.add(step)

    db.commit()
    db.refresh(sp3k)

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


@router.put("/sp3k/{registration_number}", response_model=AdminActionResponse)
def admin_update_sp3k(registration_number: str, payload: Sp3kApplicationUpdateSchema, db: Session = Depends(get_db)):
    sp3k = db.query(Sp3kApplication).filter(
        Sp3kApplication.registration_number == registration_number
    ).first()
    if not sp3k:
        raise HTTPException(status_code=404, detail=f"SP3K '{registration_number}' not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sp3k, field, value)

    db.commit()
    return AdminActionResponse(message=f"SP3K '{registration_number}' updated successfully")


@router.post("/sp3k/{registration_number}/steps", response_model=Sp3kStepSchema, status_code=status.HTTP_201_CREATED)
def admin_add_sp3k_step(registration_number: str, payload: Sp3kStepCreateSchema, db: Session = Depends(get_db)):
    sp3k = db.query(Sp3kApplication).filter(
        Sp3kApplication.registration_number == registration_number
    ).first()
    if not sp3k:
        raise HTTPException(status_code=404, detail=f"SP3K '{registration_number}' not found")

    step = Sp3kStep(
        registration_number=registration_number,
        step_number=payload.step_number,
        title=payload.title,
        subtitle=payload.subtitle,
        status=payload.status,
        status_badge_text=payload.status_badge_text
    )
    db.add(step)
    db.commit()
    db.refresh(step)
    return Sp3kStepSchema.model_validate(step)


@router.delete("/sp3k/{registration_number}", response_model=AdminActionResponse)
def admin_delete_sp3k(registration_number: str, db: Session = Depends(get_db)):
    sp3k = db.query(Sp3kApplication).filter(
        Sp3kApplication.registration_number == registration_number
    ).first()
    if not sp3k:
        raise HTTPException(status_code=404, detail=f"SP3K '{registration_number}' not found")

    db.delete(sp3k)
    db.commit()
    return AdminActionResponse(message=f"SP3K '{registration_number}' successfully deleted")

@router.post("/advisors", response_model=MortgageAdvisorSchema, status_code=status.HTTP_201_CREATED)
def admin_create_advisor(payload: MortgageAdvisorCreateSchema, db: Session = Depends(get_db)):
    advisor = MortgageAdvisor(
        name=payload.name,
        role=payload.role,
        bank=payload.bank,
        phone=payload.phone,
        is_online=payload.is_online
    )
    db.add(advisor)
    db.commit()
    db.refresh(advisor)
    return MortgageAdvisorSchema.model_validate(advisor)


@router.put("/advisors/{advisor_id}", response_model=MortgageAdvisorSchema)
def admin_update_advisor(advisor_id: int, payload: MortgageAdvisorUpdateSchema, db: Session = Depends(get_db)):
    advisor = db.query(MortgageAdvisor).filter(MortgageAdvisor.id == advisor_id).first()
    if not advisor:
        raise HTTPException(status_code=404, detail=f"Advisor ID {advisor_id} not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(advisor, field, value)

    db.commit()
    db.refresh(advisor)
    return MortgageAdvisorSchema.model_validate(advisor)


@router.delete("/advisors/{advisor_id}", response_model=AdminActionResponse)
def admin_delete_advisor(advisor_id: int, db: Session = Depends(get_db)):
    advisor = db.query(MortgageAdvisor).filter(MortgageAdvisor.id == advisor_id).first()
    if not advisor:
        raise HTTPException(status_code=404, detail=f"Advisor ID {advisor_id} not found")

    db.delete(advisor)
    db.commit()
    return AdminActionResponse(message=f"Advisor ID {advisor_id} successfully deleted")

@router.post("/user/profile", response_model=UserProfileSchema, status_code=status.HTTP_201_CREATED)
def admin_create_user_profile(payload: UserProfileCreateSchema, db: Session = Depends(get_db)):
    existing = db.query(UserProfile).filter(UserProfile.id == payload.id).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"User profile with ID '{payload.id}' already exists. Use PUT to update.")

    user = UserProfile(
        id=payload.id,
        name=payload.name,
        greeting=payload.greeting,
        subtitle=payload.subtitle,
        plafon_estimate=payload.plafon_estimate,
        financial_score=payload.financial_score,
        financial_score_grade=payload.financial_score_grade
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserProfileSchema(
        id=user.id,
        name=user.name,
        greeting=user.greeting,
        subtitle=user.subtitle,
        plafonEstimate=user.plafon_estimate or 0,
        plafonEstimateFormatted=format_rupiah(user.plafon_estimate or 0),
        financialScore=user.financial_score,
        financialScoreGrade=user.financial_score_grade
    )


@router.put("/user/profile/{user_id}", response_model=UserProfileSchema)
def admin_update_user_profile(user_id: str, payload: UserProfileUpdateSchema, db: Session = Depends(get_db)):
    user = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User profile '{user_id}' not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return UserProfileSchema(
        id=user.id,
        name=user.name,
        greeting=user.greeting,
        subtitle=user.subtitle,
        plafonEstimate=user.plafon_estimate or 0,
        plafonEstimateFormatted=format_rupiah(user.plafon_estimate or 0),
        financialScore=user.financial_score,
        financialScoreGrade=user.financial_score_grade
    )

@router.post("/notifications", response_model=NotificationSchema, status_code=status.HTTP_201_CREATED)
def admin_create_notification(payload: NotificationCreateSchema, db: Session = Depends(get_db)):
    notif = Notification(
        title=payload.title,
        message=payload.message,
        type=payload.type.upper()
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return NotificationSchema.model_validate(notif)


@router.delete("/notifications/{notification_id}", response_model=AdminActionResponse)
def admin_delete_notification(notification_id: int, db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail=f"Notification ID {notification_id} not found")

    db.delete(notif)
    db.commit()
    return AdminActionResponse(message=f"Notification ID {notification_id} successfully deleted")


@router.post("/clear-all-data", response_model=AdminActionResponse)
def admin_clear_all_data(db: Session = Depends(get_db)):
    """Mengosongkan semua data dari seluruh tabel tanpa merusak skema tabel."""
    db.query(Sp3kStep).delete()
    db.query(Sp3kApplication).delete()
    db.query(Property).delete()
    db.query(Document).delete()
    db.query(MortgageAdvisor).delete()
    db.query(Notification).delete()
    db.query(UserProfile).delete()
    db.commit()
    return AdminActionResponse(message="All application data successfully cleared. Database is now pure and empty.")
