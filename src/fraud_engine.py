from dataclasses import dataclass
from typing import List


@dataclass
class RiskAssessment:
    risk_level: str
    risk_score: int
    fraud_probability: int
    reasons: List[str]


HIGH_RISK_COUNTRIES = {
    "Unknown",
    "International",
    "High Risk Region"
}

HIGH_RISK_CHANNELS = {
    "Online",
    "Mobile Banking",
    "API"
}

SENSITIVE_TRANSACTION_TYPES = {
    "International Transfer",
    "Cash Withdrawal",
    "Beneficiary Payment"
}


def calculate_risk(transaction):
    score = 5
    reasons = []

    # Amount-based risk
    if transaction.amount > 50000:
        score += 60
        reasons.append(
            "Transaction amount exceeds the critical monitoring threshold."
        )
    elif transaction.amount > 10000:
        score += 40
        reasons.append(
            "Transaction amount exceeds the high-risk monitoring threshold."
        )
    elif transaction.amount > 5000:
        score += 25
        reasons.append(
            "Transaction amount exceeds the medium-risk monitoring threshold."
        )
    else:
        score += 5
        reasons.append(
            "Transaction amount is within the normal monitoring threshold."
        )

    # Channel-based risk
    if transaction.channel in HIGH_RISK_CHANNELS:
        score += 10
        reasons.append(
            f"{transaction.channel} transactions require additional monitoring."
        )

    # Transaction-type risk
    if transaction.transaction_type in SENSITIVE_TRANSACTION_TYPES:
        score += 12
        reasons.append(
            f"{transaction.transaction_type} is treated as a sensitive "
            "transaction type."
        )

    # Country-based risk
    if transaction.country in HIGH_RISK_COUNTRIES:
        score += 18
        reasons.append(
            "The selected transaction location requires enhanced monitoring."
        )

    score = min(score, 100)

    if score >= 80:
        risk_level = "CRITICAL"
    elif score >= 60:
        risk_level = "HIGH"
    elif score >= 35:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Deterministic probability for repeatable testing
    fraud_probability = min(
        99,
        max(1, round(score * 0.92))
    )

    return RiskAssessment(
        risk_level=risk_level,
        risk_score=score,
        fraud_probability=fraud_probability,
        reasons=reasons
    )