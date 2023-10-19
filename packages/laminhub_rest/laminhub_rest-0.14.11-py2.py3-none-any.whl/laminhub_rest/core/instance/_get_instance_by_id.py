from supabase.client import Client

from laminhub_rest.core.instance._get_account_role_for_instance import (
    get_account_role_for_instance,
)
from laminhub_rest.orm._instance import sb_select_full_instance


def get_instance_by_id(id: str, supabase_client: Client, access_token: str = None):
    instance = sb_select_full_instance(id, supabase_client)

    if instance is not None:
        if access_token is not None:
            role = get_account_role_for_instance(
                access_token=access_token,
                instance_id=id,
                supabase_client=supabase_client,
            )
        else:
            role = None
    else:
        role = None

    instance_with_role = {"instance": instance, "role": role}

    return instance_with_role
