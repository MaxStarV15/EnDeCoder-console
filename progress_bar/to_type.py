

def get_volume(volume: int) -> str:
    if volume < 1024:
        return f"{volume} Б ({volume:_})"
    elif volume < 1024**2:
        return f"{volume / 1024:.2f} КБ ({volume:_})"
    elif volume < 1024**3:
        return f"{volume / 1024**2:.2f} МБ ({volume:_})"
    else:
        return f"{volume / 1024**3:.2f} ГБ ({volume:_})"
