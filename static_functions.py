import sqlite3
import datetime


def get_stat_data():    # function to get all the data from database
    all_data = []
    with sqlite3.connect('database/database.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        query = """ SELECT * FROM payments JOIN expenses 
                ON expenses.id = payments.expense_id JOIN payer ON payer.id = payments.payer_id"""
        cursor.execute(query)
        all_data = cursor
    return all_data


def get_expenses_items():    # function to get all the data of expenses table from database
    all_data = {'accordance': {}, 'categories': []}
    result = {}
    with sqlite3.connect('database/database.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        query = """SELECT id, category FROM expenses"""
        cursor.execute(query)
        result = dict(cursor)
        all_data['accordance'] = {result[k]: k for k in result}
        all_data['categories'] = [v for v in result.values()]
    return all_data


def get_names():    # function to get all payer's name from database
    all_data = []
    with sqlite3.connect('database/database.db') as db:
        cursor = db.cursor()
        query = """SELECT name FROM payer"""
        cursor.execute(query)
        all_data = list(cursor)
    return all_data


def insert_payments(insert_payments):    # function to insert payment data to database
    success = False
    with sqlite3.connect('database/database.db') as db:
        cursor = db.cursor()
        query = '''INSERT INTO payments(amount, payment_date, expense_id, payer_id, description)
                    Values(?,?,?,?,?);'''
        cursor.execute(query, insert_payments)
        db.commit()
        success = True
    return success

def get_int_name():    # function to get all data of payer table from database
    all_data = {'accordance': {}, 'names': []}
    result = {}
    with sqlite3.connect('database/database.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        query = """SELECT id, name FROM payer"""
        cursor.execute(query)
        result = dict(cursor)
        all_data['accordance'] = {result[k]: k for k in result}
        all_data['names'] = [v for v in result.values()]
    return all_data


def most_spend_category():    # function to calculate most spend category
    data = get_stat_data()
    return max(list(data), key=lambda x: x['amount'])['category']

# functions to transform date to timestamp to save it in database as integer
def get_timestamp(y, m, d):
    return int(datetime.datetime.timestamp(datetime.datetime(y, m, d)))


def get_timestamp_from_input(s):
    t = s.split('-')
    return get_timestamp(int(t[2]), int(t[1]), int(t[0]))


def get_date(tmstmp):
    return datetime.datetime.fromtimestamp(tmstmp).date()


def most_exp_day():    # function to calculate most expensive day
    data = get_stat_data()
    week_days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday',
                 'Friday', 'Saturday', 'Sunday')
    days = {}
    for payment in data:
        if get_date(payment['payment_date']).weekday() in days:
            days[get_date(payment['payment_date']).weekday()] += payment['amount']
        else:
            days[get_date(payment['payment_date']).weekday()] = payment['amount']
    return week_days[max(days, key=days.get)]


def get_most_exp_month():    # function to calculate most expensive month
    data = get_stat_data()
    months = ('0', 'January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December')
    days = {}
    for payment in data:
        if get_date(payment['payment_date']).month in days:
            days[get_date(payment['payment_date']).month] += payment['amount']
        else:
            days[get_date(payment['payment_date']).month] = payment['amount']
    return months[max(days, key=days.get)]


def get_sum_pay1():    # function to calculate amount of all spending of first payer
    with sqlite3.connect('database/database.db') as db:
        cursor = db.cursor()
        query = """SELECT amount FROM payments WHERE payer_id = 1"""
        cursor.execute(query)
        a = cursor.fetchall()
        c = []
        for i in a[0:1]:
            for j in a:
                c.append(j[0])
    return '%.2f' % (sum(c))


def get_sum_pay2():    # function to calculate amount of all spending of second payer
    with sqlite3.connect('database/database.db') as db:
        cursor = db.cursor()
        query = """SELECT amount FROM payments WHERE payer_id = 2"""
        cursor.execute(query)
        a = cursor.fetchall()
        c = []
        for i in a[0:1]:
            for j in a:
                c.append(j[0])
    return '%.2f' % (sum(c))


def most_spender():    # function to find biggest spender of payer
    if get_sum_pay1() > get_sum_pay2():
        return 'Margarita'
    else:
        return 'Dmitrii'


def most_cost_spend():    # function to find biggest amount spent one transaction
    data = get_stat_data()
    return max(list(data), key=lambda x: x['amount'])['amount']


def get_table_data():    # function to get all data from database to bottom table with all transactions
    data = get_stat_data()
    return [(i['id'], i['amount'], '{:%d-%m-%Y}'.format(get_date(i['payment_date'])), i['category'],
            i['name'], i['description']) for i in data]
