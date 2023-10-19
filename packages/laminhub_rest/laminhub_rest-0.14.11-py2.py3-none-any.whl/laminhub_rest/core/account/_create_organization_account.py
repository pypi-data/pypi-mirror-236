from typing import Union
from uuid import uuid4

from postgrest.exceptions import APIError
from supabase.client import Client

from laminhub_rest.orm._account import sb_insert_account
from laminhub_rest.orm._organization_user import sb_insert_member
from laminhub_rest.utils._id import base62


def create_organization_account(
    handle: str,
    user_id: str,  # account_is of the user who create the organization
    supabase_client: Client,
) -> Union[None, str]:
    try:
        lnid = base62(8)

        organization = sb_insert_account(
            {
                "id": uuid4().hex,
                "user_id": None,
                "lnid": lnid,
                "handle": handle,
            },
            supabase_client,
        )
        assert organization is not None

        member = sb_insert_member(
            {
                "organization_id": organization["id"],
                "user_id": user_id,
                "role": "owner",
            },
            supabase_client,
        )
        assert member is not None

        return None

    except APIError as api_error:
        # allowed errors
        message = api_error.message
        error1 = 'duplicate key value violates unique constraint "pk_account"'
        error2 = 'duplicate key value violates unique constraint "usermeta_pkey"'
        if message == error1 or message == error2:
            return "handle-exists-already"
        raise api_error

    except Exception as e:
        raise e
