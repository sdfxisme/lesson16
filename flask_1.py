from flask import Flask, render_template, request
import sqlite3 as lite
import sys
import requests
app = Flask(__name__)


@app.route('/')
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/city_form', methods=['POST'])
def city_form():
    city = request.form['city']
    prof = request.form['prof']
    string = prof + 'AND' + city
    URL = 'https://api.hh.ru/vacancies'
    params = {'text': string,
              'only_with_salary': True,
              'page': 1,
              'per_page': 20}
    result = requests.get(URL, params=params).json()
    found_vacancies = result['found']
    pages = result['pages']
    salary_from = []
    salary_to = []

    print('найдено вакансий {} штук на {} страницах'.format(result['found'], result['pages']))

    for i in range(1, pages):
        URL = 'https://api.hh.ru/vacancies'
        params = {'text': string,
                  'only_with_salary': True,
                  'page': i,
                  'per_page': 20}
        result = requests.get(URL, params=params).json()
        items = result['items']

        for i in items:
            salary = i['salary']
            sal_from = salary['from']
            sal_to = salary['to']
            if sal_from != None: salary_from.append(sal_from)
            if sal_to != None: salary_to.append(sal_to)

    mid_sal_from = int(sum(salary_from) / len(salary_from))
    mid_sal_to = int(sum(salary_to) / len(salary_to))


    data = {'city': city,
            'prof': prof,
            'salary_from': mid_sal_from,
            'salary_to': mid_sal_to}

    connect = None
    connect = lite.connect('test.db')
    with connect:
        cur = connect.cursor()
        #cur.execute("CREATE TABLE hh(city TEXT, prof TEXT, sallary_from INT, sallary_to INT)")
        cur.execute("INSERT INTO hh VALUES(?,?,?,?)", (data['city'], data['prof'], data['salary_from'], data['salary_to']))
        #connect.close()
    return render_template('city_form.html', data=data)

@app.route('/hands_to_db')
def hands_to_db():
    return render_template('hands_to_db.html')

@app.route('/hands_to_db_rec', methods=['POST'])
def hands_to_db_rec():
    city = request.form['city']
    prof = request.form['prof']
    salary_from = request.form['salary_from']
    salary_to = request.form['salary_to']
    data = {'city': city,
            'prof': prof,
            'salary_from': salary_from,
            'salary_to': salary_to}

    connect = None
    connect = lite.connect('test.db')
    with connect:
        cur = connect.cursor()
        #cur.execute("CREATE TABLE hhotelka(city TEXT, prof TEXT, sallary_from INT, sallary_to INT)")
        cur.execute("INSERT INTO hhotelka VALUES(?,?,?,?)", (city, prof, salary_from, salary_to))
        # connect.close()
    return render_template('hands_to_db_rec.html', data = data)


if __name__ == "__main__":
    app.run(debug=True)
