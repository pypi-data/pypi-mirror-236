from typing import Union

from fastapi import Header

# TODO: Remove the code in this block
from laminhub_rest.connector import connect_hub, connect_hub_with_auth

from ..utils._supabase_client import SbClientFromAccesToken

supabase_client = connect_hub()


def get_supabase_client(access_token: Union[str, None]):
    if access_token is None:
        return connect_hub()
    else:
        return connect_hub_with_auth(access_token=access_token)


# (end of the block)


def extract_access_token(authentication: Union[str, None] = Header(default=None)):
    if authentication is not None:
        return authentication.split(" ")[1]
    return None


def get_user_by_id(id: str, authentication: Union[str, None] = Header(default=None)):
    access_token = extract_access_token(authentication)

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        user = supabase_client.table("users").select("*").eq("id", id).execute().data

    if len(user) == 0:
        return None
    return user[0]
