"""Item lookups. Legacy items come from the v1 catalog service; items added
since September come from the v2 service."""

V1_ITEMS = {
    "mug": {"sku": "mug", "name": "Mug", "price": 12.00},
    "tee": {"sku": "tee", "name": "T-shirt", "price": 20.00},
}

V2_ITEMS = {
    "cap": {"sku": "cap", "title": "Cap", "unit_price": 15.00},
}


def get_item(sku):
    if sku in V1_ITEMS:
        return dict(V1_ITEMS[sku])
    if sku in V2_ITEMS:
        return dict(V2_ITEMS[sku])
    raise KeyError(sku)
