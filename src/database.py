import json
import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent / "fraud_monitoring.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialise_database():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE NOT NULL,
            customer_name TEXT NOT NULL,
            account_number TEXT NOT NULL,
            branch TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            channel TEXT NOT NULL,
            country TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_date TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            fraud_probability INTEGER NOT NULL,
            alert_status TEXT NOT NULL,
            alert_reference TEXT NOT NULL,
            case_priority TEXT NOT NULL,
            assigned_team TEXT NOT NULL,
            reasons TEXT NOT NULL
        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS audit_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT NOT NULL,
            event_time TEXT NOT NULL,
            event_name TEXT NOT NULL,
            event_description TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_transaction(transaction, assessment, alert):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO transactions (
            transaction_id,
            customer_name,
            account_number,
            branch,
            transaction_type,
            channel,
            country,
            amount,
            transaction_date,
            risk_level,
            risk_score,
            fraud_probability,
            alert_status,
            alert_reference,
            case_priority,
            assigned_team,
            reasons
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            transaction.transaction_id,
            transaction.customer_name,
            mask_account_number(transaction.account_number),
            transaction.branch,
            transaction.transaction_type,
            transaction.channel,
            transaction.country,
            transaction.amount,
            transaction.transaction_date,
            assessment.risk_level,
            assessment.risk_score,
            assessment.fraud_probability,
            alert.alert_status,
            alert.alert_reference,
            alert.case_priority,
            alert.assigned_team,
            json.dumps(assessment.reasons)
        )
    )

    connection.commit()
    connection.close()


def save_audit_event(
    transaction_id,
    event_time,
    event_name,
    event_description
):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO audit_events (
            transaction_id,
            event_time,
            event_name,
            event_description
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            transaction_id,
            event_time,
            event_name,
            event_description
        )
    )

    connection.commit()
    connection.close()


def get_recent_transactions(limit=10):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM transactions
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()

    connection.close()
    return [dict(row) for row in rows]


def get_recent_alerts(limit=5):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM transactions
        WHERE alert_status IN ('ACTIVE', 'MONITOR')
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    ).fetchall()

    connection.close()
    return [dict(row) for row in rows]


def get_audit_events(transaction_id, limit=10):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM audit_events
        WHERE transaction_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (transaction_id, limit)
    ).fetchall()

    connection.close()
    return [dict(row) for row in rows]


def get_dashboard_metrics():
    connection = get_connection()

    summary = connection.execute(
        """
        SELECT
            COUNT(*) AS total_transactions,
            SUM(
                CASE
                    WHEN alert_status = 'ACTIVE' THEN 1
                    ELSE 0
                END
            ) AS active_alerts,
            SUM(
                CASE
                    WHEN risk_level = 'CRITICAL' THEN 1
                    ELSE 0
                END
            ) AS critical_transactions,
            COALESCE(AVG(risk_score), 0) AS average_risk_score,
            COALESCE(SUM(amount), 0) AS total_value
        FROM transactions
        """
    ).fetchone()

    distribution_rows = connection.execute(
        """
        SELECT risk_level, COUNT(*) AS total
        FROM transactions
        GROUP BY risk_level
        """
    ).fetchall()

    connection.close()

    distribution = {
        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0,
        "CRITICAL": 0
    }

    for row in distribution_rows:
        distribution[row["risk_level"]] = row["total"]

    return {
        "total_transactions": summary["total_transactions"] or 0,
        "active_alerts": summary["active_alerts"] or 0,
        "critical_transactions": summary["critical_transactions"] or 0,
        "average_risk_score": round(
            summary["average_risk_score"] or 0
        ),
        "total_value": summary["total_value"] or 0,
        "distribution": distribution
    }


def get_all_transactions():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM transactions
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()
    return [dict(row) for row in rows]


def mask_account_number(account_number):
    clean_number = account_number.replace(" ", "")

    if len(clean_number) <= 4:
        return clean_number

    return ("*" * (len(clean_number) - 4)) + clean_number[-4:]