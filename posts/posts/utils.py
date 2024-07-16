def validate_time(time):
    time_dict = {}
    time_dict['reply_seconds'] = time
    time_dict['reply_hours'] = time_dict['reply_seconds'] // 3600
    time_dict['reply_seconds'] = time_dict['reply_seconds'] % 3600
    time_dict['reply_minutes'] = time_dict['reply_seconds'] // 60
    time_dict['reply_seconds'] = time_dict['reply_seconds'] % 60
    return time_dict