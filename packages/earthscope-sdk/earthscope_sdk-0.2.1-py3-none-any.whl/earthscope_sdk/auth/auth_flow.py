import datetime as dt
import json
import logging

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, Union
import jwt

import requests

logger = logging.getLogger(__name__)


class AuthFlowError(Exception):
    """Generic authentication flow error"""


class UnauthorizedError(AuthFlowError):
    pass


class NoTokensError(AuthFlowError):
    pass


class NoIdTokenError(NoTokensError):
    pass


class NoRefreshTokenError(NoTokensError):
    pass


class InvalidRefreshTokenError(AuthFlowError):
    pass


@dataclass
class TokensResponse:
    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    token_type: str
    expires_in: int
    scope: Optional[str]


@dataclass
class UnvalidatedTokens:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    scope: str

    @classmethod
    def from_dict(cls, o: Dict):
        return cls(
            access_token=o.get("access_token"),
            id_token=o.get("id_token"),
            refresh_token=o.get("refresh_token"),
            scope=o.get("scope"),
        )


@dataclass
class ValidTokens(UnvalidatedTokens):
    expires_at: int
    issued_at: int

    @classmethod
    def from_unvalidated(cls, creds: UnvalidatedTokens, body: Dict):
        return cls(
            access_token=creds.access_token,
            id_token=creds.id_token,
            refresh_token=creds.refresh_token,
            scope=creds.scope,
            expires_at=body.get("exp"),
            issued_at=body.get("iat"),
        )


