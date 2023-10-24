import json
import logging
import requests

from abc import abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from time import sleep
from typing import Optional

from earthscope_sdk.auth.auth_flow import AuthFlow, NoTokensError, ValidTokens


logger = logging.getLogger(__name__)


class PollingErrorType(str, Enum):
    AUTHORIZATION_PENDING = "authorization_pending"
    SLOW_DOWN = "slow_down"
    EXPIRED_TOKEN = "expired_token"
    ACCESS_DENIED = "access_denied"


class RequestDeviceTokensError(RuntimeError):
    pass


class PollingError(ValueError):
    pass


class PollingExpiredError(PollingError):
    pass


class PollingAccessDeniedError(PollingError):
    pass


@dataclass
class GetDeviceCodeResponse:
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: int


@dataclass
class PollingErrorResponse:
    error: PollingErrorType
    error_description: str


class DeviceCodeFlow(AuthFlow):
    """
    This is an abstract subclass of the AuthFlow abstract class. This class handles the device code flow actions.

    Atttributes
    -----------
    domain : str
        Auth0 tenant domain URL or custom domain
    audience : str
        Auth0 API Identifier
    client_id : str
        Identification value of Auth0 Application
    scope : str
        The specific actions Auth0 applications can be allowed to do or information that they can request on a user’s behalf
    _is_polling: bool, optional
        True if currently polling (default is False)
    _device_codes, optional
        The device code (default is None)

    Methods
    -------
    do_flow
        Requests the device code, prompts the user to complete the device code flow, polls while waiting for completion
         and returns the token
    poll
        Polls for completion of the device code flow
    prompt_user
        abstract method for prompting the user to complette the device code  flow
    request_device_code
        requests the device code from Auth0
    """
    @property
    def polling(self):
        "If is in proccess of polling"
        return self._is_polling

    @property
    def started(self):
        "Returns a boolean on if the device code flow has started"
        return self._device_codes is not None

    def __init__(self, domain: str, audience: str, client_id: str, scope: str) -> None:
        super().__init__(
            domain=domain,
            audience=audience,
            client_id=client_id,
            scope=scope,
        )
        # Flow management vars
        self._is_polling = False
        self._device_codes: Optional[GetDeviceCodeResponse] = None

    def do_flow(self):
        """
        Runs request_device_code, prompt_user, and poll methods. This is the device code flow "login" process.

        Returns
        -------
        token
        """
        self.request_device_code()
        self.prompt_user()
        self.poll()
        return self.tokens

    def poll(self):
        """
        Polling auth0 for token. Sets self._is_polling.
        """
        if not self._device_codes:
            raise PollingError("Cannot poll without initial device code response")

        if self._is_polling:
            raise PollingError("Attempted to double poll")

        self._is_polling = True
        try:
            while True:
                sleep(self._device_codes.interval)

                r = requests.post(
                    f"https://{self.auth0_domain}/oauth/token",
                    headers={"content-type": "application/x-www-form-urlencoded"},
                    data={
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                        "device_code": self._device_codes.device_code,
                        "client_id": self.auth0_client_id,
                    },
                )
                if r.status_code == 200:
                    tokens = self.validate_and_save_tokens(r.json())
                    logger.debug(f"Got tokens: {tokens}")
                    return self

                poll_err = PollingErrorResponse(**r.json())
                if poll_err.error in [
                    PollingErrorType.AUTHORIZATION_PENDING,
                    PollingErrorType.SLOW_DOWN,
                ]:
                    continue

                if poll_err.error == PollingErrorType.EXPIRED_TOKEN:
                    raise PollingExpiredError

                if poll_err.error == PollingErrorType.ACCESS_DENIED:
                    raise PollingAccessDeniedError

                if poll_err:
                    raise PollingError(f"Unknown polling error: {poll_err}")
        finally:
            self._is_polling = False

    @abstractmethod
    def prompt_user(self):
        pass

    def request_device_code(self):
        """
        Request the device code from auth0 and sets self._device_codes

        Raises
        ------
        RequestDeviceTokensError
            failed to get a device code
        """
        r = requests.post(
            f"https://{self.auth0_domain}/oauth/device/code",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data={
                "client_id": self.auth0_client_id,
                "scope": self.token_scope,
                "audience": self.auth0_audience,
            },
        )
        if r.status_code == 200:
            self._device_codes = GetDeviceCodeResponse(**r.json())
            logger.debug(f"Got device code response: {self._device_codes}")
            return self

        raise RequestDeviceTokensError(f"Failed to get a device code: {r.text}")


class DeviceCodeFlowSimple(DeviceCodeFlow):
    """
    This is a concrete implementation of the DeviceCodeFlow abstract class. This will store tokens on your filesystem
    and print the user prompt to the standard out.

    Default Auth0 values are for the Production tenant for UNAVCO Data File Server Access Application and User Management API.

    Attributes:
    -----------
    path : str
        The path where your access token will be stored and read. If this is a directory, the file name will be assigned as sso_tokens.json. You maye provide your own file name if desired.
    domain : str, optional
        Auth0 tenant domain URL or custom domain (default is 'login.earthscope.org')
    audience : str, optional
        Auth0 API Identifier (default is 'https://account.earthscope.org')
    client_id : str, optional
        Identification value of Auth0 Application (default is 'b9DtAFBd6QvMg761vI3YhYquNZbJX5G0')
    scope : str, optional
        The specific actions Auth0 applications can be allowed to do or information that they can request on a user’s behalf. (default is "openid profile email offline_access")

    Methods
    -------
    load_tokens
        Loads and validates your access token from the location specified by the given path.
    save_tokens(creds)
        Saves your access token to the location specified by the given path.
    prompt_user
        Prints the link for the sso authorization flow.
    """
    def __init__(
        self,
            path: str,
            domain: str = "login.earthscope.org",
            audience: str = "https://account.earthscope.org",
            client_id: str = "b9DtAFBd6QvMg761vI3YhYquNZbJX5G0",
            scope: str = "openid profile email offline_access"

    ) -> None:
        super().__init__(
            domain=domain,
            audience=audience,
            client_id=client_id,
            scope=scope,
        )
        self.path = Path(path)
        if self.path.is_dir():
            self.path = self.path / "sso_tokens.json"

    def load_tokens(self):
        """
        Loads and validates your access token from the location specified by the given path.

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
        writes your access token to the location specified by the given path in json format.

        Parameters
        ----------
        creds: ValidTokens
            token credentials
        """
        json_str_state = json.dumps(vars(creds))
        with self.path.open("w") as f:
            f.write(json_str_state)

    def prompt_user(self):
        """
        Prints the url to complete the sso authorization flow to to stdout
        """
        if not self._device_codes:
            raise RuntimeError(
                "You must start the device flow before prompting the user"
            )

        print(
            f"""To complete the SSO authorization, please visit the following URL in a browser of your choice:
            {self._device_codes.verification_uri_complete}
            """
        )