from shop.catalog import get_item


def cart_lines(order):
    return [(get_item(sku), qty) for sku, qty in order["lines"]]


def total(order):
    return sum(item.get("price", 0) * qty for item, qty in cart_lines(order))
