from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class PropertyItemSchema(BaseSchema):
    id: str
    title: str
    location: str
    price: int
    priceFormatted: str = Field(..., alias="price_formatted")
    installmentEstimate: str = Field(..., alias="installment_estimate")
    bedrooms: int = 2
    bathrooms: int = 1
    carports: int = 1
    buildingArea: int = Field(36, alias="building_area")
    surfaceArea: int = Field(60, alias="surface_area")
    electricityVa: int = Field(1300, alias="electricity_va")
    certificateType: str = Field("SHM", alias="certificate_type")
    tagText: str = Field(..., alias="tag_text")
    tagType: str = Field(..., alias="tag_type")
    imageUrl: str = Field(..., alias="image_url")
    developerName: Optional[str] = Field(None, alias="developer_name")
    addressDetail: Optional[str] = Field(None, alias="address_detail")
    isFavorite: bool = Field(False, alias="is_favorite")


class PropertyCreateSchema(BaseSchema):
    id: Optional[str] = Field(None, description="ID properti (opsional). Jika tidak diisi, ID akan dibuat secara otomatis oleh sistem (contoh: prop_1).")
    title: str
    location: str
    price: int
    bedrooms: int = 2
    bathrooms: int = 1
    carports: int = 1
    building_area: int = 36
    surface_area: int = 60
    electricity_va: int = 1300
    certificate_type: str = "SHM"
    tag_text: str = "Subsidi"
    tag_type: str = "SUBSIDI"
    image_url: str
    developer_name: Optional[str] = None
    address_detail: Optional[str] = None
    is_featured: bool = False


class ToggleFavoriteResponse(BaseSchema):
    id: str
    isFavorite: bool
    message: str


class KprCalculateRequest(BaseSchema):
    propertyPrice: int
    dpPercent: int = 10
    tenorYears: int = 20
    isSyariah: bool = False


class KprCalculationResponse(BaseSchema):
    propertyPrice: int
    dpPercent: int
    dpAmount: int
    loanAmount: int
    tenorYears: int
    isSyariah: bool
    interestRate: float
    monthlyInstallment: int
    totalPayment: int
    totalInterest: int
    principalPercentage: float
    interestPercentage: float
    recommendedMinIncome: int


class DocumentItemSchema(BaseSchema):
    id: str
    title: str
    description: str
    status: str
    statusLabel: str = Field(..., alias="status_label")
    fileName: Optional[str] = Field(None, alias="file_name")
    fileMeta: Optional[str] = Field(None, alias="file_meta")
    actionLabel: str = Field(..., alias="action_label")


class DocumentsSummaryResponse(BaseSchema):
    totalDocuments: int
    uploadedCount: int
    summaryText: str
    completionPercent: int
    documents: List[DocumentItemSchema]


class Sp3kStepSchema(BaseSchema):
    stepNumber: int = Field(..., alias="step_number")
    title: str
    subtitle: str
    status: str
    statusBadgeText: Optional[str] = Field(None, alias="status_badge_text")


class MortgageAdvisorSchema(BaseSchema):
    name: str
    role: str
    bank: str
    phone: str
    isOnline: bool = Field(True, alias="is_online")


class Sp3kDetailsSchema(BaseSchema):
    registrationNumber: str = Field(..., alias="registration_number")
    developer: str
    unitName: str = Field(..., alias="unit_name")
    approvedAmount: int = Field(..., alias="approved_amount")
    approvedAmountFormatted: str
    interestRateText: str = Field(..., alias="interest_rate_text")
    monthlyInstallment: int = Field(..., alias="monthly_installment")
    monthlyInstallmentFormatted: str
    tenorYears: int = Field(..., alias="tenor_years")
    dpPaid: int = Field(..., alias="dp_paid")
    dpPaidFormatted: str
    status: str = "APPROVED"
    akadDate: Optional[str] = Field(None, alias="akad_date")
    akadLocation: Optional[str] = Field(None, alias="akad_location")
    steps: List[Sp3kStepSchema] = []
    advisor: Optional[MortgageAdvisorSchema] = None


class AkadScheduleRequest(BaseSchema):
    registrationNumber: str
    akadDate: str
    akadLocation: str


class NotificationSchema(BaseSchema):
    id: int
    title: str
    message: str
    type: str = "INFO"


class UserProfileSchema(BaseSchema):
    id: str
    name: str
    greeting: Optional[str] = "Halo"
    subtitle: Optional[str] = None
    plafonEstimate: int = Field(0, alias="plafon_estimate")
    plafonEstimateFormatted: str
    financialScore: Optional[str] = Field(None, alias="financial_score")
    financialScoreGrade: Optional[str] = Field(None, alias="financial_score_grade")


