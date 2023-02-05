def testing(name):
    import timeit
    return timeit.repeat(
        f"for x in range(100): {name}()",
        f"from __main__ import {name}",
        number=10
        )

