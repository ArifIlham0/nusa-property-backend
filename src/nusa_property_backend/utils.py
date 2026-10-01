import math
from typing import Dict, Any


def format_rupiah(amount: int) -> str:
    formatted = f"{amount:,}".replace(",", ".")
    return f"Rp {formatted}"


def calculate_kpr(
    price: int,
    dp_percent: int,
    tenor_years: int,
    is_syariah: bool = False
) -> Dict[str, Any]:
    dp_amount = round(price * (dp_percent / 100.0))
    loan_amount = max(0, price - dp_amount)
    rate = 0.0515 if is_syariah else 0.0488
    total_months = tenor_years * 12
    monthly_rate = rate / 12.0

    if loan_amount > 0 and monthly_rate > 0:
        factor = math.pow(1.0 + monthly_rate, float(total_months))
        monthly_installment = round((loan_amount * monthly_rate * factor) / (factor - 1.0))
    else:
        monthly_installment = 0

    total_payment = monthly_installment * total_months
    total_interest = max(0, total_payment - loan_amount)

    if total_payment > 0:
        principal_pct = float((loan_amount / total_payment) * 100.0)
    else:
        principal_pct = 60.0

    interest_pct = max(0.0, 100.0 - principal_pct)

    raw_min_income = round((monthly_installment / 0.38) / 500_000) * 500_000
    recommended_min_income = max(5_000_000, raw_min_income)

    return {
        "propertyPrice": price,
        "dpPercent": dp_percent,
        "dpAmount": dp_amount,
        "loanAmount": loan_amount,
        "tenorYears": tenor_years,
        "isSyariah": is_syariah,
        "interestRate": rate,
        "monthlyInstallment": monthly_installment,
        "totalPayment": total_payment,
        "totalInterest": total_interest,
        "principalPercentage": round(principal_pct, 1),
        "interestPercentage": round(interest_pct, 1),
        "recommendedMinIncome": recommended_min_income,
    }
