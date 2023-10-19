from supabase.client import Client

from laminhub_rest.core.instance._get_account_role_for_instance import (
    get_account_role_for_instance,
)
from laminhub_rest.orm._account import sb_select_account_by_handle
from laminhub_rest.orm._instance import sb_select_full_instance_by_name


def get_instance_by_name(
    account_handle: str, name: str, supabase_client: Client, access_token: str = None
):
    account = sb_select_account_by_handle(
        handle=account_handle, supabase_client=supabase_client
    )

    instance = sb_select_full_instance_by_name(
        account_id=account["id"], name=name, supabase_client=supabase_client
    )

    if instance is not None:
        if access_token is not None:
            role = get_account_role_for_instance(
                instance_id=instance["id"],
                supabase_client=supabase_client,
                access_token=access_token,
            )
        else:
            role = None
    else:
        role = None

    instance_with_role = {"instance": instance, "role": role}

    return instance_with_role
