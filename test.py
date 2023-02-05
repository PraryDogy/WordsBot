def testing(name):
    import timeit
    return timeit.repeat(
        f"for x in range(100): {name}()",
        f"from __main__ import {name}",
        number=10
        )


def split_link():
    import clipboard
    max = 50
    url = clipboard.paste()
    
    chunks = [url[i:i+max] for i in range(0, len(url), max)]
    chunks = (f"'{i}'" for i in chunks)
    url = "\n".join(chunks)

    clipboard.copy(url)
