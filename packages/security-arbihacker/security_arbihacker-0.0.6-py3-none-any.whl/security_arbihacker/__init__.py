import logging
import re

from fastapi import HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes, HTTPBearer
from jose import jwt, JWTError

__all__ = [
    "JWTBearer",
    "get_security",
    "CredentialsException",
    "check_token_and_scopes",
]


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> str | None:
        result = await super().__call__(request)
        if result is None:
            return None
        return result.credentials


def get_security(
    token_url: str | None = None,
    auto_error: bool = True,
    scheme_name: str | None = None,
    description: str | None = None,
):
    if token_url is None:
        return JWTBearer(
            auto_error=auto_error, scheme_name=scheme_name, description=description
        )
    else:
        return OAuth2PasswordBearer(
            tokenUrl=token_url,
            auto_error=auto_error,
            scheme_name=scheme_name,
            description=description,
        )


class CredentialsException(HTTPException):
    def __init__(self, authenticate_value="bearer") -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )


def check_token_and_scopes(
    security_scopes: SecurityScopes,
    token: str,
    key: str | dict,
    algorithms: str | list,
    auto_error=True,
) -> dict | None:
    if security_scopes.scopes:
        authenticate_value = f"bearer scope={security_scopes.scope_str}"
    else:
        authenticate_value = "bearer"
    try:
        payload = jwt.decode(token, key, algorithms=algorithms)
        if "sub" not in payload:
            raise KeyError("sub claim is not present")
        if not security_scopes.scopes:
            return payload
        security_scopes_scopes = set(security_scopes.scopes)
        for scope in payload["scope"].split(" "):
            # scopes are in format prefix:service:entity:action, wildcard is supported
            # prefix:service:entity:action grant access to prefix:service:entity, prefix:service and prefix as well
            # this way prefix:service:entity is weaker than prefix:service:entity:action,
            # but prefix:service:entity:* is stronger than prefix:service:entity:action
            if scope in security_scopes_scopes.union({"role:*", "role:superuser"}):
                break
            for i in range(len(scope.split(":"))):
                partial_scope = ":".join(scope.split(":")[: i + 1]).replace("*", ".*")
                for security_scope in security_scopes_scopes:
                    if re.match(partial_scope, security_scope):
                        break
                else:
                    raise KeyError(f"Scope not present: {security_scopes_scopes}")
        return payload
    except (JWTError, KeyError, ValueError):
        logging.error("Invalid JWT token during authentication")
        if auto_error:
            raise CredentialsException(authenticate_value)
        else:
            return None
