from typing import Optional, Union

from supabase.client import Client

from laminhub_rest.orm._account import sb_update_account
from laminhub_rest.utils._query import filter_null_from_dict


def update_account(
    id: str,
    supabase_client: Client,
    handle: Optional[str] = None,
    name: Optional[str] = None,
    bio: Optional[str] = None,
    github_handle: Optional[str] = None,
    linkedin_handle: Optional[str] = None,
    twitter_handle: Optional[str] = None,
    website: Optional[str] = None,
) -> Union[None, str]:
    data = supabase_client.table("account").select("*").eq("id", id).execute().data

    if len(data) == 0:
        return "account-not-exists"

    fields = filter_null_from_dict(
        {
            "id": id,
            "handle": handle,
            "name": name,
            "bio": bio,
            "github_handle": github_handle,
            "linkedin_handle": linkedin_handle,
            "twitter_handle": twitter_handle,
            "website": website,
        }
    )

    account = sb_update_account(id, fields, supabase_client)
    assert account is not None

    return None
