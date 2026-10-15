from dataclasses import dataclass
from datetime import datetime


@dataclass
class FraudAlert:
    alert_status: str
    alert_reference: str
    case_priority: str
    assigned_team: str
    generated_at: str
    message: str


def create_alert(transaction, assessment):
    generated_at = datetime.now().strftime("%d %b %Y %H:%M:%S")

    if assessment.risk_level == "CRITICAL":
        return FraudAlert(
            alert_status="ACTIVE",
            alert_reference=f"ALT-{transaction.transaction_id}",
            case_priority="P1 - Critical",
            assigned_team="Fraud Investigations",
            generated_at=generated_at,
            message=(
                "Critical fraud alert generated. Immediate investigation "
                "is required."
            )
        )

    if assessment.risk_level == "HIGH":
        return FraudAlert(
            alert_status="ACTIVE",
            alert_reference=f"ALT-{transaction.transaction_id}",
            case_priority="P2 - High",
            assigned_team="Fraud Operations",
            generated_at=generated_at,
            message=(
                "High-risk fraud alert generated for operational review."
            )
        )

    if assessment.risk_level == "MEDIUM":
        return FraudAlert(
            alert_status="MONITOR",
            alert_reference=f"MON-{transaction.transaction_id}",
            case_priority="P3 - Medium",
            assigned_team="Transaction Monitoring",
            generated_at=generated_at,
            message=(
                "Transaction added to the monitoring queue."
            )
        )

    return FraudAlert(
        alert_status="CLEARED",
        alert_reference=f"CLR-{transaction.transaction_id}",
        case_priority="P4 - Low",
        assigned_team="Automated Monitoring",
        generated_at=generated_at,
        message="No fraud alert generated."
    )