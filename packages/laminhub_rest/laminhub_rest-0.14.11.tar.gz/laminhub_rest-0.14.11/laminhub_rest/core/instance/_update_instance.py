from typing import Optional, Union

from supabase.client import Client

from laminhub_rest.orm._instance import sb_update_instance
from laminhub_rest.utils._query import filter_null_from_dict


def update_instance(
    instance_id: str,
    supabase_client: Client,
    account_id: Union[str, None] = None,
    public: Optional[bool] = False,
    description: Optional[str] = None,
) -> Union[None, str]:
    fields = filter_null_from_dict(
        {
            "account_id": account_id,
            "public": public,
            "description": description,
        }
    )

    instance = sb_update_instance(instance_id, fields, supabase_client)

    if instance is None:
        return "instance-not-updated"

    return None
