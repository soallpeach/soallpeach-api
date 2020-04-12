def convert_ms_to_minutes(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    # days, hours = divmod(hours, 24)
    # seconds = seconds + milliseconds / 1000
    return minutes
