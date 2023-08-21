from api.base_api import API
import requests


class HeadHunterAPI(API):
    """Класс для запроса вакансий на HeadHunter API"""

    url: str = 'https://api.hh.ru/vacancies'

    def __init__(self, url: str = url):
        """
        Инициализация класса HeadHunterAPI.

        :param url: URL для запросов к HeadHunter API.
        """
        super().__init__(url)

    def _search_vacancies(self, employer_id: int, page=1) -> list:
        """
        Поиск вакансий на HeadHunter API.
        """
        params = {
            'per_page': self._number_of_vacancies,
            'archived': False,
            'employer_id': employer_id,
            'page': page
        }

        response = requests.get(url=self._base_url, params=params)
        response_json = response.json()

        return response_json.get("items", [])

    def get_vacancies(self, employer_id: int) -> list[dict]:
        """
        Получение вакансий по всем доступным страницам
        """
        all_vacancies = []

        for page in range(20):
            page_vacancies = self._search_vacancies(employer_id, page)
            if len(page_vacancies) == 0:
                break
            all_vacancies.extend(page_vacancies)
        return all_vacancies
