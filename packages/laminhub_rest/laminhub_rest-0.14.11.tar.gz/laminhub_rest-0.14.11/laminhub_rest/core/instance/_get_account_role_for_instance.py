import jwt
from supabase.client import Client

# TODO: Remove the code in this block
from laminhub_rest.orm._account_instance import sb_select_collaborator_role
from laminhub_rest.utils._supabase_client import SbClientFromAccesToken


def get_account_role_for_instance(
    instance_id: str, access_token: str, supabase_client: Client
):
    session_payload = jwt.decode(
        access_token, algorithms="HS256", options={"verify_signature": False}
    )

    account_id = session_payload["sub"]

    with SbClientFromAccesToken(access_token).connect() as supabase_client:
        role = sb_select_collaborator_role(
            account_id=account_id,
            instance_id=instance_id,
            supabase_client=supabase_client,
        )

    return role
