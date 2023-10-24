from dataclasses import dataclass
from pathlib import Path
import json
import logging
import requests

from earthscope_sdk.auth.auth_flow import (
    AuthFlow,
    AuthFlowError,
    NoTokensError,
    UnauthorizedError,
    ValidTokens
)

logger = logging.getLogger(__name__)


class ClientCredentialsFlowError(AuthFlowError):
    pass


@dataclass
class ClientCredentials:
    client_id: str
    client_secret: str


@dataclass
class GetTokensErrorResponse:
    error: str
    error_description: str


class ClientCredentialsFlow(AuthFlow):
    """
    This is an abstract subclass of the AuthFlow abstract class. This class handles the client credential flow actions.

    Attributes
    __________
    audience : str
        Auth0 API Identifier (default is 'https://account.earthscope.org')
    domain : str
        Auth0 tenant domain URL or custom domain (default is 'login.earthscope.org')
    client_credentials: ClientCredentials
        The client credentials - client id and client secret
    _secret: str
        The client secret of the machine-to-machine application from the client_credentials

    Methods
    -------
    request_tokens
        Request the token from Auth0. Validates and saves the token locally.
    """
    def __init__(
        self, domain: str, audience: str, client_credentials: ClientCredentials
    ) -> None:
        if not client_credentials or not client_credentials.client_secret:
            raise ValueError("Client secret missing")

        super().__init__(
            domain=domain,
            audience=audience,
            client_id=client_credentials.client_id,
            scope="",
        )
        # Flow management vars
        self._secret = client_credentials.client_secret

    def get_token_or_request_if_expired(self):
        """
        Loads the access token if it is currently saved locally.
        Requests the token if the token is expired or if no token is found locally
        """
        try:
            self.load_tokens()
            if self.ttl.total_seconds() <= 0:
                self.request_tokens()

        except NoTokensError:
                self.request_tokens()

        return self.access_token

    def request_tokens(self):
        """
        Request the token from Auth0. Validates and saves the token locally.

        Raises
        ------
        Unauthorized Error
            If the request returns as unauthorized
        ClientCredentialsFlowError
            If there is an error in the clientcredentials flow other than unauthorized
        """
        r = requests.post(
            f"https://{self.auth0_domain}/oauth/token",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": self.auth0_client_id,
                "client_secret": self._secret,
                "audience": self.auth0_audience,
            },
        )
        if r.status_code == 200:
            self.validate_and_save_tokens(r.json())
            logger.debug(f"Got tokens: {self.tokens}")
            return self

        if r.status_code == 401:
            err = GetTokensErrorResponse(**r.json())
            if err.error == "access_denied":
                if err.error_description == "Unauthorized":
                    raise UnauthorizedError

        raise ClientCredentialsFlowError


class ClientCredentialsFlowSimple(ClientCredentialsFlow):
    """
    A simple concrete implementation of the ClientCredentialsFlow class. This will store and load tokens on your filesystem

    Attributes:
    -----------
    audience : str, optional
        Auth0 API Identifier (default is 'https://account.earthscope.org')
    client_credentials: ClientCredentials
        the client credentials
    domain : str, optional
        Auth0 tenant domain URL or custom domain (default is 'login.earthscope.org')
    path : str
        The path where your access token will be stored and read

    Methods
    -------
    load_tokens
        Loads and validates your access token from the location specified by the given path.
    save_tokens(creds)
        Saves your access token to the location specified by the given path.
    """
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        path: str,
        domain: str = "login.earthscope.org",
        audience: str = "https://account.earthscope.org",
    ) -> None:
        super().__init__(
            domain=domain,
            audience=audience,
            client_credentials=ClientCredentials(
                client_id=client_id, client_secret=client_secret
            ),
        )
        self.path = Path(path)

    def load_tokens(self):
        """
        Loads and validates the access token from the location specified by the given path.

        Raises
        ------
        NoTokensError
            If no token is found
        Returns
        _______
        valid token : str
        """
        try:
            with self.path.open() as f:
                json_state = json.load(f)
        except FileNotFoundError:
            raise NoTokensError

        self.validate_tokens(json_state)
        return self.tokens

    def save_tokens(self, creds: ValidTokens):
        """
        Writes the token to the location specified by the given path in json format.

        Parameters
        ----------
        creds: ValidTokens
            token credentials
        """
        json_str_state = json.dumps(vars(creds))
        with self.path.open("w") as f:
            f.write(json_str_state)