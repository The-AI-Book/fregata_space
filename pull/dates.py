def generate_dates(num_days = 365 * 2):
    import datetime
    base = datetime.datetime.today()
    date_list = list()
    for x in range(num_days):
        day = base - datetime.timedelta(days=x)
        day = day.strftime("%Y-%m-%d")
        date_list.append(day)
    date_list = date_list[::-1]
    return date_list