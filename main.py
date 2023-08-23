from config import COMPANIES_ID
from database.db_manager import DBManager
from api.hh import HeadHunterAPI
from utils.currency_converter import get_currency_data
from utils.unique_key_generation import generate_unique_four_letter_value

if __name__ == '__main__':
    dbm = DBManager()
    dbm.connects_to_database()
    user_input = int(input('Обновить базу данных по вакансиям: 1\n'
                           'Не обновлять: нажмите любую другую цифру\n'))
    if user_input == 1:
        dbm.erase_all_tables()
        dbm.create_vacancies_table()
        hh = HeadHunterAPI()
        existing_values = []
        for employer_name, employer_id in COMPANIES_ID.items():
            company_vacancies = hh.get_vacancies(employer_id)
            dbm.create_company_table(employer_name)
            for vacancy in company_vacancies:
                vacancy_name = vacancy["name"]
                vacancy_url = vacancy["alternate_url"]
                vacancy_from = int(vacancy["salary"]["from"]) if vacancy.get("salary") is not None and vacancy[
                    "salary"].get("from") is not None else 0
                vacancy_to = int(vacancy["salary"]["to"]) if vacancy.get("salary") is not None and vacancy[
                    "salary"].get("to") is not None else 0
                if vacancy.get("salary") and vacancy["salary"]["currency"] not in ["RUR", "RUB"]:
                    vacancy_from = get_currency_data(vacancy["salary"]["currency"])
                    vacancy_to = get_currency_data(vacancy["salary"]["currency"])
                vacancy_currency = "RUR"
                vacancy_id = generate_unique_four_letter_value(existing_values)
                dbm.insert_all_vacancies(id=vacancy_id, company_name=employer_name, vacancy_name=vacancy_name,
                                         vacancy_salary_from=vacancy_from, vacancy_salary_to=vacancy_to,
                                         vacancy_currency=vacancy_currency,
                                         vacancy_url=vacancy_url)
                dbm.insert_company_vacancies(employer_name, vacancy_id=vacancy_id, vacancy_name=vacancy_name,
                                             vacancy_salary_from=vacancy_from, vacancy_salary_to=vacancy_to,
                                             vacancy_currency=vacancy_currency, vacancy_url=vacancy_url)
    while True:
        user_input = int(input('Вывод всех вакансий: 1\n'
                               'Вывести среднюю зарплату: 2\n'
                               'Вывести вакансии с высокой зарплатой: 3\n'
                               'Вывести вакансии по ключевому слову: 4\n'
                               'Вывести количество вакансий у компании: 5\n'
                               'Выход: 0\n'))
        if user_input == 1:
            dbm.get_all_vacancies()
        elif user_input == 2:
            dbm.get_avg_salary()
        elif user_input == 3:
            dbm.get_vacancies_with_higher_salary()
        elif user_input == 4:
            dbm.get_vacancies_with_keyword(keyword=input('Введите ключевое слово: '))
        elif user_input == 5:
            dbm.get_companies_and_vacancies_count()
        elif user_input == 0:
            exit()
        else:
            print("Введено некорректное значение")

    dbm.disconnect_database()
