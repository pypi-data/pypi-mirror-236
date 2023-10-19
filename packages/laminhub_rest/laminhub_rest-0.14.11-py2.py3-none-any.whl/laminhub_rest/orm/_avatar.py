from typing import Annotated

from fastapi import Query
from supabase.client import Client


def sb_select_single_avatar(
    lnid: str,
    supabase_client: Client,
):
    data = (
        supabase_client.table("account")
        .select("avatar_url")
        .eq("lnid", lnid)
        .execute()
        .data
    )
    if len(data) == 0:
        return None
    return data[0]["avatar_url"]


def sb_select_bulk_avatars(
    lnids: Annotated[list[str], Query()],
    supabase_client: Client,
):
    data = (
        supabase_client.table("account")
        .select("lnid, avatar_url")
        .in_("lnid", lnids)
        .execute()
        .data
    )
    if len(data) == 0:
        return []
    return data
