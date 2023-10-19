from supabase.client import Client

from laminhub_rest.core.instance._get_account_role_for_instance import (
    get_account_role_for_instance,
)
from laminhub_rest.orm._account import sb_select_account_by_handle
from laminhub_rest.orm._instance_related_accounts import sb_select_instance_accounts


def get_instance_accounts(
    account_handle: str, name: str, supabase_client: Client, access_token: str = None
):
    account = sb_select_account_by_handle(
        handle=account_handle, supabase_client=supabase_client
    )

    instance_accounts = sb_select_instance_accounts(
        account_id=account["id"], name=name, supabase_client=supabase_client
    )

    if instance_accounts is not None:
        collaborators = instance_accounts["account_instance"]
        if access_token is not None:
            role = get_account_role_for_instance(
                instance_id=instance_accounts["id"],
                supabase_client=supabase_client,
                access_token=access_token,
            )
        else:
            role = None
    else:
        collaborators = None
        role = None

    collaborators_with_role = {"accounts": collaborators, "role": role}

    return collaborators_with_role
