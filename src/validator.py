def validate_transaction(transaction):
    if transaction.amount <= 0:
        return False
    return True