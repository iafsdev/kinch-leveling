def format_time(time_seconds: float) -> str:
    minutes = int(time_seconds / 60)
    seconds = round(time_seconds - minutes * 60, 3)
    return f"{minutes}:{seconds:06.3f}" if minutes > 0 else f"{seconds:06.3f}"

def unformat_time(time_str: str) -> float:
    split_time = time_str.split(":")
    if len(split_time) == 2:
        minutes, seconds = split_time
        return float(minutes) * 60 + float(seconds)
    else:
        return float(split_time[0])