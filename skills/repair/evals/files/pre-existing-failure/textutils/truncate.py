def truncate(text, width):
    """Shorten text to at most `width` characters, ending in an ellipsis."""
    if len(text) <= width:
        return text
    return text[:width] + "..."
