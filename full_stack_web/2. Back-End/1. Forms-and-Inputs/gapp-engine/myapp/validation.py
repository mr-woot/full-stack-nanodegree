months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

def valid_month(month):
    m = month.capitalize()
    if m in months:
        return True
    else:
        return False

def valid_day(day):
  if day.isdigit():
    day = int(day)
    if day>=0 and day<=31:
      return True
  else:
    return None

def valid_year(year):
  if year.isdigit():
    year = int(year)
    if year>=0 and year<=31:
      return True
  else:
    return None