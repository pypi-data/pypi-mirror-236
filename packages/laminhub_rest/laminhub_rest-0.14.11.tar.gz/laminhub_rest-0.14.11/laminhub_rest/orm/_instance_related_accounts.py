from supabase.client import Client


def sb_select_instance_accounts(
    account_id: str,
    name: str,
    supabase_client: Client,
):
    data = (
        supabase_client.table("instance")
        .select("""id, account_instance(*, account(*))""")
        .eq("account_id", account_id)
        .eq("name", name)
        .execute()
        .data
    )
    if len(data) == 0:
        return None
    return data[0]
