from fastapi import APIRouter, Query
from ..schemas import KprCalculateRequest, KprCalculationResponse
from ..utils import calculate_kpr

router = APIRouter(prefix="/api/kpr", tags=["KPR Calculator"])


@router.post("/calculate", response_model=KprCalculationResponse)
def calculate_mortgage(payload: KprCalculateRequest):
    result = calculate_kpr(
        price=payload.propertyPrice,
        dp_percent=payload.dpPercent,
        tenor_years=payload.tenorYears,
        is_syariah=payload.isSyariah
    )
    return KprCalculationResponse(**result)


@router.get("/calculate", response_model=KprCalculationResponse)
def calculate_mortgage_get(
    propertyPrice: int = Query(450_000_000, description="Property price in IDR"),
    dpPercent: int = Query(10, ge=5, le=50, description="Down Payment percentage"),
    tenorYears: int = Query(20, ge=1, le=30, description="Tenor in years"),
    isSyariah: bool = Query(False, description="True for Syariah Murabahah margin, False for conventional fixed")
):
    result = calculate_kpr(
        price=propertyPrice,
        dp_percent=dpPercent,
        tenor_years=tenorYears,
        is_syariah=isSyariah
    )
    return KprCalculationResponse(**result)
