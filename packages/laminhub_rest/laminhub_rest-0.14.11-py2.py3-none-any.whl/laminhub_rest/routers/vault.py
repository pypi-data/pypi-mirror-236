from typing import Union

from fastapi import APIRouter, Header
from lamin_vault.server._create_instance_admin_token_from_jwt import (
    create_instance_admin_token_from_jwt as create_instance_admin_token_from_jwt_base,
)
from lamin_vault.server._create_token_from_jwt import (
    create_token_from_jwt as create_token_from_jwt_base,
)
from lamin_vault.server._get_vault_client_approle import get_vault_approle_client

from laminhub_rest.routers.utils import extract_access_token

router = APIRouter(prefix="/vault")


@router.post("/token/from-jwt/{instance_id}")
def create_token_from_jwt(
    instance_id: str, authentication: Union[str, None] = Header(default=None)
):
    vault_client = get_vault_approle_client()
    access_token = extract_access_token(authentication)
    return create_token_from_jwt_base(vault_client, access_token, instance_id)


@router.post("/token/from-jwt/admin/{instance_id}")
def create_instance_admin_token_from_jwt(
    instance_id: str, authentication: Union[str, None] = Header(default=None)
):
    vault_client = get_vault_approle_client()
    access_token = extract_access_token(authentication)
    return create_instance_admin_token_from_jwt_base(
        vault_client, access_token, instance_id
    )
