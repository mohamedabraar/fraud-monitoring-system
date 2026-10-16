from validator import validate_transaction_data


def valid_form_data():
    return {
        "customer_name": "Test Customer",
        "account_number": "123456789",
        "branch": "Johannesburg",
        "transaction_type": "Card Payment",
        "channel": "Branch",
        "country": "South Africa",
        "amount": "1000"
    }


def test_valid_transaction_data():
    form_data = valid_form_data()

    errors, amount = validate_transaction_data(form_data)

    assert errors == []
    assert amount == 1000.0


def test_missing_customer_name():
    form_data = valid_form_data()
    form_data["customer_name"] = ""

    errors, _ = validate_transaction_data(form_data)

    assert len(errors) > 0
    assert any(
        "customer name" in error.lower()
        for error in errors
    )


def test_invalid_account_number():
    form_data = valid_form_data()
    form_data["account_number"] = "ABC123"

    errors, _ = validate_transaction_data(form_data)

    assert len(errors) > 0
    assert any(
        "account number" in error.lower()
        for error in errors
    )


def test_short_account_number():
    form_data = valid_form_data()
    form_data["account_number"] = "123"

    errors, _ = validate_transaction_data(form_data)

    assert len(errors) > 0


def test_zero_transaction_amount():
    form_data = valid_form_data()
    form_data["amount"] = "0"

    errors, amount = validate_transaction_data(form_data)

    assert amount == 0
    assert len(errors) > 0


def test_negative_transaction_amount():
    form_data = valid_form_data()
    form_data["amount"] = "-500"

    errors, amount = validate_transaction_data(form_data)

    assert amount == -500
    assert len(errors) > 0


def test_non_numeric_amount():
    form_data = valid_form_data()
    form_data["amount"] = "not-a-number"

    errors, amount = validate_transaction_data(form_data)

    assert amount == 0
    assert len(errors) > 0


def test_missing_branch():
    form_data = valid_form_data()
    form_data["branch"] = ""

    errors, _ = validate_transaction_data(form_data)

    assert any(
        "branch" in error.lower()
        for error in errors
    )


def test_missing_transaction_type():
    form_data = valid_form_data()
    form_data["transaction_type"] = ""

    errors, _ = validate_transaction_data(form_data)

    assert any(
        "transaction type" in error.lower()
        for error in errors
    )


def test_missing_country():
    form_data = valid_form_data()
    form_data["country"] = ""

    errors, _ = validate_transaction_data(form_data)

    assert any(
        "country" in error.lower()
        for error in errors
    )


def test_amount_over_supported_limit():
    form_data = valid_form_data()
    form_data["amount"] = "100000001"

    errors, amount = validate_transaction_data(form_data)

    assert amount == 100000001
    assert any(
        "supported assessment limit" in error.lower()
        for error in errors
    )