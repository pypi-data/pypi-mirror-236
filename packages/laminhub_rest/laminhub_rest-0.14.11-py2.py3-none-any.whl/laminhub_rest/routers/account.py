from typing import Annotated, Union

from fastapi import APIRouter, Header, Query

from laminhub_rest.orm._account import (
    sb_select_account_by_handle,
    sb_select_account_by_id,
)
from laminhub_rest.orm._avatar import sb_select_bulk_avatars, sb_select_single_avatar
from laminhub_rest.utils._access_token import extract_id

from ..core.account._create_account import create_user_account
from ..core.account._create_organization_account import create_organization_account
from ..core.account._get_account_instances import (
    get_account_instances as get_account_instances_base,
)
from ..core.account._get_account_instances import (
    get_account_instances_with_role as get_account_instances_with_role_base,
)
from ..core.account._get_account_organizations import (
    get_account_organizations as get_account_organizations_base,
)
from ..core.account._update_account import update_account as update_account_base
from ..utils._supabase_client import SbClientAnonymous, SbClientFromAccesToken
from .utils import extract_access_token

router = APIRouter(prefix="/account")


@router.post("/")
def create_account(
    handle: str,
    organization: Union[bool, None] = False,
    authentication: Union[str, None] = Header(default=None),
):
    """Create user or organization account in the Hub.

    Returns:
        message (str): status message. "success" or "handle-exists-already".
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        if organization:
            message = create_organization_account(
                user_id=extract_id(access_token),
                handle=handle,
                supabase_client=supabase_client,
            )
        else:
            message = create_user_account(
                id=extract_id(access_token),
                handle=handle,
                supabase_client=supabase_client,
            )

    if message is None:
        return "success"
    return message


@router.put("/")
def update_account(
    handle: Union[str, None] = None,
    name: Union[str, None] = None,
    bio: Union[str, None] = None,
    github_handle: Union[str, None] = None,
    linkedin_handle: Union[str, None] = None,
    twitter_handle: Union[str, None] = None,
    website: Union[str, None] = None,
    authentication: Union[str, None] = Header(default=None),
):
    """Update account in the Hub.

    Returns:
        message (str): status message. "sucess" or "account-not-exists".
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        message = update_account_base(
            id=extract_id(access_token),
            handle=handle,
            name=name,
            bio=bio,
            github_handle=github_handle,
            linkedin_handle=linkedin_handle,
            twitter_handle=twitter_handle,
            website=website,
            supabase_client=supabase_client,
        )

    if message is None:
        return "success"
    return message


@router.get("/bulk/avatars")
def get_account_avatars(lnids: Annotated[list[str], Query()]):
    """Get list of account records with their avatar URLs.

    Returns:
        bulk_avatars (List): list of account(lnid, avatar_url) records.
            Empty list if none are found.
    """
    with SbClientAnonymous().connect() as supabase_client:
        return sb_select_bulk_avatars(lnids, supabase_client)


@router.get("/avatar")
def get_account_avatar(lnid: str):
    """Get avatar URL for a single account.

    Returns:
        avatar (Union[str, None]): avatar URL. Returns None if not found.
    """
    with SbClientAnonymous().connect() as supabase_client:
        return sb_select_single_avatar(lnid, supabase_client)


@router.get("/{id}")
def get_account_by_id(id: str):
    """Get single account associated with an id.

    Returns:
        account (Union[dict, None]): account(*) record. Returns None if not found.
    """
    with SbClientAnonymous().connect() as supabase_client:
        return sb_select_account_by_id(id, supabase_client)


@router.get("/handle/{handle}")
def get_account_by_handle(handle: str):
    """Get single account associated with a handle.

    Returns:
        account (Union[dict, None]): account(*) record. Returns None if not found.
    """
    with SbClientAnonymous().connect() as supabase_client:
        return sb_select_account_by_handle(handle, supabase_client)


@router.get("/resources/instances/{handle}")
def get_account_instances(
    handle: str,
    owner: bool = False,
    authentication: Union[str, None] = Header(default=None),
):
    """Get list of instances in which an account is a collaborator.

    Returns:
        account_instances (List): list of instance(*, storage(root),
            account(handle, id)) records. Returns empty list if not found.
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        return get_account_instances_base(
            handle=handle, owner=owner, supabase_client=supabase_client
        )


@router.get("/resources/instances-with-role/{handle}")
def get_account_instances_with_role(
    handle: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Get list of instances, with role, in which an account is a collaborator.

    Returns:
        account_instances (List): list of (instance(*, storage(root),
            account(handle, id), cloud_run_instance(api_url, last_access_at)),
            role) records. Returns empty list if not found.
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        return get_account_instances_with_role_base(
            handle=handle, supabase_client=supabase_client
        )


@router.get("/resources/organizations/{handle}")
def get_account_organizations(
    handle: str, authentication: Union[str, None] = Header(default=None)
):
    """Get list of organization_user records with which an account is associated.

    Returns:
        organizations_user (List): list of organization_user(*, account(*))
            records. Returns empty list if not found.
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        return get_account_organizations_base(
            handle=handle, supabase_client=supabase_client
        )
