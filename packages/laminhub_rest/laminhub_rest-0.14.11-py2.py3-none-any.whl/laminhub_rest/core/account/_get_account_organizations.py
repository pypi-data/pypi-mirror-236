from supabase.client import Client

from laminhub_rest.orm._account import sb_select_account_by_handle
from laminhub_rest.orm._account_related_organizations import (
    sb_select_user_organizations,
)


def get_account_organizations(handle: str, supabase_client: Client):
    user_id = sb_select_account_by_handle(handle, supabase_client)["id"]
    return sb_select_user_organizations(user_id, supabase_client)
