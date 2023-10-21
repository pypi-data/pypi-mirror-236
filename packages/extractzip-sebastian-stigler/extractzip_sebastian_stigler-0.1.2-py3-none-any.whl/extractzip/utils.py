def red(text: str):
    return f"\x1b[31m{text}\x1b[0m"


def green(text: str):
    return f"\x1b[32m{text}\x1b[0m"


def blue(text: str):
    return f"\x1b[34m{text}\x1b[0m"


def bold(text: str):
    return f"\x1b[1m{text}\x1b[0m"
