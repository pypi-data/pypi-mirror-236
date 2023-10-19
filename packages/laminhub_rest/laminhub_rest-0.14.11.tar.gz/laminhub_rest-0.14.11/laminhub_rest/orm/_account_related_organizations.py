from supabase.client import Client


def sb_select_user_organizations(
    user_id: str,
    supabase_client: Client,
):
    organizations_user = (
        supabase_client.table("organization_user")
        .select("""*, account(*)""")
        .eq("user_id", user_id)
        .execute()
        .data
    )
    return organizations_user
