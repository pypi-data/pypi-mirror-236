from investec_python.api.api import API

from investec_python.api.v1.accounts import AccountsManager


class Investec:

    _api: API

    def __init__(
        self,
        use_sandbox: bool = False,
        client_id: str = "",
        secret: str = "",
        api_key: str = "",
    ):
        self._api = API(
            use_sandbox=use_sandbox,
            client_id=client_id,
            secret=secret,
            api_key=api_key,
        )
        self._setup_api_resources()

    def _setup_api_resources(self):
        self.accounts = AccountsManager(self._api)

    @property
    def api_url(self) -> str:
        return self._api.api_url
