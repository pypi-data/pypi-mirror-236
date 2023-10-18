class TestInvestec:
    def test_api_url(self, investec_client):
        assert investec_client.api_url == "https://openapisandbox.investec.com"

    def test_account_list(self, investec_client):
        accounts = investec_client.accounts.list()
        assert len(accounts) > 0
