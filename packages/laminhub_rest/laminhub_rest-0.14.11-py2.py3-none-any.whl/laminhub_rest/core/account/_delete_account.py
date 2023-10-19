from typing import Union

from supabase.client import Client

from laminhub_rest.orm._account import sb_delete_account, sb_select_account_by_handle
from laminhub_rest.orm._account_instance import (
    sb_delete_collaborator_from_all_instances,
)


def delete_account(
    handle: str,  # owner handle
    supabase_client: Client,
) -> Union[None, str]:
    account = sb_select_account_by_handle(handle, supabase_client)
    sb_delete_collaborator_from_all_instances(account["id"], supabase_client)
    sb_delete_account(handle, supabase_client)
    return None
