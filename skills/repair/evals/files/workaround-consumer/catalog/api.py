from catalog.paging import page_count


def list_items_response(items, per_page=10):
    return {"count": len(items), "pages": page_count(len(items), per_page)}
