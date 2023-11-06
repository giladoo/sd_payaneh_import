
def get_years():
    year_list = []
    for i in range(2016, 2036):
        year_list.append((str(i), str(i)))
    return year_list
def get_years_pr():
    year_list = []
    for i in range(1397, 1420):
        year_list.append((str(i), str(i)))
    return year_list

def get_months():
    return [('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
                              ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'),
                              ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December'), ]
def get_months_pr():

    return [('01', 'فروردین'), ('02', 'اردیبهشت'), ('03', 'خرداد'), ('04', 'تیر'),
                              ('05', 'مرداد'), ('06', 'شهریور'), ('07', 'مهر'), ('08', 'آبان'),
                              ('09', 'آذر'), ('10', 'دی'), ('11', 'بهمن'), ('12', 'اسفند'), ]
