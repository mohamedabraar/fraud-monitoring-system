from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    transaction_id: str
    customer_name: str
    account_number: str
    branch: str
    transaction_type: str
    channel: str
    country: str
    amount: float
    transaction_date: str

    @classmethod
    def create(
        cls,
        transaction_id,
        customer_name,
        account_number,
        branch,
        transaction_type,
        channel,
        country,
        amount
    ):
        return cls(
            transaction_id=transaction_id,
            customer_name=customer_name.strip(),
            account_number=account_number.strip(),
            branch=branch.strip(),
            transaction_type=transaction_type.strip(),
            channel=channel.strip(),
            country=country.strip(),
            amount=float(amount),
            transaction_date=datetime.now().strftime("%d %b %Y %H:%M:%S")
        )
    