def format_time(time_seconds: float) -> str:
    minutes = int(time_seconds / 60)
    seconds = round(time_seconds - minutes * 60, 3)
    return f"{minutes}:{seconds:06.3f}" if minutes > 0 else f"{seconds:06.3f}"