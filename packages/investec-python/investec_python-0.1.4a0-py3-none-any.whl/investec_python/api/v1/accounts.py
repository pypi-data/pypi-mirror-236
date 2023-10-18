from datetime import date
from typing import List

from pydantic import BaseModel, Field

from investec_python.api.api import API, APIMixin


class Balance(BaseModel):
    current_balance: float = Field(alias="currentBalance")


class Transaction(BaseModel):
    account_id: str = Field(alias="accountId")
    type: str
    transaction_type: str = Field(alias="transactionType")
    status: str
    description: str
    card_number: str = Field(alias="cardNumber")
    posted_order: int = Field(alias="postedOrder")
    posting_date: date = Field(alias="postingDate")
    value_date: date = Field(alias="valueDate")
    action_date: date = Field(alias="actionDate")
    transaction_date: date = Field(alias="transactionDate")
    amount: float
    running_balance: float = Field(alias="runningBalance")


class Account(APIMixin, BaseModel):
    account_id: str = Field(alias="accountId")

    def balance(self) -> Balance:
        response = self.api.get(f"za/pb/v1/accounts/{self.account_id}/balance")
        balance = response["data"]
        return Balance(**balance)

    def transactions(self) -> List[Transaction]:
        response = self.api.get(f"za/pb/v1/accounts/{self.account_id}/transactions")
        transactions = response["data"]["transactions"]
        return [Transaction(**transaction) for transaction in transactions]


class AccountsManager:

    _api: API

    def __init__(self, api: API):
        self._api = api

    def list(self) -> List[Account]:
        response = self._api.get("za/pb/v1/accounts")
        accounts = response["data"]["accounts"]
        return [Account(**account) for account in accounts]
