from typing import List

from investec_python.api.api import API


class Account:
    ...


class AccountsManager:

    _api: API

    def __init__(self, api: API):
        self._api = api

    def list(self) -> List[Account]:
        response = self._api.get("za/pb/v1/accounts")
        accounts = response["data"]["accounts"]
        return accounts
