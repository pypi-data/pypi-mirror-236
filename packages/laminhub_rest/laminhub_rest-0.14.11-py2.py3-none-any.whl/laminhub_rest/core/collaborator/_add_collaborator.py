from supabase.client import Client

from laminhub_rest.core.instance._get_instance_by_name import get_instance_by_name
from laminhub_rest.orm._account import sb_select_account_by_handle
from laminhub_rest.orm._account_instance import sb_insert_collaborator
from laminhub_rest.orm._db_user import sb_select_db_user_by_instance


def add_collaborator(
    handle: str,
    instance_owner_handle: str,
    instance_name: str,
    supabase_client: Client,
    role: str = "read",
):
    account = sb_select_account_by_handle(
        handle=handle, supabase_client=supabase_client
    )

    if account is None:
        return "account-not-exists"

    response = get_instance_by_name(
        account_handle=instance_owner_handle,
        name=instance_name,
        supabase_client=supabase_client,
    )

    if response["instance"] is None:
        return "instance-not-exists"

    if response["instance"]["db"] is None or response["instance"]["db"].startswith(
        "sqlite://"
    ):
        db_user_id = None
    else:
        db_user = sb_select_db_user_by_instance(
            instance_id=response["instance"]["id"], supabase_client=supabase_client
        )
        if db_user is None:
            return "db-user-not-reachable"
        else:
            db_user_id = db_user["id"]

    account_instance_fields = {
        "account_id": account["id"],
        "instance_id": response["instance"]["id"],
        "role": role,
        "db_user_id": db_user_id,
    }
    data = sb_insert_collaborator(
        account_instance_fields=account_instance_fields, supabase_client=supabase_client
    )
    assert data is not None

    if data == "collaborator-exists-already":
        return data
    return "success"
