from typing import Dict, Optional

from supabase.client import Client

# SELECT


def select_instance_by_owner_name(
    owner: str,
    name: str,
    client: Client,
) -> Optional[Dict]:
    data = (
        client.table("instance")
        .select("*, account!inner!fk_instance_account_id_account(*)")
        .eq("account.handle", owner)
        .eq("name", name)
        .execute()
        .data
    )
    if len(data) == 0:
        return None
    return data[0]


def sb_select_instance(
    id: str,
    supabase_client: Client,
):
    data = supabase_client.table("instance").select("*").eq("id", id).execute().data
    if len(data) == 0:
        return None
    return data[0]


def sb_select_full_instance(
    id: str,
    supabase_client: Client,
):
    data = (
        supabase_client.table("instance")
        .select("*, storage(root), account!fk_instance_account_id_account(handle, id))")
        .eq("id", id)
        .execute()
        .data
    )
    if len(data) == 0:
        return None
    return data[0]


def sb_select_instance_by_name(
    account_id: str,
    name: str,
    supabase_client: Client,
):
    data = (
        supabase_client.table("instance")
        .select("*")
        .eq("account_id", account_id)
        .eq("name", name)
        .execute()
        .data
    )
    if len(data) == 0:
        return None
    return data[0]


def sb_select_full_instance_by_name(
    account_id: str,
    name: str,
    supabase_client: Client,
):
    data = (
        supabase_client.table("instance")
        .select("*, storage(root), account!fk_instance_account_id_account(handle, id))")
        .eq("account_id", account_id)
        .eq("name", name)
        .execute()
        .data
    )
    if len(data) == 0:
        return None
    return data[0]


# INSERT


def sb_insert_instance(instance_fields: dict, supabase_client: Client):
    try:
        (
            supabase_client.table("instance")
            .insert(instance_fields, returning="minimal")
            .execute()
            .data
        )
    except Exception as e:
        if str(e) == str("Expecting value: line 1 column 1 (char 0)"):
            pass
        else:
            raise e
    return sb_select_instance_by_name(
        instance_fields["account_id"], instance_fields["name"], supabase_client
    )


# UPDATE


def sb_update_instance(
    instance_id: str, instance_fields: dict, supabase_client: Client
):
    data = (
        supabase_client.table("instance")
        .update(instance_fields)
        .eq("id", instance_id)
        .execute()
        .data
    )
    if len(data) == 0:
        return None
    return data[0]


# DELETE


def sb_delete_instance(
    id: str,
    supabase_client: Client,
):
    data = supabase_client.table("instance").delete().eq("id", id).execute().data
    if len(data) == 0:
        return None
    return data[0]
