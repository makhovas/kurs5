import psycopg2
from config import DB_CONNECTION_STRING
from utils.read_sql import read_sql
import pandas as pd


class DBManager:
    """Класс для подключения к БД PostgreSQL"""

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    def __init__(self) -> None:
        self.connection = None
        self.sql_queries = read_sql()

    def connects_to_database(self) -> None:
        """Подключение к БД"""
        self.connection = psycopg2.connect(DB_CONNECTION_STRING)

    def disconnect_database(self) -> None:
        """Отключение от БД"""
        if self.connection:
            self.connection.close()

    def __execute_query(self, query, params=None):
        """Метод для выполнения запроса БД"""
        with self.connection:
            with self.connection.cursor() as cur:
                cur.execute(query, params)

    def __show_result(self, query, params=None):
        """Метод для вывода"""
        with self.connection:
            with self.connection.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                print(pd.DataFrame(result, columns=columns).to_string(index=False))

    def create_vacancies_table(self) -> None:
        """Создание таблицы вакансий"""
        query = self.sql_queries['Cоздание таблицы данных о работодателях и их вакансиях']
        self.__execute_query(query)

    def create_company_table(self, company_name) -> None:
        """Создание таблицы компании"""
        query = self.sql_queries['Создание таблицы вакансий компании'].replace('{company_name}', company_name)
        self.__execute_query(query)

    def erase_all_tables(self):
        """Удаление всех таблиц"""
        query = self.sql_queries['Удаление всех таблиц']
        self.__execute_query(query)

    def insert_all_vacancies(self, **kwargs):
        """Заполнение таблиц всех вакансий"""
        query = self.sql_queries['Заполнение таблиц всех вакансий']
        params = list(kwargs.values())
        self.__execute_query(query, params)

    def insert_company_vacancies(self, company_name, **kwargs):
        """Заполнение таблиц вакансий компании"""
        query = self.sql_queries['Заполнение таблиц вакансий компании'].replace('{company_name}', company_name)
        params = list(kwargs.values())
        self.__execute_query(query, params)

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        query = self.sql_queries['Получает список всех компаний и количество вакансий у каждой компании']
        self.__show_result(query)

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        query = self.sql_queries[
            'Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию']
        self.__show_result(query)

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        query = self.sql_queries['Получает среднюю зарплату по вакансиям']
        self.__show_result(query)

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        query = self.sql_queries['Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям']
        self.__show_result(query)

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        query = self.sql_queries[
            'Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python']
        params = ("%"+keyword+"%",)
        self.__show_result(query, params=params)
