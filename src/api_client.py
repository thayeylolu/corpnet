# src/api_client.py

import requests
from src.config import OPENCORPORATES_API_KEY, OPENCORPORATES_BASE_URL

class OpenCorporatesClient:
    def __init__(self):
        self.api_key = OPENCORPORATES_API_KEY
        self.base_url = OPENCORPORATES_BASE_URL

    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        params['api_token'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def search_companies(self, query, jurisdiction_code=None, per_page=10):
        params = {'q': query, 'per_page': per_page}
        if jurisdiction_code:
            params['jurisdiction_code'] = jurisdiction_code
        return self._get("companies/search", params)

    def get_company(self, jurisdiction_code, company_number):
        return self._get(f"companies/{jurisdiction_code}/{company_number}")

    def get_officers(self, jurisdiction_code, company_number):
        return self._get(f"companies/{jurisdiction_code}/{company_number}/officers")

