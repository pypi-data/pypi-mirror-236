from typing import Union

from fastapi import APIRouter, Header

from laminhub_rest.orm._organization_user import (
    sb_delete_member,
    sb_insert_member,
    sb_select_members,
    sb_update_member,
)

from ..utils._supabase_client import SbClientFromAccesToken
from .utils import extract_access_token

router = APIRouter(prefix="/organization")


@router.get("/resources/members/{organization_id}")
def get_organization_members(
    organization_id: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Get members of an organization in the Hub.

    Returns:
        members (List): list of member records. Returns empty list if no members
            are found.
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        members = sb_select_members(organization_id, supabase_client)

    return members


@router.post("/resources/members/{organization_id}/")
def add_member(
    organization_id: str,
    user_id: str,
    role: Union[str, None] = "member",
    authentication: Union[str, None] = Header(default=None),
):
    """Add member to an organization in the Hub.

    Returns:
        message (str): status message. "sucess" or "member-not-added".
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        organization_user_fields = {
            "organization_id": organization_id,
            "user_id": user_id,
            "role": role,
        }
        member = sb_insert_member(organization_user_fields, supabase_client)

    if member is not None:
        return "success"
    else:
        return "member-not-added"


@router.put("/resources/members/{organization_id}/")
def update_member(
    organization_id: str,
    user_id: str,
    role: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Update member of an organization in the Hub.

    Returns:
        message (str): status message. "sucess" or "member-not-updated".
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        member = sb_update_member(organization_id, user_id, role, supabase_client)

    if member is not None:
        return "success"
    else:
        return "member-not-updated"


@router.delete("/resources/members/{organization_id}/")
def remove_member(
    organization_id: str,
    user_id: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Remove member from an organization in the Hub.

    Returns:
        message (str): status message. "sucess" or "member-not-deleted".
    """
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        member = sb_delete_member(organization_id, user_id, supabase_client)

    if member is not None:
        return "success"
    else:
        return "member-not-deleted"
