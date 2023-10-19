from typing import Union

from supabase.client import Client

from laminhub_rest.orm._account import sb_insert_account
from laminhub_rest.utils._id import base62


def create_user_account(
    handle: str,
    id: str,
    supabase_client: Client,
) -> Union[None, str]:
    account = sb_insert_account(
        {
            "id": id,
            "user_id": id,
            "lnid": base62(8),
            "handle": handle,
        },
        supabase_client,
    )
    assert account is not None

    return None
