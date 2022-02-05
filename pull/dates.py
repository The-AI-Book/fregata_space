import datetime

def generate_days(end_date, num_days, shift: int = 2):
    date_list = list()
    for x in range(0, num_days, shift):
        day = end_date - datetime.timedelta(days=x)
        day = day.strftime("%Y-%m-%d")
        date_list.append(day)
    date_list = date_list[::-1]
    return date_list

def generate_last_dates(num_days = 365 * 2):
    """
    Generates list of the last num_days days.
    """
    base = datetime.datetime.today()
    date_list = generate_days(base, num_days)
    return date_list

def generate_days_between(start_date: str, end_date: str, shift: int = 2):
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    #print("Start date: ", start)
    #print("End date: ", end)
    end += datetime.timedelta(days = 1)
    diff = (end - start).days + 1
    #print("Difference between days: ", diff)
    date_list = generate_days(end, diff, shift = shift)
    return date_list 

if __name__ == '__main__':
    start_date = "2021-04-09"
    end_date = "2021-04-30"
    days = generate_days_between(start_date, end_date)
    print(days)
    days = generate_last_dates(30)
    print(days)