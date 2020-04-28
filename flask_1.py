from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String, Float, create_engine, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

    salary_from = int(sum(salary_from) / len(salary_from))
    salary_to = int(sum(salary_to) / len(salary_to))


    data = {'city': city,
            'prof': prof,
            'salary_from': salary_from,
            'salary_to': salary_to}

    engine = create_engine('sqlite:///orm1.sqlite', echo=False)
    Base = declarative_base()

    class HH_request(Base):
        __tablename__ = 'HH_request_new'
        id = Column(Integer, primary_key=True)
        city = Column(String)
        prof = Column(String)
        salary_from = Column(Integer)
        salary_to = Column(Integer)

        def __init__(self, city, prof, salary_from, salary_to):
            self.city = city
            self.prof = prof
            self.salary_from = salary_from
            self.salary_to = salary_to

        def __str__(self):
            return f'{self.city},{self.prof},{self.salary_from},{self.salary_to}'

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    HH_request_1 = HH_request(city, prof, salary_from, salary_to)
    session.add(HH_request_1)
    session.commit()

    return render_template('city_form.html', data=data)

@app.route('/hands_to_db')
def hands_to_db():
    return render_template('hands_to_db.html')

@app.route('/hands_to_db_rec', methods=['POST'])
def hands_to_db_rec():
    city_hotelka = request.form['City']
    prof_hotelka = request.form['Prof']
    salary_from_hotelka = request.form['Salary_from']
    salary_to_hotelka = request.form['Salary_to']

    data = {'city': city_hotelka,
            'prof': prof_hotelka,
            'salary_from': salary_from_hotelka,
            'salary_to': salary_to_hotelka}

    engine = create_engine('sqlite:///orm1.sqlite', echo=False)
    Base = declarative_base()

    class HH_hotelka(Base):
        __tablename__ = 'HH_hotelka'
        id = Column(Integer, primary_key=True)
        city_hotelka = Column(String)
        prof_hotelka = Column(String)
        salary_from_hotelka = Column(Integer)
        salary_to_hotelka = Column(Integer)

        def __init__(self, city_hotelka, prof_hotelka, salary_from_hotelka, salary_to_hotelka):
            self.city_hotelka = city_hotelka
            self.prof_hotelka = prof_hotelka
            self.salary_from_hotelka = salary_from_hotelka
            self.salary_to_hotelka = salary_to_hotelka

        def __str__(self):
            return f'{self.city_hotelka},{self.prof_hotelka},{self.salary_from_hotelka},{self.salary_to_hotelka}'


    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    HH_hotelka_1 = HH_hotelka(city_hotelka, prof_hotelka, salary_from_hotelka, salary_to_hotelka)
    session.add(HH_hotelka_1)
    session.commit()

    return render_template('hands_to_db_rec.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