class UserRegisterRequest(BaseSchema):
    email: str
    password: str
    fullName: str = Field(..., alias="full_name")
    phone: Optional[str] = None


class UserLoginRequest(BaseSchema):
    email: str
    password: str


class UserDataSchema(BaseSchema):
    id: str
    email: str
    fullName: str = Field(..., alias="full_name")
    phone: Optional[str] = None
    profile: Optional[UserProfileSchema] = None


class AuthResponseSchema(BaseSchema):
    accessToken: str = Field(..., alias="access_token")
    tokenType: str = Field("bearer", alias="token_type")
    user: UserDataSchema


class UserUpdateProfileRequest(BaseSchema):
    fullName: Optional[str] = Field(None, alias="full_name")
    phone: Optional[str] = None


class AdminActionResponse(BaseSchema):
    success: bool = True
    message: str
    data: Optional[dict] = None


class PropertyUpdateSchema(BaseSchema):
    title: Optional[str] = None
    location: Optional[str] = None
    price: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    carports: Optional[int] = None
    building_area: Optional[int] = None
    surface_area: Optional[int] = None
    electricity_va: Optional[int] = None
    certificate_type: Optional[str] = None
    tag_text: Optional[str] = None
    tag_type: Optional[str] = None
    image_url: Optional[str] = None
    developer_name: Optional[str] = None
    address_detail: Optional[str] = None
    is_featured: Optional[bool] = None
    is_favorite: Optional[bool] = None


class DocumentCreateSchema(BaseSchema):
    id: Optional[str] = Field(None, description="ID dokumen (opsional). Jika tidak diisi, ID akan dibuat secara otomatis oleh sistem (contoh: doc_1).")
    title: str
    description: str
    status: str = "REQUIRED"
    status_label: str = "Dibutuhkan"
    action_label: str = "Pilih Berkas"
    order_index: int = 0
    file_name: Optional[str] = None
    file_meta: Optional[str] = None


class DocumentUpdateSchema(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    status_label: Optional[str] = None
    action_label: Optional[str] = None
    order_index: Optional[int] = None


class Sp3kStepCreateSchema(BaseSchema):
    step_number: int
    title: str
    subtitle: str
    status: str = "UPCOMING"
    status_badge_text: Optional[str] = None


class Sp3kApplicationCreateSchema(BaseSchema):
    registration_number: Optional[str] = Field(None, description="Nomor registrasi SP3K (opsional). Jika tidak diisi, akan digenerate otomatis.")
    developer: str
    unit_name: str
    approved_amount: int
    interest_rate_text: str = "4.88% p.a. Fixed 3 Tahun"
    monthly_installment: int
    tenor_years: int = 20
    dp_paid: int = 0
    status: str = "APPROVED"
    akad_date: Optional[str] = None
    akad_location: Optional[str] = None
    steps: List[Sp3kStepCreateSchema] = []


class Sp3kApplicationUpdateSchema(BaseSchema):
    developer: Optional[str] = None
    unit_name: Optional[str] = None
    approved_amount: Optional[int] = None
    interest_rate_text: Optional[str] = None
    monthly_installment: Optional[int] = None
    tenor_years: Optional[int] = None
    dp_paid: Optional[int] = None
    status: Optional[str] = None
    akad_date: Optional[str] = None
    akad_location: Optional[str] = None


class MortgageAdvisorCreateSchema(BaseSchema):
    name: str
    role: str
    bank: str
    phone: str
    is_online: bool = True


class MortgageAdvisorUpdateSchema(BaseSchema):
    name: Optional[str] = None
    role: Optional[str] = None
    bank: Optional[str] = None
    phone: Optional[str] = None
    is_online: Optional[bool] = None


class UserProfileCreateSchema(BaseSchema):
    id: str = "user_default"
    name: str
    greeting: Optional[str] = "Halo"
    subtitle: Optional[str] = None
    plafon_estimate: int = 0
    financial_score: Optional[str] = None
    financial_score_grade: Optional[str] = None


class UserProfileUpdateSchema(BaseSchema):
    name: Optional[str] = None
    greeting: Optional[str] = None
    subtitle: Optional[str] = None
    plafon_estimate: Optional[int] = None
    financial_score: Optional[str] = None
    financial_score_grade: Optional[str] = None


class NotificationCreateSchema(BaseSchema):
    title: str
    message: str
    type: str = "INFO"

