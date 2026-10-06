from shop.cart import cart_lines, total


def render_receipt(order):
    rows = [
        f"{item.get('name', '?')} x{qty}  ${item.get('price', 0) * qty:.2f}"
        for item, qty in cart_lines(order)
    ]
    rows.append(f"TOTAL  ${total(order):.2f}")
    return "\n".join(rows)
