from typing import Union

from supabase.client import Client

from laminhub_rest.orm._account import sb_select_account_by_handle
from laminhub_rest.orm._instance import sb_delete_instance, sb_select_instance_by_name


def delete_instance(
    *, owner: str, name: str, supabase_client: Client
) -> Union[None, str]:
    # get account
    account = sb_select_account_by_handle(owner, supabase_client)
    if account is None:
        return "account-not-exists"

    # get instance
    instance = sb_select_instance_by_name(account["id"], name, supabase_client)
    if instance is None:
        return "instance-not-reachable"

    sb_delete_instance(instance["id"], supabase_client)

    # TODO: delete storage if no other instances use it
    return None
