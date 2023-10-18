class TestInvestec:
    def test_api_url(self, investec_client):
        assert investec_client.api_url == "https://openapisandbox.investec.com"

    def test_account_list(self, investec_client):
        accounts = investec_client.accounts.list()

        assert len(accounts) > 0
        for account in accounts:
            assert account.account_id is not None

    def test_account_balance(self, investec_client):
        account = investec_client.accounts.list()[0]
        balance = account.balance()

        assert balance.current_balance is not None

    def test_account_transactions(self, investec_client):
        account = investec_client.accounts.list()[0]
        transactions = account.transactions()

        assert len(transactions) > 0
        assert transactions[0].amount is not None
