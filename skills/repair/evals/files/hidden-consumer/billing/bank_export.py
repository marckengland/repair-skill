from billing.formatting import format_date


def export_payments(payments):
    """CSV upload for the bank's payment portal."""
    lines = ["date,payee,amount"]
    for p in payments:
        lines.append(f"{format_date(p['date'])},{p['payee']},{p['amount']:.2f}")
    return "\n".join(lines)
