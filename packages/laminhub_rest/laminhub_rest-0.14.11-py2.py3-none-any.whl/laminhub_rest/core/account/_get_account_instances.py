from supabase.client import Client

from laminhub_rest.orm._account_related_instances import (
    sb_select_account_instances,
    sb_select_account_instances_with_role,
    sb_select_account_own_instances,
)


def get_account_instances(
    handle: str,
    supabase_client: Client,
    owner: bool = False,
):
    if owner:
        return sb_select_account_own_instances(handle, supabase_client)
    else:
        return sb_select_account_instances(handle, supabase_client)


def get_account_instances_with_role(
    handle: str,
    supabase_client: Client,
):
    return sb_select_account_instances_with_role(handle, supabase_client)