class AuthFlow(ABC):
    """
    This is an abstract class that handles retrieving, validating, saving, and refreshing access tokens.

    Attributes
    __________
    domain : str
        Auth0 tenant domain URL or custom domain (default is 'login.earthscope.org')
    audience : str
        Auth0 API Identifier (default is 'https://account.earthscope.org')
    client_id : str
        Identification value of Auth0 Application (default is 'b9DtAFBd6QvMg761vI3YhYquNZbJX5G0')
    scope : str
        The specific actions Auth0 applications can be allowed to do or information that they can request on a user’s behalf.
    _tokens : str, optional
        Access or ID Token
    _access_token_body : dict, optional
        Body of the decrypted access token
    _id_token_body : dict, optional
        Body of the decrypted id token

    Methods
    _______
    load_tokens
        Load the token (abstract method)
    save_tokens(creds)
        Save the token (abstract method)
    refresh(scope=None, revoke=False)
        Refresh the access token or revoke the refresh token
    validate_and_save_tokens(unvalidated_creds)
        Validate and save the token
    validate_tokens(unvalidated_creds)
        Validate the token
    get_access_token_refresh_if_necessary(no_auto_refresh=False, auto_refresh_threshold=3600)
        Retrieve the access token. Automatically refreshes the token when necessary.

    """
    @property
    def access_token(self):
        """
        Get access token

        Returns
        -------
        access token: str
        """
        return self.tokens.access_token

    @property
    def access_token_body(self):
        """
        Body of the access token

        Raises
        ______
        NoTokensError
            If there is no token

        Returns
        -------
        access_token_body: dict
        """
        if self._access_token_body is None:
            raise NoTokensError
        return self._access_token_body

    @property
    def tokens(self):
        """
        Get tokens

        raises
        ------
        NoTokensError
            If no token to retrieve

        Returns
        -------
        tokens
        """
        if not self._tokens:
            raise NoTokensError

        return self._tokens

    @property
    def expires_at(self):
        """
        When the token expires

        Returns
        -------
        datetime
        """
        return dt.datetime.fromtimestamp(self.tokens.expires_at, dt.timezone.utc)

    @property
    def id_token(self):
        """
        Get the ID token

        Raises
        ------
        NoIDTokenError
            If there is no id token to be retrieved

        Returns
        -------
        id token: srt
        """
        idt = self.tokens.id_token
        if not idt:
            raise NoIdTokenError

        return idt

    @property
    def id_token_body(self):
        """
        Body of the id token

        Raises
        ______
        NoIdTokenError
            If there is no id token

        Returns
        -------
        id_token_body: dict
        """
        if self._id_token_body is None:
            raise NoIdTokenError
        return self._id_token_body

    @property
    def issued_at(self):
        """
        When the token was issued

        Returns
        -------
        datetime
        """
        return dt.datetime.fromtimestamp(self.tokens.issued_at, dt.timezone.utc)

    @property
    def refresh_token(self):
        """
        Get the refresh token

        Raises
        ------
        NoRefreshTokenError
            If there is no refresh token to be retrieved

        Returns
        -------
        refresh token: srt
        """
        rt = self.tokens.refresh_token
        if not rt:
            raise NoRefreshTokenError

        return rt

    @property
    def has_refresh_token(self):
        """
        If the acces token contains a refresh token

        Returns
        -------
        boolean
        """
        try:
            return self.tokens.refresh_token is not None
        except NoTokensError:
            return False

    @property
    def ttl(self):
        """
        Time to live of the token

        Returns
        -------
        datetime
        """
        return self.expires_at - dt.datetime.now(dt.timezone.utc)

    def __init__(self, domain: str, audience: str, client_id: str, scope: str) -> None:
        self.auth0_domain = domain
        self.auth0_audience = audience
        self.auth0_client_id = client_id
        self.token_scope = scope

        self._tokens: Optional[ValidTokens] = None
        self._access_token_body: Optional[Dict[str, Union[str, int]]] = None
        self._id_token_body: Optional[Dict[str, Union[str, int]]] = None

    @abstractmethod
    def load_tokens(self):
        """
        Load the token (abstract method)
        """
        pass

    @abstractmethod
    def save_tokens(self, creds: ValidTokens):
        """
        Save the token (abstract method)

        Parameters
        ----------
        creds : ValidTokens
        """
        pass

    def refresh(self, scope: Optional[str] = None, revoke: bool = False):
        """
        Refresh the access token

        Parameters
        __________
        scope : str, optional
            The specific actions Auth0 applications can be allowed to do or information that they can request on a user’s behalf.
        revoke: bool, optional
            Whether to revoke the refresh token (default is False)

        Raises
        ______
        InvalidRefreshTokenError
            If the token refresh fails
        """
        scope = scope or self.token_scope

        if not self.has_refresh_token:
            raise NoRefreshTokenError("No refresh token was found. Please re-authenticate.")

        if revoke:
            r = requests.post(
                f"https://{self.auth0_domain}/oauth/revoke",
                headers={"content-type": "application/json"},
                data=json.dumps({
                    "client_id": self.auth0_client_id,
                    "token": self.refresh_token,
                }),
            )
            if r.status_code == 200:
                logger.debug(f"Refresh token revoked: {self.refresh_token}")
                return
            else:
                raise RuntimeError(r.json()["detail"])
                

        else:
            r = requests.post(
                f"https://{self.auth0_domain}/oauth/token",
                headers={"content-type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "refresh_token",
                    "client_id": self.auth0_client_id,
                    "refresh_token": self.refresh_token,
                    "scopes": scope,
                },
            )

            # add previous refresh token to new access token
            if r.status_code == 200:
                refresh_token = self.refresh_token
                self.validate_and_save_tokens(r.json())
                if not self.has_refresh_token:
                    self._tokens.refresh_token = refresh_token
                    self.save_tokens(self._tokens)
                logger.debug(f"Refreshed tokens: {self._tokens}")
                return self

        raise InvalidRefreshTokenError

    def validate_and_save_tokens(self, unvalidated_creds: Dict):
        """
        Validate and save the token

        Parameters
        __________
        unvalidated_creds: dict
            The unvalidated credentials to be validated
        """
        self.validate_tokens(unvalidated_creds)
        try:
            self.save_tokens(self._tokens)
        except Exception as e:
            logger.error("Error while persisting tokens", exc_info=e)

        return self

    def validate_tokens(self, unvalidated_creds: Dict):
        """
        Validate the token

        Paramaters
        ----------
        unvalidated_creds: dict
            The unvalidated credentials to be validated
        """
        creds = UnvalidatedTokens.from_dict(unvalidated_creds)
        idt_body: Optional[Dict] = None

        try:
            at_body = jwt.decode(
                creds.access_token,
                options={"verify_signature": False},
            )

            if creds.id_token:
                idt_body = jwt.decode(
                    creds.id_token,
                    options={"verify_signature": False},
                )
        except Exception as e:
            logger.error("Invalid tokens", exc_info=e)
            raise

        self._access_token_body = at_body
        self._id_token_body = idt_body
        self._tokens = ValidTokens.from_unvalidated(
            creds=creds,
            body=at_body,
        )
        self.token_scope = self._tokens.scope

        return self

    def get_access_token_refresh_if_necessary(self, no_auto_refresh: bool = False, auto_refresh_threshold: int = 3600):
        """
        Retrieve the access token. Automatically refreshes the token when necessary.

        Parameters
        ___________
        no_auto_refresh: bool, optional
            Disable automatic token refresh. The default behavior is to automatically attempt to refresh the token if it can be refreshed and there is less than 1 hour before the token expires (default is False)
        auto_refresh_threshold: int, optional
            The amount of time remaining (in seconds) before token expiration after which a refresh is automatically attempted (default is 3600)

        Return
        ________
        access_token: str
        """

        self.load_tokens()
        if (
                not no_auto_refresh
                and self.ttl < dt.timedelta(seconds=auto_refresh_threshold)
        ):
            try:
                self.refresh()
            except InvalidRefreshTokenError:
                raise InvalidRefreshTokenError("Unable to refresh because the refresh token is not valid. Use 'no-auto-refresh' option to get token anyway. To resolve, re-authenticate")
        return self.access_token
