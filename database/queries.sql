--Cоздание таблицы данных о работодателях и их вакансиях
CREATE TABLE IF NOT EXISTS all_vacancies (
            id VARCHAR(4) PRIMARY KEY,
            company_name VARCHAR(30) NOT NULL,
            vacancy_name VARCHAR(100) NOT NULL,
            vacancy_salary_from INTEGER NOT NULL,
            vacancy_salary_to INTEGER NOT NULL,
            vacancy_currency VARCHAR(10),
            vacancy_url VARCHAR(100) NOT NULL
);

--Создание таблицы вакансий компании
CREATE TABLE IF NOT EXISTS {company_name} (
    id SERIAL PRIMARY KEY,
    vacancy_name VARCHAR(100) NOT NULL,
    vacancy_salary_from INTEGER NOT NULL,
    vacancy_salary_to INTEGER NOT NULL,
    vacancy_currency VARCHAR(10) NOT NULL,
    vacancy_url VARCHAR(255) NOT NULL,
    vacancy_id VARCHAR(4),
    FOREIGN KEY (vacancy_id) REFERENCES all_vacancies (id) ON DELETE CASCADE
);

--Удаление всех таблиц
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

--Заполнение таблиц всех вакансий
INSERT INTO all_vacancies (id, company_name, vacancy_name, vacancy_salary_from, vacancy_salary_to, vacancy_currency, vacancy_url)
VALUES (%s, %s, %s, %s, %s, %s, %s);

--Заполнение таблиц вакансий компании
INSERT INTO {company_name} (vacancy_id, vacancy_name, vacancy_salary_from, vacancy_salary_to, vacancy_currency, vacancy_url)
VALUES (%s, %s, %s, %s, %s, %s);

--Получает список всех компаний и количество вакансий у каждой компании
SELECT company_name, COUNT(*) AS quantity_of_vacancies
FROM all_vacancies
GROUP BY company_name;

--Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
SELECT * FROM all_vacancies;

--Получает среднюю зарплату по вакансиям
SELECT
    (SELECT ROUND(AVG(vacancy_salary_from)) FROM all_vacancies WHERE vacancy_salary_from <> 0) as avg_salary_from,
    (SELECT ROUND(AVG(vacancy_salary_to)) FROM all_vacancies WHERE vacancy_salary_to <> 0) as avg_salary_to;

--Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
SELECT * FROM all_vacancies
WHERE vacancy_salary_from >
    (SELECT ROUND(AVG(vacancy_salary_from)) FROM all_vacancies WHERE vacancy_salary_from <> 0)
    AND vacancy_salary_to >
    (SELECT ROUND(AVG(vacancy_salary_to)) FROM all_vacancies WHERE vacancy_salary_to <> 0)
ORDER BY vacancy_salary_from DESC, vacancy_salary_to DESC;

--Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python
SELECT * FROM all_vacancies
WHERE LOWER(vacancy_name) ILIKE %s;
