from supabase.client import Client


def sb_select_account_instances(
    handle: str,
    supabase_client: Client,
):
    account_instances = (
        supabase_client.table("account")
        .select(
            "account_instance(instance(*, storage(root),"
            " account!fk_instance_account_id_account(handle, id)))"
        )
        .eq("handle", handle)
        .execute()
        .data[0]["account_instance"]
    )
    account_instances = [entry["instance"] for entry in account_instances]
    return account_instances


def sb_select_account_instances_with_role(
    handle: str,
    supabase_client: Client,
):
    account_instances = (
        supabase_client.table("account")
        .select(
            "account_instance(instance(*, storage(root),"
            " account!fk_instance_account_id_account(handle, id),"
            " cloud_run_instance(api_url, last_access_at)), role)"
        )
        .eq("handle", handle)
        .execute()
        .data[0]["account_instance"]
    )
    return account_instances


def sb_select_account_own_instances(
    handle: str,
    supabase_client: Client,
):
    own_instances = (
        supabase_client.table("account")
        .select(
            "instance!fk_instance_account_id_account(*, storage(root),"
            " account!fk_instance_account_id_account(handle, id))"
        )
        .eq("handle", handle)
        .execute()
        .data[0]["instance"]
    )
    return own_instances
