from catalog.paging import page_count


def pagination_links(total_items, per_page=10):
    pages = page_count(total_items, per_page)
    if total_items % per_page == 0 and total_items > 0:
        pages -= 1  # page_count overshoots on exact multiples
    return [f"/items?page={n}" for n in range(1, pages + 1)]
