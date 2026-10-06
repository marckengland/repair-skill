from billing.formatting import format_date


def render_invoice(number, issued, amount):
    return (
        f"Invoice #{number}\n"
        f"Date: {format_date(issued)}\n"
        f"Amount due: ${amount:.2f}\n"
    )
