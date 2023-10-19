from typing import Union

from fastapi import APIRouter, Header
from lamin_logger import logger
from lamin_vault.client._create_vault_client import create_vault_admin_client
from lamin_vault.client._set_collaborator_role import set_collaborator_role
from lamin_vault.client.postgres._delete_db_role import delete_db_role

from laminhub_rest.orm._account_instance import (
    sb_delete_collaborator,
    sb_select_collaborator,
    sb_update_collaborator,
)

from ..utils._supabase_client import SbClientFromAccesToken
from .instance import get_instance_by_name
from .utils import extract_access_token

router = APIRouter(prefix="/instance/collaborator")


@router.get("/{account_handle}/{name}")
def is_collaborator(
    instance_id: str,
    account_id: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Check if collaborator exists.

    Returns:
        collaborator_exists (bool): False or True.
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        collaborator = sb_select_collaborator(instance_id, account_id, supabase_client)

    return collaborator is not None


@router.put("/{account_handle}/{name}")
def update_collaborator(
    account_handle: str,
    name: str,
    account_id: str,
    role: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Update collaborator entry in the Hub.

    Returns:
        collaborator (Union[dict, str]): updated collaborator record.
            Returns "update-failed" for unsuccessful operations.
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        instance_id = get_instance_by_name(
            account_handle=account_handle, name=name, authentication=authentication
        )["instance"]["id"]
        collaborator = sb_update_collaborator(
            instance_id=instance_id,
            account_id=account_id,
            role=role,
            supabase_client=supabase_client,
        )

    try:
        set_collaborator_role(
            instance_id=instance_id,
            account_id=account_id,
            role_name=role,
            access_token=access_token,
        )
    except Exception as e:
        logger.error("Failed to set db role in vault for the new collaborator.")
        logger.error(e)

    if collaborator is None:
        return "update-failed"
    else:
        return collaborator


@router.delete("/{account_handle}/{name}")
def delete_collaborator(
    account_handle: str,
    name: str,
    account_id: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Delete collaborators in the hub.

    Returns"
        collaborator (Union[dict, str]): deleted collaborator record.
            Returns "delete-failed" for unsuccessful operations.
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        instance_id = get_instance_by_name(
            account_handle=account_handle, name=name, authentication=authentication
        )["instance"]["id"]
        collaborator = sb_delete_collaborator(
            instance_id=instance_id,
            account_id=account_id,
            supabase_client=supabase_client,
        )

        try:
            vault_admin_client = create_vault_admin_client(access_token, instance_id)
            delete_db_role(vault_admin_client, instance_id, account_id)
        except Exception as e:
            logger.error("Failed to delete db role in vault.")
            logger.error(e)

    if collaborator is None:
        return "delete-failed"
    else:
        return collaborator
