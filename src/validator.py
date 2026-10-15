def validate_transaction_data(form_data):
    errors = []

    customer_name = form_data.get("customer_name", "").strip()
    account_number = form_data.get("account_number", "").strip()
    branch = form_data.get("branch", "").strip()
    transaction_type = form_data.get("transaction_type", "").strip()
    channel = form_data.get("channel", "").strip()
    country = form_data.get("country", "").strip()
    amount_value = form_data.get("amount", "").strip()

    if len(customer_name) < 2:
        errors.append("Customer name must contain at least two characters.")

    clean_account_number = account_number.replace(" ", "")

    if not clean_account_number.isdigit():
        errors.append("Account number may only contain numbers.")

    if len(clean_account_number) < 6:
        errors.append("Account number must contain at least six digits.")

    if not branch:
        errors.append("Branch is required.")

    if not transaction_type:
        errors.append("Transaction type is required.")

    if not channel:
        errors.append("Transaction channel is required.")

    if not country:
        errors.append("Transaction country is required.")

    try:
        amount = float(amount_value)

        if amount <= 0:
            errors.append("Transaction amount must be greater than zero.")

        if amount > 100000000:
            errors.append(
                "Transaction amount exceeds the supported assessment limit."
            )

    except ValueError:
        amount = 0
        errors.append("Transaction amount must be a valid number.")

    return errors, amount