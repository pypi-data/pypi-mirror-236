from typing import Union

from fastapi import APIRouter, Header

from laminhub_rest.core.collaborator._add_collaborator import (
    add_collaborator as add_collaborator_base,
)
from laminhub_rest.core.instance._delete_instance import (
    delete_instance as delete_instance_base,
)
from laminhub_rest.core.instance._get_instance_accounts import (
    get_instance_accounts as get_instance_accounts_base,
)
from laminhub_rest.core.instance._get_instance_by_id import (
    get_instance_by_id as get_instance_by_id_base,
)
from laminhub_rest.core.instance._get_instance_by_name import (
    get_instance_by_name as get_instance_by_name_base,
)
from laminhub_rest.core.instance._update_instance import (
    update_instance as update_instance_base,
)

from ..utils._supabase_client import SbClientFromAccesToken
from .utils import extract_access_token

router = APIRouter(prefix="/instance")


@router.get("/{id}")
def get_instance_by_id(
    id: str,
    authentication: Union[str, None] = Header(default=None),
):
    access_token = extract_access_token(authentication)
    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        return get_instance_by_id_base(
            id=id, supabase_client=supabase_client, access_token=access_token
        )


@router.get("/{account_handle}/{name}")
def get_instance_by_name(
    account_handle: str,
    name: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Get full instance information by name.

    Returns:
        instance_with_role (dict): dictionary with keys "instance" and "role".
            "instance": instance(*, storage(root), account(handle, id))
            "role": "admin", "write", or "read"
    """
    access_token = extract_access_token(authentication)
    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        return get_instance_by_name_base(
            account_handle=account_handle,
            name=name,
            supabase_client=supabase_client,
            access_token=access_token,
        )


@router.get("/resources/accounts/{account_handle}/{name}")
def get_instance_accounts(
    account_handle: str,
    name: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Get collaborators of an instance.

    Returns:
        collaborators_with_role (dict):  dictionary with keys "accounts" and "role".
            "accounts": account_instance(*, account(*)). Returns None if no
                collaborators exist.
            "role": "admin", "write", or "read". Returns None if caller not
                authenticated or no collaborators exist.
    """
    access_token = extract_access_token(authentication)
    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        return get_instance_accounts_base(
            account_handle=account_handle,
            name=name,
            supabase_client=supabase_client,
            access_token=access_token,
        )


@router.post("/resources/accounts/")
def add_collaborator(
    handle: str,
    instance_owner_handle: str,
    instance_name: str,
    role: str = "read",
    authentication: Union[str, None] = Header(default=None),
):
    """Add collaborator in the hub.

    Returns:
        message (str): status message. "success", "collaborator-exists-already",
            or "account-not-exists".
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        return add_collaborator_base(
            handle=handle,
            instance_owner_handle=instance_owner_handle,
            instance_name=instance_name,
            role=role,
            supabase_client=supabase_client,
        )


@router.delete("/")
def delete_instance(
    account_handle: str,
    name: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Delete instance in the hub.

    Returns:
        message (str): status message. "sucess", "account-not-exists", or
            "instance-not-reachable".
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        message = delete_instance_base(
            owner=account_handle, name=name, supabase_client=supabase_client
        )

    if message is None:
        return "success"
    return message


@router.put("/")
def update_instance(
    instance_id: str,
    account_id: Union[str, None] = None,
    public: Union[bool, None] = None,
    description: Union[str, None] = None,
    authentication: Union[str, None] = Header(default=None),
):
    """Update instance in the Hub.

    Returns:
        message (str): status message. "success" or "instance-not-updated".
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        message = update_instance_base(
            instance_id=instance_id,
            account_id=account_id,
            public=public,
            description=description,
            supabase_client=supabase_client,
        )

    if message is None:
        return "success"
    return message
