def calculate_risk(transaction):
    if transaction.amount > 10000:
        return "HIGH"

    if transaction.amount > 5000:
        return "MEDIUM"

    return "LOW"