from fraud_engine import calculate_risk
from transaction import Transaction


def create_transaction(
    amount,
    transaction_type="Card Payment",
    channel="Branch",
    country="South Africa"
):
    return Transaction.create(
        transaction_id="TX-TEST001",
        customer_name="Test Customer",
        account_number="123456789",
        branch="Johannesburg",
        transaction_type=transaction_type,
        channel=channel,
        country=country,
        amount=amount
    )


def test_low_value_transaction():
    transaction = create_transaction(1000)

    assessment = calculate_risk(transaction)

    assert assessment.risk_level == "LOW"
    assert assessment.risk_score < 35


def test_medium_value_transaction():
    transaction = create_transaction(6000)

    assessment = calculate_risk(transaction)

    assert assessment.risk_level == "MEDIUM"
    assert 35 <= assessment.risk_score < 60


def test_high_value_transaction():
    transaction = create_transaction(
        amount=15000,
        transaction_type="Beneficiary Payment",
        channel="Online"
    )

    assessment = calculate_risk(transaction)

    assert assessment.risk_level == "HIGH"
    assert 60 <= assessment.risk_score < 80


def test_critical_transaction():
    transaction = create_transaction(
        amount=75000,
        transaction_type="International Transfer",
        channel="API",
        country="International"
    )

    assessment = calculate_risk(transaction)

    assert assessment.risk_level == "CRITICAL"
    assert assessment.risk_score >= 80


def test_fraud_probability_stays_within_range():
    transaction = create_transaction(
        amount=75000,
        transaction_type="International Transfer",
        channel="API",
        country="International"
    )

    assessment = calculate_risk(transaction)

    assert 1 <= assessment.fraud_probability <= 99


def test_risk_assessment_contains_reasons():
    transaction = create_transaction(15000)

    assessment = calculate_risk(transaction)

    assert len(assessment.reasons) > 0