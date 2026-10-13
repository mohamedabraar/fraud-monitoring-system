from transaction import Transaction
from validator import validate_transaction
from fraud_engine import calculate_risk
from alert_manager import create_alert

transaction = Transaction("TX1001", 15000)

if validate_transaction(transaction):

    risk = calculate_risk(transaction)

    alert = create_alert(risk)

    print("Transaction:", transaction.transaction_id)
    print("Risk:", risk)
    print("Alert:", alert)

else:
    print("Invalid Transaction")