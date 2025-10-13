# /// script
# dependencies = [
# "lxml",
# ]
# ///

def replace_apostrophe(element):
    if element.text:
        element.text = element.text.translate({ord("'"): "’",})
    if element.tail:
        element.tail = element.tail.translate({ord("'"): "’",})
    for child in element:
        replace_apostrophe(child)
