from typing import List
from dcentrapi.Base import Base
from dcentrapi.requests_dappi import requests_get


class TokenPrices(Base):

    def get_token_price(self, match_string: str):
        url = self.web3index_url + "tokenPrices"
        data = {"match_strings": [match_string]}
        response = requests_get(url, params=data, headers=self.headers)
        return response.json()

    def get_token_prices(self, match_strings: List[str]):
        url = self.web3index_url + "tokenPrices"
        data = {"match_strings": match_strings}
        response = requests_get(url, params=data, headers=self.headers)
        return response.json()
