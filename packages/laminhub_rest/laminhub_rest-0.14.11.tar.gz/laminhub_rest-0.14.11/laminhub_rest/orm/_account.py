from supabase.client import Client

# SELECT


def sb_select_account_by_id(
    id: str,
    supabase_client: Client,
):
    data = supabase_client.table("account").select("*").eq("id", id).execute().data
    if len(data) == 0:
        return None
    return data[0]


def sb_select_account_by_handle(
    handle: str,
    supabase_client: Client,
):
    data = (
        supabase_client.table("account").select("*").eq("handle", handle).execute().data
    )
    if len(data) == 0:
        return None
    return data[0]


def sb_select_all_accounts(supabase_client: Client):
    accounts = supabase_client.table("account").select("*").execute().data
    return accounts


# INSERT


def sb_insert_account(
    account_fields: dict,
    supabase_client: Client,
):
    data = supabase_client.table("account").insert(account_fields).execute().data
    if len(data) == 0:
        return None
    return data[0]


# UPDATE


def sb_update_account(
    account_id: str,
    account_fields: dict,
    supabase_client: Client,
):
    data = (
        supabase_client.table("account")
        .update(account_fields)
        .eq("id", account_id)
        .execute()
        .data
    )
    if len(data) == 0:
        return None
    return data[0]


# DELETE


def sb_delete_account(
    handle: str,
    supabase_client: Client,
):
    data = supabase_client.table("account").delete().eq("handle", handle).execute().data
    if len(data) == 0:
        return None
    return data[0]
